<script lang="ts">
  import { onMount } from 'svelte';

  type ImageSource = { src: string; alt?: string };

  let {
    images,
    alt = '',
    position = '50% 50%',
    variant = 'card'
  }: { images: ImageSource[]; alt?: string; position?: string; variant?: string } = $props();

  let active = $state(0);
  let previous = $state<number | null>(null);
  let rotatorElement = $state<HTMLElement>();

  const previewPattern = /^\/(projects|labeled-media)\/(.+)\.(?:jpe?g|png|webp)$/i;
  const motionAllowed = () => !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function previewSources(source: string) {
    const match = source.match(previewPattern);
    if (!match) return undefined;
    const path = `${match[1]}/${match[2]}`;
    return `/card-media/${path}-640.webp 640w, /card-media/${path}-1200.webp 1200w`;
  }

  function preload(index: number) {
    const source = images[index]?.src;
    if (!source) return;
    const image = new Image();
    const sources = previewSources(source);
    if (sources) {
      image.srcset = sources;
      image.sizes = '(max-width: 650px) 100vw, (max-width: 1050px) 50vw, 700px';
    }
    image.src = source;
  }

  onMount(() => {
    if (images.length < 2 || !motionAllowed()) return;

    const seed = images[0].src.split('').reduce((total, character) => total + character.charCodeAt(0), 0);
    const initialDelay = 1800 + (seed % 13_000);
    const interval = 10_000 + (seed % 5_000);
    let timeout: number | undefined;
    let visible = false;
    let paused = false;

    const clearTimer = () => {
      if (timeout) window.clearTimeout(timeout);
      timeout = undefined;
    };
    const advance = () => {
      previous = active;
      active = (active + 1) % images.length;
      preload((active + 1) % images.length);
      window.setTimeout(() => (previous = null), 360);
    };
    const schedule = (delay: number) => {
      clearTimer();
      if (!visible || paused) return;
      preload((active + 1) % images.length);
      timeout = window.setTimeout(() => {
        advance();
        schedule(interval);
      }, delay);
    };
    const observer = new IntersectionObserver(
      ([entry]) => {
        visible = entry.isIntersecting;
        if (visible) schedule(initialDelay);
        else clearTimer();
      },
      { rootMargin: '180px 0px' }
    );

    if (rotatorElement) observer.observe(rotatorElement);
    const pause = () => {
      paused = true;
      clearTimer();
    };
    const resume = () => {
      paused = false;
      schedule(interval);
    };
    rotatorElement?.addEventListener('mouseenter', pause);
    rotatorElement?.addEventListener('mouseleave', resume);
    return () => {
      clearTimer();
      observer.disconnect();
      rotatorElement?.removeEventListener('mouseenter', pause);
      rotatorElement?.removeEventListener('mouseleave', resume);
    };
  });
</script>

<span class={`project-image-rotator ${variant}`} bind:this={rotatorElement}>
  {#if previous !== null}
    {@const previousImage = images[previous]}
    <img
      class="outgoing"
      src={previousImage.src}
      srcset={previewSources(previousImage.src)}
      sizes="(max-width: 650px) 100vw, (max-width: 1050px) 50vw, 700px"
      alt=""
      aria-hidden="true"
      decoding="async"
      style:object-position={position}
    />
  {/if}
  {#if images[active]}
    {@const activeImage = images[active]}
    <img
      class="active"
      src={activeImage.src}
      srcset={previewSources(activeImage.src)}
      sizes="(max-width: 650px) 100vw, (max-width: 1050px) 50vw, 700px"
      alt={activeImage.alt || alt}
      loading={variant === 'featured' ? 'eager' : 'lazy'}
      decoding="async"
      style:object-position={position}
    />
  {/if}
</span>
