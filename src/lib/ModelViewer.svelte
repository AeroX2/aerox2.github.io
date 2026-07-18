<script lang="ts">
  let {
    src,
    poster,
    alt,
    caption
  }: { src: string; poster?: string; alt: string; caption: string } = $props();

  let active = $state(false);
  let ready = $state(false);

  async function activate() {
    active = true;
    await import('@google/model-viewer');
    ready = true;
  }
</script>

<figure class="artifact-viewer">
  <div class="viewer-stage">
    {#if active && ready}
      <svelte:element
        this={'model-viewer'}
        {src}
        poster={poster || undefined}
        {alt}
        camera-controls=""
        auto-rotate=""
        shadow-intensity="1"
        exposure="1.05"
        interaction-prompt="auto"
      ></svelte:element>
    {:else}
      <button class="viewer-poster" onclick={activate} aria-label={`Load interactive 3D model: ${alt}`}>
        {#if poster}<img src={poster} alt="" />{:else}<div class="model-placeholder">3D</div>{/if}
        <span>{active ? 'Loading model…' : 'Load interactive 3D model'}</span>
      </button>
    {/if}
  </div>
  <figcaption>
    <span>3D artifact / drag to orbit</span>
    {caption}
  </figcaption>
</figure>

<style>
  .artifact-viewer {
    margin: 0;
  }

  .viewer-stage {
    position: relative;
    min-height: 520px;
    overflow: hidden;
    border: 1px solid var(--ink);
    background:
      linear-gradient(rgba(48, 79, 211, 0.12) 1px, transparent 1px),
      linear-gradient(90deg, rgba(48, 79, 211, 0.12) 1px, transparent 1px),
      #e5e9ef;
    background-size: 28px 28px;
  }

  :global(model-viewer) {
    width: 100%;
    height: 520px;
    --poster-color: transparent;
    --progress-bar-color: var(--orange);
  }

  .viewer-poster {
    position: absolute;
    inset: 0;
    display: grid;
    width: 100%;
    padding: 0;
    overflow: hidden;
    border: 0;
    color: var(--paper-bright);
    background: var(--ink);
    cursor: pointer;
  }

  .viewer-poster img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.62) saturate(0.75);
    transition: transform 300ms ease, filter 300ms ease;
  }

  .model-placeholder {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    color: rgba(255, 255, 255, 0.15);
    background:
      linear-gradient(rgba(232, 255, 98, 0.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232, 255, 98, 0.08) 1px, transparent 1px),
      var(--ink);
    background-size: 24px 24px;
    font-family: 'Recursive Variable', monospace;
    font-size: 120px;
    font-weight: 900;
  }

  .viewer-poster:hover img {
    filter: brightness(0.72) saturate(0.9);
    transform: scale(1.02);
  }

  .viewer-poster span {
    position: absolute;
    top: 50%;
    left: 50%;
    padding: 14px 18px;
    border: 1px solid var(--paper-bright);
    background: rgba(21, 27, 42, 0.84);
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
    padding: 12px 0 0;
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
    .viewer-stage,
    :global(model-viewer) {
      min-height: 390px;
      height: 390px;
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
