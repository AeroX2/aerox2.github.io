<script lang="ts">
  import { onMount } from 'svelte';

  let darkMode = $state(
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  function updateBodyClass() {
    if (darkMode) {
      window.document.body.classList.add('dark-mode');
      window.document.body.classList.remove('light-mode');
    } else {
      window.document.body.classList.remove('dark-mode');
      window.document.body.classList.add('light-mode');
    }
  }

  function toggleMode() {
    darkMode = !darkMode;
    updateBodyClass();
  }

  onMount(() => {
    updateBodyClass();
  });
</script>

<button onclick={toggleMode} aria-label="Dark/Light mode switch">
  {#if darkMode}
    <i class="fa fa-xl fa-moon"></i>
  {:else}
    <i class="fa fa-xl fa-sun"></i>
  {/if}
</button>

<style>
  button {
    position: fixed;
    top: 2rem;
    right: 2rem;
    width: 4rem;
    height: 4rem;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    color: var(--accent-primary);
    border-radius: 50%;
    cursor: pointer;
    z-index: 1000;
    transition: all 0.3s ease;
  }

  button:hover {
    background: var(--accent-primary);
    color: var(--bg-color);
    border-color: var(--accent-primary);
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
  }

  @media (max-width: 600px) {
    button {
      top: 1rem;
      right: 1rem;
      width: 3.5rem;
      height: 3.5rem;
    }
  }
</style>
