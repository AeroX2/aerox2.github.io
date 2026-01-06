<script lang="ts">
  import Prism from 'prismjs';
  import 'prismjs/themes/prism-tomorrow.css';
  import 'prismjs/components/prism-clike';
  import 'prismjs/components/prism-javascript';
  import 'prismjs/components/prism-typescript';
  import 'prismjs/components/prism-c';
  import 'prismjs/components/prism-glsl';
  import 'prism-svelte';

  let { code = '', filename = 'component.svelte' } = $props();
  let codeElement: HTMLElement;

  let language = $derived(filename.endsWith('.glsl') ? 'glsl' : 'svelte');

  $effect(() => {
    if (code && codeElement) {
      Prism.highlightElement(codeElement);
    }
  });
</script>

<div class="code-window">
  <div class="window-header">
    <div class="dots">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <div class="filename">
      <i class="fa fa-file-code"></i>
      {filename}
    </div>
  </div>
  <div class="code-container">
    <pre class="line-numbers"><code
        bind:this={codeElement}
        class="language-{language}">{code}</code
      ></pre>
  </div>
</div>

<style>
  .code-window {
    background: #1e1e1e;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    border: 1px solid #333;
    font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;
    text-align: left;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .window-header {
    background: #252526;
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border-bottom: 1px solid #333;
  }

  .dots {
    display: flex;
    gap: 0.5rem;
  }

  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }

  .red {
    background: #ff5f56;
  }
  .yellow {
    background: #ffbd2e;
  }
  .green {
    background: #27c93f;
  }

  .filename {
    color: #969696;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .code-container {
    flex: 1;
    overflow: auto;
    padding: 1rem;
    background: #1e1e1e;
  }

  pre {
    margin: 0;
    padding: 0;
    background: transparent !important;
  }

  code {
    font-size: 0.9rem;
    line-height: 1.5;
    background: transparent !important;
  }

  :global(.token.comment) {
    color: #6a9955;
  }
  :global(.token.keyword) {
    color: #569cd6;
  }
  :global(.token.string) {
    color: #ce9178;
  }
  :global(.token.function) {
    color: #dcdcaa;
  }
  :global(.token.operator) {
    color: #d4d4d4;
  }
  :global(.token.punctuation) {
    color: #d4d4d4;
  }
</style>
