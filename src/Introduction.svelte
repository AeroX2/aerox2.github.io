<script lang="ts">
  import vite from '../node_modules/devicon/icons/vitejs/vitejs-original.svg';
  import bun from '../node_modules/devicon/icons/bun/bun-original.svg';
  import svelte from '../node_modules/devicon/icons/svelte/svelte-original.svg';
  import github from '../node_modules/devicon/icons/github/github-original.svg';
  import typescript from '../node_modules/devicon/icons/typescript/typescript-original.svg';
  import { onMount } from 'svelte';
  import { sourceReality } from './lib/stores';
  let { glSupported = $bindable(true) } = $props();
  let isSourceActive = $state(false);

  sourceReality.subscribe((val) => (isSourceActive = val));

  // Typewriter effect
  const roles = [
    'Software Engineer',
    'Programmer',
    'Tinkerer',
    'Hacker',
    'Maker',
    'Coder',
    'Security Enthusiast'
  ];
  let currentRoleIndex = $state(0);
  let displayText = $state('');
  let isDeleting = $state(false);
  let isWaiting = $state(false);
  let typingSpeed = $state(150);

  let observer: IntersectionObserver;
  let isVisible = true;
  let container: HTMLElement;

  function tick() {
    if (!isVisible || isSourceActive) {
      setTimeout(tick, 1000);
      return;
    }
    const fullText = roles[currentRoleIndex];
    isWaiting = false;

    if (isDeleting) {
      displayText = fullText.substring(0, displayText.length - 1);
      typingSpeed = 50;
    } else {
      displayText = fullText.substring(0, displayText.length + 1);
      typingSpeed = 150;
    }

    if (!isDeleting && displayText === fullText) {
      isDeleting = true;
      typingSpeed = 2000;
      isWaiting = true;
    } else if (isDeleting && displayText === '') {
      isDeleting = false;
      currentRoleIndex = (currentRoleIndex + 1) % roles.length;
      typingSpeed = 500;
      isWaiting = true;
    }

    setTimeout(tick, typingSpeed);
  }

  onMount(() => {
    observer = new IntersectionObserver((entries) => {
      isVisible = entries[0].isIntersecting;
    });
    if (container) observer.observe(container);

    tick();

    return () => {
      if (observer) observer.disconnect();
    };
  });
</script>

<div class="intro-content" bind:this={container}>
  <div class="name-header">
    <h4 class="intro-label">Hi, I'm</h4>
    <h1 class="main-name">James Ridey</h1>
  </div>

  <div class="role-container">
    <span>I am a</span>
    <span class="typewriter-text">
      {displayText}<span class="cursor" class:blinking={isWaiting}></span>
    </span>
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
    margin-top: 3rem;
    margin-bottom: 3rem;
    text-align: center;
  }

  .name-header {
    margin-bottom: 2rem;
    animation: fadeInUp 0.8s ease-out forwards;
  }

  .intro-label {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.3em;
    color: var(--accent-primary);
    margin-bottom: 0.5rem;
    opacity: 0.8;
  }

  .main-name {
    font-size: 5rem;
    margin: 0;
    line-height: 1;
    background: linear-gradient(
      135deg,
      #fff 0%,
      var(--accent-primary) 50%,
      var(--accent-secondary) 100%
    );
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 20px rgba(0, 242, 255, 0.2));
    letter-spacing: -0.04em;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 600px) {
    .main-name {
      font-size: 3.5rem;
    }
    .intro-label {
      font-size: 0.8rem;
    }
  }

  .role-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.5rem;
    color: var(--text-secondary);
    min-height: 2.5rem;
  }

  .typewriter-text {
    color: var(--text-primary);
    font-weight: 600;
  }

  .cursor {
    display: inline-block;
    width: 2px;
    height: 1.2em;
    background-color: var(--accent-primary, #0070f3);
    margin-left: 2px;
    vertical-align: middle;
  }

  .cursor.blinking {
    animation: blink 1s step-end infinite;
  }

  @keyframes blink {
    from,
    to {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
  }

  @media (max-width: 600px) {
    .role-container {
      font-size: 1.2rem;
    }
  }

  .tech-stack-card {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    overflow: hidden;
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

  .pentagon-container {
    margin: 3rem auto 4rem auto;
    position: relative;
    width: 12em;
    height: 12em;
    animation: rotate-pentagon 20s linear infinite;
    will-change: transform;
  }

  @keyframes rotate-pentagon {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @media (max-width: 600px) {
    .pentagon-container {
      width: 9em;
      height: 9em;
      font-size: 0.9rem;
      margin-bottom: 2rem;
    }
  }

  .pentagon-item {
    position: absolute;
    height: 3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    animation: counter-rotate-item 20s linear infinite;
    will-change: transform;
  }

  @keyframes counter-rotate-item {
    from {
      transform: translateX(-50%) translateY(-50%) rotate(0deg);
    }
    to {
      transform: translateX(-50%) translateY(-50%) rotate(-360deg);
    }
  }

  .pentagon-item div {
    font-size: 0.8em;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .dev-icon {
    width: 2.5em;
    height: 2.5em;
    max-width: unset;
    filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.3));
  }

  .pentagon-item:nth-child(1) {
    top: 0%;
    left: 50%;
  }

  .pentagon-item:nth-child(2) {
    top: 38%;
    left: 100%;
  }

  .pentagon-item:nth-child(3) {
    top: 100%;
    left: 81%;
  }

  .pentagon-item:nth-child(4) {
    top: 100%;
    left: 19%;
  }

  .pentagon-item:nth-child(5) {
    top: 38%;
    left: 0%;
  }

  /* Accessibility: Disable animations for reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .name-header {
      animation: none;
    }

    .pentagon-container {
      animation: none;
    }

    .pentagon-item {
      animation: none;
    }

    .cursor.blinking {
      animation: none;
      opacity: 1;
    }
  }
</style>
