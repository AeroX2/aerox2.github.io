<script lang="ts">
  import { onMount } from 'svelte';

  let {
    title,
    src,
    alt,
    onclose
  }: {
    title: string;
    src: string;
    alt: string;
    onclose: () => void;
  } = $props();

  let dialogElement: HTMLDivElement;

  onMount(() => {
    dialogElement.focus();
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      document.body.style.overflow = previousOverflow;
    };
  });
</script>

<svelte:window onkeydown={(event) => event.key === 'Escape' && onclose()} />

<div
  class="certificate-backdrop"
  role="presentation"
  onclick={(event) => event.target === event.currentTarget && onclose()}
>
  <div
    class="certificate-dialog"
    role="dialog"
    aria-modal="true"
    aria-labelledby="certificate-title"
    tabindex="-1"
    bind:this={dialogElement}
  >
    <header>
      <p id="certificate-title">{title}</p>
      <button type="button" onclick={onclose}>Close ×</button>
    </header>
    <img {src} {alt} />
  </div>
</div>

<style>
  .certificate-backdrop {
    position: fixed;
    z-index: 110;
    inset: 0;
    display: grid;
    place-items: center;
    padding: 24px;
    overflow: auto;
    background: rgba(10, 18, 35, 0.78);
    backdrop-filter: blur(9px);
  }

  .certificate-dialog {
    width: min(1180px, 100%);
    padding: 18px;
    color: var(--ink);
    background: var(--paper-bright);
    box-shadow: 16px 16px 0 var(--acid);
  }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--ink);
  }

  header p,
  header button {
    margin: 0;
    font-family: 'Recursive Variable', monospace;
    font-size: 10px;
    font-variation-settings: 'MONO' 1;
    font-weight: 760;
    letter-spacing: .06em;
    text-transform: uppercase;
  }

  header button {
    padding: 7px 9px;
    color: var(--ink);
    background: transparent;
    border: 1px solid var(--ink);
    cursor: pointer;
  }

  header button:hover,
  header button:focus-visible {
    color: var(--paper-bright);
    background: var(--ink);
  }

  img {
    display: block;
    width: 100%;
    max-height: calc(100vh - 160px);
    margin-top: 16px;
    object-fit: contain;
    background: var(--ink);
  }

  @media (max-width: 640px) {
    .certificate-backdrop { padding: 12px; }
    .certificate-dialog { padding: 12px; box-shadow: 8px 8px 0 var(--acid); }
    img { max-height: calc(100vh - 128px); }
  }
</style>
