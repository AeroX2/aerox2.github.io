<script lang="ts">
  import { onMount } from 'svelte';

  export let text: string = '';

  let displayText = text;
  let isHovered = false;
  let interval: any;

  const characters = '0123456789ABCDEF';

  function toHex(str: string) {
    return str
      .split('')
      .map((char) =>
        char.charCodeAt(0).toString(16).toUpperCase().padStart(2, '0')
      )
      .join(' ');
  }

  function startGlitch() {
    isHovered = true;
    let iteration = 0;
    const hexTarget = toHex(text);

    clearInterval(interval);

    interval = setInterval(() => {
      displayText = text
        .split('')
        .map((char, index) => {
          if (index < iteration) {
            return char.charCodeAt(0).toString(16).toUpperCase();
          }
          return characters[Math.floor(Math.random() * 16)];
        })
        .join('');

      if (iteration >= text.length) {
        clearInterval(interval);
        // Pause briefly at hex before returning?
        // Or just stay at hex while hovered.
        displayText = hexTarget;
      }

      iteration += 1 / 3;
    }, 30);
  }

  function stopGlitch() {
    isHovered = false;
    clearInterval(interval);
    displayText = text;
  }
</script>

<span
  class="hex-glitch"
  on:mouseenter={startGlitch}
  on:mouseleave={stopGlitch}
  role="presentation"
>
  {displayText}
</span>

<style>
  .hex-glitch {
    font-family: 'Space Mono', 'Courier New', monospace;
    transition: color 0.3s ease;
    cursor: crosshair;
    display: inline-block;
  }

  .hex-glitch:hover {
    color: var(--accent-primary);
    text-shadow: 0 0 8px rgba(0, 242, 255, 0.5);
  }
</style>
