<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { SvelteSet } from 'svelte/reactivity';

  // Configuration constants - adjust these to tune the animation speed
  const BASE_INTERVAL_MS = 30; // Base speed for animation ticks
  const CHARS_PER_TICK_RATIO = 50; // Higher = slower reveal (text.length / this value)

  export let speed: number = BASE_INTERVAL_MS;
  export let revealOnInView: boolean = true;

  let displayText = '';
  let interval: ReturnType<typeof setInterval> | undefined;
  let element: HTMLElement;
  let observer: IntersectionObserver;
  let hasRevealed = false;
  let revealedIndices = new SvelteSet<number>();
  let originalText = '';
  let prefersReducedMotion = false;

  // Extended character set for scrambling
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';

  function getRandomChar(): string {
    return characters[Math.floor(Math.random() * characters.length)];
  }

  function startReveal() {
    if (hasRevealed) return;
    hasRevealed = true;

    // If user prefers reduced motion, just show the text immediately
    if (prefersReducedMotion) {
      displayText = originalText;
      return;
    }

    revealedIndices.clear();
    clearInterval(interval);

    // Get all non-space character indices
    const nonSpaceIndices: number[] = [];
    for (let i = 0; i < originalText.length; i++) {
      if (originalText[i] !== ' ') {
        nonSpaceIndices.push(i);
      }
    }

    // Shuffle the indices to reveal in random order
    const shuffledIndices = [...nonSpaceIndices].sort(
      () => Math.random() - 0.5
    );
    let revealIndex = 0;

    // Adjust speed based on text length - longer text reveals faster
    const textLength = nonSpaceIndices.length;
    const adjustedSpeed =
      textLength > 100 ? speed * 0.7 : textLength < 20 ? speed * 1.5 : speed;

    interval = setInterval(() => {
      // Reveal characters - more chars per tick for longer text
      const charsToReveal = Math.max(
        1,
        Math.ceil(shuffledIndices.length / CHARS_PER_TICK_RATIO)
      );
      for (
        let i = 0;
        i < charsToReveal && revealIndex < shuffledIndices.length;
        i++
      ) {
        revealedIndices.add(shuffledIndices[revealIndex]);
        revealIndex++;
      }

      // Build display text
      displayText = originalText
        .split('')
        .map((char, index) => {
          if (char === ' ') return ' ';
          if (revealedIndices.has(index)) return char;
          return getRandomChar();
        })
        .join('');

      if (revealIndex >= shuffledIndices.length) {
        clearInterval(interval);
        displayText = originalText;
      }
    }, adjustedSpeed);
  }

  function startIdle() {
    // If user prefers reduced motion, just show the text
    if (prefersReducedMotion) {
      displayText = originalText;
      return;
    }

    // Show scrambled text initially
    displayText = originalText
      .split('')
      .map((char) => {
        if (char === ' ') return ' ';
        return getRandomChar();
      })
      .join('');
  }

  onMount(() => {
    // Check for reduced motion preference
    if (typeof window !== 'undefined') {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
      prefersReducedMotion = mediaQuery.matches;

      // Listen for changes to the preference
      mediaQuery.addEventListener('change', (e) => {
        prefersReducedMotion = e.matches;
        if (prefersReducedMotion && !hasRevealed) {
          displayText = originalText;
        }
      });
    }

    // Extract text content from the element
    if (element) {
      originalText = element.textContent || '';

      if (revealOnInView) {
        startIdle();
        observer = new IntersectionObserver(
          (entries) => {
            if (entries[0].isIntersecting) {
              startReveal();
            }
          },
          { threshold: 0.1 }
        );
        observer.observe(element);
      } else {
        displayText = originalText;
      }
    }
  });

  onDestroy(() => {
    clearInterval(interval);
    if (observer) observer.disconnect();
  });
</script>

<span
  bind:this={element}
  class="text-scramble"
  class:revealed={hasRevealed}
  class:no-motion={prefersReducedMotion}
  role="presentation"
>
  {#if displayText}
    {displayText}
  {:else}
    <slot />
  {/if}
</span>

<style>
  .text-scramble {
    font-family: 'Space Mono', 'Courier New', monospace;
    transition: color 0.3s ease;
    display: inline-block;
    color: var(--accent-primary);
    opacity: 0.8;
    filter: blur(0.5px);
  }

  .text-scramble.revealed,
  .text-scramble.no-motion {
    color: inherit;
    opacity: 1;
    filter: none;
    transition: all 0.5s ease;
  }

  /* Respect reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    .text-scramble {
      color: inherit;
      opacity: 1;
      filter: none;
    }
  }
</style>
