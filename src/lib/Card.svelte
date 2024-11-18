<script>
  let showBack = $state(false);
  let { title, backgroundImage } = $props();

  function flipCard() {
    showBack = !showBack;
  }
</script>

<div class="card-container" onclick={flipCard}>
  <div class="card" class:show-back={showBack}>
    <div
      class="card-background"
      style="background-image: url({backgroundImage})"
    ></div>
    <div class="card-front">
      <h5>{title}</h5>
      <slot name="front"></slot>
    </div>
    <div class="card-back">
      <slot name="back"></slot>
    </div>
  </div>
</div>

<style>
  .card-container {
    display: flex;
    margin: 2em;

    perspective: 100vw;
  }

  .card-background {
    content: '';
    border: 1px solid grey;
    background-color: white;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    opacity: 0.2;

    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    z-index: -1;

    border-radius: 1em;
  }

  /* Add the sync icon in the top right */
  .card::before {
    content: '\f2f1'; /* sync-alt */
    font-family: 'Font Awesome 5 Free';
    font-weight: 900;

    position: absolute;
    right: 1em;
    top: 0.8em;
    opacity: 0.3;
  }

  .card {
    width: 100%;
    height: 300px;

    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;

    transition: transform 1s;
    transform-style: preserve-3d;
    will-change: transform;

    position: relative;
  }

  .card.show-back {
    transform: rotateY(180deg);
  }

  .card-front,
  .card-back {
    padding: 2em;

    position: absolute;
    backface-visibility: hidden;
  }

  .card-front {
    /* For firefox 31 */
    transform: rotateY(0deg);
  }

  .card-back {
    transform: rotateY(180deg);
  }
</style>
