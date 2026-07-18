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

  onMount(() => {
    if (images.length < 2 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const offset = images[0].src.split('').reduce((total, character) => total + character.charCodeAt(0), 0) % 3200;
    let interval: number | undefined;
    const timeout = window.setTimeout(() => {
      active = (active + 1) % images.length;
      interval = window.setInterval(() => { active = (active + 1) % images.length; }, 7200);
    }, 3200 + offset);
    return () => {
      window.clearTimeout(timeout);
      if (interval) window.clearInterval(interval);
    };
  });
</script>

<span class={`project-image-rotator ${variant}`}>
  {#each images as image, index (image.src)}
    <img
      class:active={index === active}
      src={image.src}
      alt={index === active ? (image.alt || alt) : ''}
      aria-hidden={index !== active}
      loading={index === 0 ? 'eager' : 'lazy'}
      style:object-position={position}
    />
  {/each}
</span>
