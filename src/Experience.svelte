<script lang="ts">
  import google from './assets/google.svg';
  import canva from './assets/canva.svg';
  import first from './assets/first.png';
  import thoughdesign from './assets/thoughtdesign.png';

  let timeline: HTMLDivElement;

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function scrollLeft() {
    timeline.scroll({
      left: timeline.scrollLeft - timeline.clientWidth,
      behavior: prefersReducedMotion() ? 'instant' : 'smooth'
    });
  }

  function scrollRight() {
    timeline.scroll({
      left: timeline.scrollLeft + timeline.clientWidth,
      behavior: prefersReducedMotion() ? 'instant' : 'smooth'
    });
  }
</script>

<h3>Experience:</h3>
<div class="timeline">
  <button
    class="timeline-button left"
    onclick={scrollLeft}
    aria-label="Scroll content left"
  >
    <i class="fa fa-xl fa-arrow-left"></i>
  </button>
  <button
    class="timeline-button right"
    onclick={scrollRight}
    aria-label="Scroll content right"
  >
    <i class="fa fa-xl fa-arrow-right"></i>
  </button>
  <div class="timeline-cards" bind:this={timeline}>
    <div class="timeline-card">
      <div class="date">2020-2025</div>
      <img src={canva} alt="Canva logo" />
      <p>
        At Canva, I built several AI features. I led the Magic Design project,
        which integrated Generative AI into the core platform and launched for
        Droptober. I also ran the Team Brain initiative, delivering an
        AI-powered search prototype for internal knowledge retrieval.
        Separately, I worked on the Forms, Polls, and Quizzes overhaul, which
        involved refactoring legacy code to reduce technical debt. I mentored
        junior engineers and helped with team knowledge sharing.
      </p>
    </div>
    <div class="timeline-card">
      <div class="date">2017-2018</div>
      <img src={google} alt="Google logo" />
      <p>
        I completed two internships at Google in 2017 and 2018. In 2017, I built
        a new internal tool for Google Maps to help streamline their workflow.
        In 2018, I joined the Neighbourly team to port their web application to
        the Jiophone. This required reverse-engineering the existing system with
        minimal documentation to deliver a fully functional app and creating
        comprehensive documentation for the team.
      </p>
    </div>

    <div class="timeline-card">
      <div class="date">2014-2020</div>
      <img src={thoughdesign} alt="ThoughtDesign logo" style="height: 4em" />
      <p>
        I worked part-time at ThoughtDesign from 2014 to 2020. I developed web
        applications using MVC and ASP.NET and customized JavaScript libraries
        for commercial use. By 2018, I was managing several Angular projects,
        implementing Protractor for end-to-end testing, and establishing a
        TypeScript unit testing framework.
      </p>
    </div>

    <div class="timeline-card">
      <div class="date">2013-2016</div>
      <img src={first} alt="FIRST Robotics logo" />
      <p>
        From 2013 to 2016, I was the lead software developer for a FIRST
        Robotics team. I worked with the team to design, build, and test a 50kg
        robot for international competition. I was responsible for developing
        critical components of the robot control system within a strict six-week
        deadline, ensuring high precision and reliability during competition.
      </p>
    </div>
  </div>
</div>

<style>
  img {
    height: 3em;
    margin-bottom: 0.5em;
  }

  .timeline {
    position: relative;
  }

  .timeline-button {
    width: 3em;
    height: 3em;
    padding: 0;

    border: none;
    background-color: #606c76;
    color: white;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;
    overflow: hidden;

    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }

  .timeline-button.left {
    left: 0;
    transform: translateX(-50%);
  }

  .timeline-button.right {
    right: 0;
    transform: translateX(50%);
  }

  .timeline-cards {
    display: flex;
    align-items: center;

    overflow-x: auto;
    scroll-snap-type: x mandatory;
  }

  .timeline-cards::-webkit-scrollbar {
    display: none;
  }

  .timeline-card {
    flex: 0 0 100%;
    padding: 0 1.5em;
    scroll-snap-align: center;
  }
</style>
