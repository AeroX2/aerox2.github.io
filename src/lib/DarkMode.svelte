<script lang="ts">
  let darkMode = $state(
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  function toggleMode() {
    if (darkMode) {
      darkMode = false;
      window.document.body.classList.remove('dark-mode');
      window.document.body.classList.add('light-mode');
    } else {
      darkMode = true;
      window.document.body.classList.add('dark-mode');
      window.document.body.classList.remove('light-mode');
    }
  }
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
    top: 1em;
    right: 1em;

    width: 3em;
    height: 3em;
    padding: 0.5rem;
    line-height: initial;

    background-color: #606c76;
    color: white;
    border: none;
  }
</style>
