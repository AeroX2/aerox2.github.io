<script lang="ts">
  let isActive = $state(false);
  let { title, backgroundImage, front, back } = $props();

  function toggleOverlay() {
    isActive = !isActive;
  }
</script>

<div
  class="card-container"
  class:active={isActive}
  onpointerenter={(e) => {
    if (e.pointerType === 'mouse') isActive = true;
  }}
  onmouseleave={() => (isActive = false)}
  onclick={toggleOverlay}
  role="button"
  tabindex="0"
  onkeydown={(e) => e.key === 'Enter' && toggleOverlay()}
>
  <!-- Background Image with Dark Overlay -->
  <div
    class="card-image-bg"
    style="background-image: url({backgroundImage})"
  ></div>

  <!-- Primary Content (Always Visible) -->
  <div class="card-main">
    <h5>{title}</h5>
    <div class="main-content">
      {@render front()}
    </div>
  </div>

  <!-- Sliding Overlay (Revealed on Hover/Tap) -->
  <div class="card-overlay">
    <div class="drag-handle"></div>
    <div class="overlay-content">
      {@render back()}
    </div>
  </div>

  <!-- Interactive Indicator -->
  <div class="info-badge">
    <i class="fa fa-circle-info"></i>
  </div>
</div>

<style>
  .card-container {
    position: relative;
    width: 100%;
    min-height: 320px;
    height: 100%;
    margin: 0;
    border-radius: 20px;
    background: var(--bg-color);
    border: 1px solid var(--glass-border);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--glass-shadow);
    display: flex;
    flex-direction: column;
  }

  @media (max-width: 600px) {
    .card-container {
      min-height: 250px;
    }
  }

  /* Active states (for both hover and tap) */
  .active {
    border-color: var(--accent-primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(0, 242, 255, 0.15);
  }
  .active .card-image-bg {
    transform: scale(1.05);
    opacity: 0.15;
  }
  .active .info-badge {
    opacity: 1;
    animation: pulse 2s infinite;
  }
  .active .card-overlay {
    transform: translateY(0);
  }

  /* Background Handling */
  .card-image-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    opacity: 0.25;
    transition:
      transform 0.6s ease,
      opacity 0.4s ease;
    z-index: 0;
  }

  /* Main Static Content */
  .card-main {
    position: relative;
    z-index: 1;
    flex: 1;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .card-main h5 {
    color: var(--accent-primary);
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    width: 100%;
    word-break: break-word;
  }

  .main-content {
    width: 100%;
  }

  /* Sliding Overlay */
  .card-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--glass-bg);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border-top: 1px solid var(--accent-primary);
    padding: 2.5rem;
    z-index: 2;
    transform: translateY(105%);
    transition: transform 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .active .card-overlay {
    transform: translateY(0);
  }

  .drag-handle {
    position: absolute;
    top: 12px;
    width: 40px;
    height: 4px;
    background: var(--accent-primary);
    border-radius: 2px;
    opacity: 0.5;
  }

  .overlay-content {
    width: 100%;
    color: var(--text-primary);
    font-size: 1.15rem;
    line-height: 1.7;
    white-space: normal;
  }

  /* Info Badge Info Animation */
  .info-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    color: var(--accent-primary);
    opacity: 0.6;
    z-index: 1;
    transition: opacity 0.3s ease;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.2);
      opacity: 0.7;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* Accessibility: Disable animations for reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .card-container {
      transition: none;
    }

    .active {
      transform: none;
    }

    .card-image-bg {
      transition: none;
    }

    .active .card-image-bg {
      transform: none;
    }

    .active .info-badge {
      animation: none;
    }

    .card-overlay {
      transition: none;
    }
  }
</style>
