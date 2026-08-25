<script module lang="ts">
  let kicanvasPromise: Promise<void> | null = null;

  function loadKiCanvas() {
    if (customElements.get('kicanvas-embed')) return Promise.resolve();
    if (kicanvasPromise) return kicanvasPromise;
    kicanvasPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.type = 'module';
      script.src = '/vendor/kicanvas/kicanvas.js';
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('KiCanvas failed to load'));
      document.head.appendChild(script);
    });
    return kicanvasPromise;
  }
</script>

<script lang="ts">
  import { tick } from 'svelte';

  let {
    src,
    poster,
    title
  }: { src: string; poster?: string; title: string } = $props();

  let active = $state(false);
  let error = $state('');
  let viewerElement = $state<HTMLElement>();
  const configuredCanvases = new WeakSet<HTMLCanvasElement>();

  type KiCanvasPreferences = {
    alignControlsWithKiCad: boolean;
    save: () => void;
  };

  function preferWheelZoom() {
    localStorage.setItem(
      'kc:prefs:alignControlsWithKiCad',
      JSON.stringify({ val: true })
    );
  }

  function applyWheelZoomPreference(root: ParentNode) {
    for (const element of root.querySelectorAll<HTMLElement>('*')) {
      const preferences = (element as HTMLElement & { preferences?: KiCanvasPreferences })
        .preferences;
      if (preferences && !preferences.alignControlsWithKiCad) {
        preferences.alignControlsWithKiCad = true;
        preferences.save();
      }
      if (element.shadowRoot) applyWheelZoomPreference(element.shadowRoot);
    }
  }

  function enableLeftDragPan(root: ParentNode) {
    for (const canvas of root.querySelectorAll<HTMLCanvasElement>('canvas')) {
      if (configuredCanvases.has(canvas)) continue;
      configuredCanvases.add(canvas);

      let dragging = false;
      let moved = false;
      let startX = 0;
      let startY = 0;

      const relayAsMiddleClick = (type: 'mousedown' | 'mouseup', event: MouseEvent) => {
        canvas.dispatchEvent(
          new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            composed: true,
            button: 1,
            buttons: type === 'mousedown' ? 4 : 0,
            clientX: event.clientX,
            clientY: event.clientY,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey,
            altKey: event.altKey,
            metaKey: event.metaKey
          })
        );
      };

      canvas.addEventListener(
        'mousedown',
        (event) => {
          if (event.button === 2) {
            event.preventDefault();
            event.stopImmediatePropagation();
            return;
          }
          if (event.button !== 0) return;

          dragging = true;
          moved = false;
          startX = event.clientX;
          startY = event.clientY;
          event.preventDefault();
          event.stopImmediatePropagation();
          relayAsMiddleClick('mousedown', event);
        },
        true
      );
      canvas.addEventListener(
        'mousemove',
        (event) => {
          if (dragging && Math.hypot(event.clientX - startX, event.clientY - startY) > 3) {
            moved = true;
          }
        },
        true
      );
      canvas.addEventListener(
        'mouseup',
        (event) => {
          if (!dragging || event.button !== 0) return;
          dragging = false;
          event.preventDefault();
          event.stopImmediatePropagation();
          relayAsMiddleClick('mouseup', event);
        },
        true
      );
      canvas.addEventListener(
        'click',
        (event) => {
          if (moved) {
            event.preventDefault();
            event.stopImmediatePropagation();
          }
        },
        true
      );
    }

    for (const element of root.querySelectorAll<HTMLElement>('*')) {
      if (element.shadowRoot) enableLeftDragPan(element.shadowRoot);
    }
  }

  async function configureViewerControls() {
    preferWheelZoom();
    await tick();
    const configureCanvas = () => {
      if (viewerElement) {
        const root = viewerElement.shadowRoot || viewerElement;
        applyWheelZoomPreference(root);
        enableLeftDragPan(root);
      }
    };
    requestAnimationFrame(configureCanvas);
    // KiCanvas creates its nested canvas after its own initial render.
    window.setTimeout(configureCanvas, 250);
  }

  async function activate() {
    try {
      preferWheelZoom();
      await loadKiCanvas();
      active = true;
      await configureViewerControls();
    } catch {
      error = 'The board viewer could not load. The source file is still available.';
    }
  }

  function containViewerWheel(node: HTMLElement) {
    const contain = (event: WheelEvent) => {
      if (active) event.preventDefault();
    };
    node.addEventListener('wheel', contain, { passive: false });
    return {
      destroy: () => node.removeEventListener('wheel', contain)
    };
  }

</script>

<figure class="board-viewer">
  <div class="board-stage" use:containViewerWheel>
    {#if active}
      <svelte:element
        this={'kicanvas-embed'}
        {src}
        controls="basic"
        controlslist="nodownload nooverlay"
        bind:this={viewerElement}
      ></svelte:element>
    {:else}
      <button onclick={activate} aria-label={`Load interactive KiCanvas board: ${title}`}>
        {#if poster}<img src={poster} alt="" />{:else}<div class="board-placeholder">PCB</div>{/if}
        <span>{error || 'Inspect the board in KiCanvas'}</span>
      </button>
    {/if}
  </div>
  <figcaption>
    <span>KiCad artifact / left-drag to pan</span>
    {title}. Load the interactive board when you are ready to inspect it.
  </figcaption>
</figure>

<style>
  .board-viewer {
    margin: 0;
  }

  .board-stage {
    min-height: 560px;
    border: 1px solid var(--ink);
    background: #121722;
    overscroll-behavior: contain;
  }

  :global(kicanvas-embed) {
    display: block;
    width: 100%;
    height: 560px;
  }

  button {
    position: relative;
    display: block;
    width: 100%;
    height: 560px;
    padding: 0;
    overflow: hidden;
    border: 0;
    color: var(--paper-bright);
    background: #121722;
    cursor: pointer;
  }

  button img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.52) saturate(0.8);
  }

  .board-placeholder {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    color: rgba(232, 255, 98, 0.18);
    background:
      linear-gradient(rgba(232, 255, 98, 0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232, 255, 98, 0.06) 1px, transparent 1px),
      #121722;
    background-size: 24px 24px;
    font-family: 'Recursive Variable', monospace;
    font-size: 110px;
    font-weight: 900;
  }

  button span {
    position: absolute;
    top: 50%;
    left: 50%;
    width: max-content;
    max-width: calc(100% - 40px);
    padding: 14px 18px;
    border: 1px solid var(--acid);
    color: var(--acid);
    background: rgba(18, 23, 34, 0.9);
    font-family: 'Recursive Variable', monospace;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transform: translate(-50%, -50%);
  }

  figcaption {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    padding-top: 12px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.4;
  }

  figcaption span {
    color: var(--blue-dark);
    font-family: 'Recursive Variable', monospace;
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  @media (max-width: 700px) {
    .board-stage,
    :global(kicanvas-embed),
    button {
      min-height: 420px;
      height: 420px;
    }

    figcaption {
      display: block;
    }

    figcaption span {
      display: block;
      margin-bottom: 6px;
    }
  }
</style>
