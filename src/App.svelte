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

  <div class="glass-card">
    <AboutMe />
  </div>

  <div class="glass-card">
    <Experience />
  </div>

  <div class="glass-card">
    <Competitions />
  </div>

  <div class="glass-card">
    <Buzzwords />
  </div>

  <DarkMode />
</main>

<style>
  /* Local adjustments if needed */
  main {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
</style>
