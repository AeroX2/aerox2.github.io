<script lang="ts">
  import { sourceReality } from './stores';

  function toggle() {
    sourceReality.update((v) => !v);
  }

  // Update body class whenever store changes
  $effect(() => {
    if (typeof document !== 'undefined') {
      if ($sourceReality) {
        document.body.classList.add('source-mode');
        document.body.classList.remove('normal-mode');
      } else {
        document.body.classList.add('normal-mode');
        document.body.classList.remove('source-mode');
      }
    }
  });
</script>

<div class="switch-container">
  <span class="label">{$sourceReality ? 'SOURCE' : 'NORMAL'}</span>
  <button
    class="reality-toggle"
    class:active={$sourceReality}
    onclick={toggle}
    aria-label="Toggle Source Reality"
  >
    <div class="glitch-layer"></div>
    <div class="toggle-handle">
      <div class="core"></div>
    </div>
    <div class="status-indicators">
      <div class="dot normal"></div>
      <div class="dot source"></div>
    </div>
  </button>
</div>

<style>
  .switch-container {
    position: fixed;
    top: 2rem;
    right: 7rem;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
    z-index: 1001;
  }

  .label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent-primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.7;
    text-shadow: 0 0 5px var(--accent-primary);
  }

  .reality-toggle {
    position: relative;
    width: 4.5rem;
    height: 2.2rem;
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    border-radius: 100px;
    cursor: pointer;
    padding: 0;
    transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
  }

  .reality-toggle:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
  }

  .toggle-handle {
    position: absolute;
    top: 50%;
    left: 0.3rem;
    transform: translateY(-50%);
    width: 1.6rem;
    height: 1.6rem;
    background: var(--text-secondary);
    border-radius: 50%;
    transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
  }

  .active .toggle-handle {
    left: calc(100% - 1.9rem);
    background: var(--accent-primary);
    box-shadow: 0 0 15px var(--accent-primary);
  }

  .core {
    width: 0.5rem;
    height: 0.5rem;
    background: var(--bg-color);
    border-radius: 50%;
  }

  .status-indicators {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.8rem;
    pointer-events: none;
  }

  .dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--text-secondary);
    opacity: 0.3;
  }

  .active .dot.source {
    background: var(--accent-primary);
    opacity: 1;
    box-shadow: 0 0 5px var(--accent-primary);
  }

  .reality-toggle:not(.active) .dot.normal {
    background: var(--accent-secondary);
    opacity: 1;
    box-shadow: 0 0 5px var(--accent-secondary);
  }

  /* Glitch effect layer */
  .glitch-layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--accent-primary);
    opacity: 0;
    pointer-events: none;
  }

  @media (max-width: 600px) {
    .switch-container {
      top: 1rem;
      right: 5rem;
    }
    .reality-toggle {
      width: 3.5rem;
      height: 1.8rem;
    }
    .toggle-handle {
      width: 1.3rem;
      height: 1.3rem;
    }
    .active .toggle-handle {
      left: calc(100% - 1.6rem);
    }
  }
</style>
