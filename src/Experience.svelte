<script lang="ts">
  import './lib/scroll-timeline.js';

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
      <div class="date">2020-Present</div>
      <img src={canva} alt="Canva logo" />
      <p>
        Since joining Canva in 2020, I have contributed significantly to a
        variety of initiatives. I led the Magic Design project, integrating
        AI-created designs into the platform and launching it ahead of schedule
        for Droptober. Additionally, I was responsible for the Team Brain
        initiative, delivering an AI-powered search prototype on a tight
        deadline, which led to an early pivot that saved resources. I also
        spearheaded the Forms, Polls, and Quizzes initiative, enhancing the
        search panel and contributed heavily to refactoring the codebase,
        reducing technical debt, and improving maintainability. Throughout my
        tenure, I mentored junior engineers, improving team productivity and
        driving knowledge-sharing.
      </p>
    </div>
    <div class="timeline-card">
      <div class="date">2017-2018</div>
      <img src={google} alt="Google logo" />
      <p>
        During my internships at Google in 2017 and 2018, I contributed to
        impactful projects. In 2017, I built an internal tool for Google Maps,
        adapting to an unfamiliar framework and launching the tool successfully.
        In 2018, I worked with the Neighbourly team to port their web app to the
        Jiophone. Despite limited documentation, I reverse-engineered the system
        to deliver a functional app and extensive internal documentation.
      </p>
    </div>

    <div class="timeline-card">
      <div class="date">2014-2020</div>
      <img src={thoughdesign} alt="ThoughtDesign logo" style="height: 4em" />
      <p>
        From 2014 to 2020, I worked part-time at ThoughtDesign, where I honed my
        web development skills across multiple projects. My work included
        designing a small website with MVC and ASP.NET, customizing JavaScript
        libraries for commercial use, and leading Angular 2 projects with
        Protractor for end-to-end testing. By 2018, I was managing multiple
        Angular projects and developing robust TypeScript unit testing
        frameworks.
      </p>
    </div>

    <div class="timeline-card">
      <div class="date">2013-2016</div>
      <img src={first} alt="FIRST Robotics logo" />
      <p>
        From 2013 to 2016, I served as the lead software developer for a FIRST
        Robotics team, collaborating with like-minded peers to design, build,
        and test a 50kg robot for international competition. Within a strict
        six-week timeline, I developed critical components of the robot control
        system, enhancing its precision and reliability. This experience
        sharpened my problem-solving skills and cultivated a strong foundation
        in teamwork and agile development.
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
    padding: 0 1em;
    scroll-snap-align: center;
  }
</style>
