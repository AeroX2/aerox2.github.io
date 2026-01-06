<script lang="ts">
  import Introduction from './Introduction.svelte';
  import AboutMe from './AboutMe.svelte';
  import Buzzwords from './Buzzwords.svelte';
  import Competitions from './Competitions.svelte';
  import Experience from './Experience.svelte';
  import DarkMode from './lib/DarkMode.svelte';
  import SourceRealitySwitch from './lib/SourceRealitySwitch.svelte';
  import SourceRealityWrapper from './lib/SourceRealityWrapper.svelte';
  import Canvas from './sdf/Canvas.svelte';

  import aboutMeSource from './AboutMe.svelte?raw';
  import experienceSource from './Experience.svelte?raw';
  import competitionsSource from './Competitions.svelte?raw';
  import buzzwordsSource from './Buzzwords.svelte?raw';
  import introSource from './Introduction.svelte?raw';
  import fragmentSource from './sdf/fragment.glsl?raw';

  let glSupported = $state(true);
</script>

<SourceRealitySwitch />
<DarkMode />

<main>
  {#if glSupported}
    <SourceRealityWrapper code={fragmentSource} filename="fragment.glsl">
      <Canvas bind:glSupported />
    </SourceRealityWrapper>
  {/if}

  <SourceRealityWrapper code={introSource} filename="Introduction.svelte">
    <Introduction bind:glSupported />
  </SourceRealityWrapper>

  <div class="glass-card">
    <SourceRealityWrapper code={aboutMeSource} filename="AboutMe.svelte">
      <AboutMe />
    </SourceRealityWrapper>
  </div>

  <div class="glass-card">
    <SourceRealityWrapper code={experienceSource} filename="Experience.svelte">
      <Experience />
    </SourceRealityWrapper>
  </div>

  <div class="glass-card">
    <SourceRealityWrapper
      code={competitionsSource}
      filename="Competitions.svelte"
    >
      <Competitions />
    </SourceRealityWrapper>
  </div>

  <div class="glass-card">
    <SourceRealityWrapper code={buzzwordsSource} filename="Buzzwords.svelte">
      <Buzzwords />
    </SourceRealityWrapper>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
</style>
