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
<div class="intro-content">
  <h1>James Ridey</h1>

  <div class="role-container">
    <span>I am a</span>
    <ul class="role-list">
      <li>Software Engineer</li>
      <li>Programmer</li>
      <li>Tinkerer</li>
      <li>Hacker</li>
      <li>Maker</li>
      <li>Coder</li>
    </ul>
  </div>
</div>
<div class="glass-card tech-stack-card">
  <p class="intro-punchline">
    In other words, I build things—this website included. It is powered by:
  </p>
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
        <img class="dev-icon theme-icon" src={github} alt="Github logo" />
        <div>Github</div>
      </div>
    </div>
  </div>
</div>

<style>
  .intro-content {
    margin-top: 4rem;
    margin-bottom: 2rem;
  }

  .role-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 1.2rem;
    color: var(--text-secondary);
    padding: 0 1rem;
  }

  .role-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
    color: var(--text-primary);
    font-weight: 600;
  }

  .role-list li:not(:last-child)::after {
    content: '•';
    margin-left: 0.5rem;
    color: var(--glass-border);
  }

  @media (max-width: 600px) {
    .role-list li:not(:last-child)::after {
      display: none;
    }
    .role-list li {
      background: var(--glass-bg);
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      font-size: 0.9rem;
    }
  }

  .tech-stack-card {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .intro-punchline {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin: 0;
  }

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
    margin: 1.5em auto 3rem auto;
    position: relative;
    width: 10em;
    height: 10em;
  }

  @media (max-width: 600px) {
    .pentagon-container {
      width: 7em;
      height: 7em;
      font-size: 0.9rem;
      margin-bottom: 2rem;
    }
  }

  .pentagon-item {
    position: absolute;
    height: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
  }

  .pentagon-item div {
    font-size: 0.7em;
    font-weight: 600;
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
