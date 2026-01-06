<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { WebGL } from './webgl';
  import jamesRideyTexture from '../assets/jamesridey.png';

  let { glSupported = $bindable() } = $props();

  let webgl: WebGL;
  let canvas: HTMLCanvasElement;

  let observer: IntersectionObserver;
  let isVisible = true;
  let stop = false;
  let isDragging = false;
  let mousePos = { x: 0, y: 0 };
  let lastMousePos = { x: 0, y: 0 };

  onMount(async () => {
    if (canvas == null) return;

    webgl = new WebGL(canvas);
    glSupported = webgl.isSupported();
    if (!glSupported) return;

    function loop() {
      if (stop || !isVisible) return;
      webgl.setMousePos(mousePos);
      webgl.loop();
      requestAnimationFrame(loop);
    }

    observer = new IntersectionObserver((entries) => {
      const wasVisible = isVisible;
      isVisible = entries[0].isIntersecting;
      if (isVisible && !wasVisible) {
        requestAnimationFrame(loop);
      }
    });
    observer.observe(canvas);

    canvas.addEventListener('pointerdown', (event) => {
      isDragging = true;
      lastMousePos = { x: event.clientX, y: event.clientY };
    });

    canvas.addEventListener('pointermove', (event) => {
      if (isDragging) {
        const rect = canvas.getBoundingClientRect();
        const deltaX = event.clientX - lastMousePos.x;
        const deltaY = event.clientY - lastMousePos.y;

        mousePos.x += (deltaX / rect.width) * 2.0;
        mousePos.y -= (deltaY / rect.height) * 2.0;

        lastMousePos = { x: event.clientX, y: event.clientY };
      }
    });

    canvas.addEventListener('pointerup', () => {
      isDragging = false;
    });

    window.addEventListener('resize', () => webgl.resetViewport());
    webgl.resetViewport();

    const img = new Image();
    img.src = jamesRideyTexture;
    webgl.loadFontTexture(img);

    webgl.init();
    loop();
  });

  onDestroy(async () => {
    stop = true;
    if (observer) observer.disconnect();
  });
</script>

<canvas bind:this={canvas}>Loading...</canvas>

<style>
  canvas {
    touch-action: none;
    width: 100%;

    border-radius: 1em;
    overflow: hidden;
  }
</style>
