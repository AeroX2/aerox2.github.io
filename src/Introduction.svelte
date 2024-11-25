<script lang="ts">
  import vite from '../node_modules/devicon/icons/vitejs/vitejs-original.svg';
  import bun from '../node_modules/devicon/icons/bun/bun-original.svg';
  import svelte from '../node_modules/devicon/icons/svelte/svelte-original.svg';
  import github from '../node_modules/devicon/icons/github/github-original.svg';
  import typescript from '../node_modules/devicon/icons/typescript/typescript-original.svg';
  import Canvas from './sdf/Canvas.svelte';

  let sdfEnabled = $state(false);
  let glSupported = $state(true);
</script>

{#if glSupported}
  <Canvas bind:glSupported />
{/if}
  <h1>Hi, I'm James Ridey</h1>

  I'm a<br />
  <ul class="list-no-space">
    <li><b>Software Engineer</b></li>
    <li><b>Programmer</b></li>
    <li><b>Tinkerer</b></li>
    <li><b>Hacker</b></li>
    <li><b>Maker</b></li>
    <li><b>Coder</b></li>
  </ul>
  In other words, I build things, this website included. Crafted using the latest
  frameworks and techniques, it is powered by
  <div class="dev-icons">
    <div class="pentagon-container">
      <div class="pentagon-item">
        <img class="dev-icon" src={vite} alt="Vite logo" />
        <div>Vite</div>
      </div>
      <div class="pentagon-item">
        <img class="dev-icon" src={bun} alt="Bun logo" />
        <div>Bun</div>
      </div>
      <div class="pentagon-item">
        <img class="dev-icon" src={svelte} alt="Svelte logo" />
        <div>Svelte</div>
      </div>
      <div class="pentagon-item">
        <img class="dev-icon" src={typescript} alt="Typescript logo" />
        <div>Typescript</div>
      </div>
      <div class="pentagon-item">
        <img class="dev-icon" src={github} alt="Github logo" />
        <div>Github</div>
      </div>
    </div>
  </div>

<style>
  .dev-icons {
    margin-top: 0.5em;

    display: flex;
    justify-content: center;
    gap: 1em;
  }

  .dev-icon {
    width: 2em;
    height: 2em;
  }

  .pentagon-container {
    margin: 1.5em 2em 3em 2em;
    position: relative;
    width: 10em;
    height: 10em;
  }

  .pentagon-item {
    position: absolute;
    height: 2em;
  }

  .pentagon-item:nth-child(1) {
    top: 0%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
  }

  .pentagon-item:nth-child(2) {
    top: 38%;
    left: 100%;
    transform: translateX(-50%) translateY(-50%);
  }

  .pentagon-item:nth-child(3) {
    top: 100%;
    left: 81%;
    transform: translateX(-50%) translateY(-50%);
  }

  .pentagon-item:nth-child(4) {
    top: 100%;
    left: 19%;
    transform: translateX(-50%) translateY(-50%);
  }

  .pentagon-item:nth-child(5) {
    top: 38%;
    left: 0%;
    transform: translateX(-50%) translateY(-50%);
  }
</style>
