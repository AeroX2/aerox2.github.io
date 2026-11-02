<script lang="ts">
  import { onMount } from 'svelte';
  import { previewSrcset } from './data/pages';
  import { onRotationTick } from './lib/rotationClock';

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

  const variantSizes: Record<string, string> = {
    featured: '(max-width: 1050px) 100vw, 66vw',
    supporting: '(max-width: 650px) 130px, (max-width: 1050px) 33vw, 17vw',
    machine: '(max-width: 650px) 100vw, (max-width: 1050px) 300px, 420px',
    drawer: '(max-width: 650px) 100vw, 30vw'
  };
  const imageSizes = $derived(variantSizes[variant] ?? '(max-width: 650px) 100vw, 50vw');

  const motionAllowed = () => !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  async function preload(index: number) {
    const source = images[index]?.src;
    if (!source) return false;
    const image = new Image();
    const sources = previewSrcset(source);
    if (sources) {
      image.srcset = sources;
      image.sizes = imageSizes;
    }
    image.src = source;
    try {
      await image.decode();
      return true;
    } catch {
      return false;
    }
  }

  onMount(() => {
    if (images.length < 2 || !motionAllowed()) return;

    let fadeTimeout: number | undefined;
    let visible = false;
    let paused = false;
    let nextReady = false;
    let preparing = false;

    const prepareNext = async () => {
      if (preparing) return;
      preparing = true;
      nextReady = false;
      const next = (active + 1) % images.length;
      const loaded = await preload(next);
      nextReady = loaded && next === (active + 1) % images.length;
      preparing = false;
    };
    const advance = () => {
      if (!visible || paused || !motionAllowed()) return;
      if (!nextReady) {
        prepareNext();
        return;
      }
      window.clearTimeout(fadeTimeout);
      previous = active;
      active = (active + 1) % images.length;
      fadeTimeout = window.setTimeout(() => (previous = null), 950);
      prepareNext();
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        visible = entry.isIntersecting;
        if (visible && !nextReady) prepareNext();
      },
      { rootMargin: '180px 0px' }
    );
    if (rotatorElement) observer.observe(rotatorElement);

    const pause = () => (paused = true);
    const resume = () => (paused = false);
    rotatorElement?.addEventListener('mouseenter', pause);
    rotatorElement?.addEventListener('mouseleave', resume);

    const stopTicking = onRotationTick(advance);
    return () => {
      stopTicking();
      window.clearTimeout(fadeTimeout);
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
      srcset={previewSrcset(previousImage.src)}
      sizes={imageSizes}
      alt=""
      aria-hidden="true"
      decoding="async"
      style:object-position={position}
    />
  {/if}
  {#if images[active]}
    {@const activeImage = images[active]}
    {#key active}
    <img
      class="active"
      class:crossfading={previous !== null}
      src={activeImage.src}
      srcset={previewSrcset(activeImage.src)}
      sizes={imageSizes}
      alt={activeImage.alt || alt}
      loading={variant === 'featured' ? 'eager' : 'lazy'}
      fetchpriority={variant === 'featured' && active === 0 ? 'high' : 'auto'}
      decoding="async"
      style:object-position={position}
    />
    {/key}
  {/if}
</span>
