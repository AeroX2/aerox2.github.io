<script lang="ts">
  import Introduction from './Introduction.svelte';
  import AboutMe from './AboutMe.svelte';
  import Buzzwords from './Buzzwords.svelte';
  import Competitions from './Competitions.svelte';
  import Experience from './Experience.svelte';
  import DarkMode from './lib/DarkMode.svelte';
</script>

<main>
  <Introduction />
  <AboutMe />
  <Experience />
  <Competitions />
  <Buzzwords />
  <DarkMode/>
</main>

<style>
  :global(body.light-mode) {
    color: #213547;
    background-color: #f5f8fa;
  }

  :global(body.dark-mode) {
    color: #c8dced;
    background-color: #1c252b;
  }

  :global(body) {
    color: #213547;
    background-color: #f5f8fa;
  }
  @media (prefers-color-scheme: dark) {
    :global(body) {
      color: #c8dced;
      background-color: #1c252b;
    }
  }
</style>
