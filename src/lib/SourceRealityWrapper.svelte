<script lang="ts">
  import { sourceReality } from './stores';
  import CodeViewer from './CodeViewer.svelte';
  import { fade } from 'svelte/transition';

  let { children, code = '', filename = '' } = $props();
</script>

<div class="reality-wrapper">
  {#if $sourceReality}
    <div class="source-side" in:fade={{ duration: 150 }}>
      <CodeViewer {code} {filename} />
    </div>
  {:else}
    <div class="content-side" in:fade={{ duration: 150 }}>
      {@render children()}
    </div>
  {/if}
</div>

<style>
  .reality-wrapper {
    width: 100%;
    min-height: 200px;
    display: grid;
    grid-template-areas: 'overlap';
  }

  .content-side,
  .source-side {
    grid-area: overlap;
    width: 100%;
  }
</style>
