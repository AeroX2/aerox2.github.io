<script lang="ts">
  import google from './assets/google.svg';
  import canva from './assets/canva.svg';
  import first from './assets/first.png';
  import thoughdesign from './assets/thoughtdesign.png';
  import TextScramble from './lib/TextScramble.svelte';

  const experiences = [
    {
      date: '2020-2025',
      company: 'Canva',
      logo: canva,
      desc:
        'At Canva, I built several AI features. I led the Magic Design project, ' +
        'which integrated Generative AI into the core platform and launched for Droptober. ' +
        'I also ran the Team Brain initiative, delivering an AI-powered search prototype ' +
        'for internal knowledge retrieval. Separately, I worked on the Forms, Polls, ' +
        'and Quizzes overhaul, which involved refactoring legacy code to reduce ' +
        'technical debt. I mentored junior engineers and helped with team knowledge sharing.'
    },
    {
      date: '2017-2018',
      company: 'Google',
      logo: google,
      desc:
        'I completed two internships at Google in 2017 and 2018. In 2017, ' +
        'I built a new internal tool for Google Maps to help streamline their workflow. ' +
        'In 2018, I joined the Neighbourly team to port their web application to the Jiophone. ' +
        'This required reverse-engineering the existing system with minimal documentation ' +
        'to deliver a fully functional app and creating comprehensive documentation for the team.'
    },
    {
      date: '2014-2020',
      company: 'ThoughtDesign',
      logo: thoughdesign,
      desc:
        'I worked part-time at ThoughtDesign from 2014 to 2020. I developed web ' +
        'applications using MVC and ASP.NET and customized JavaScript libraries for ' +
        'commercial use. By 2018, I was managing several Angular projects, ' +
        'implementing Protractor for end-to-end testing, and establishing a ' +
        'TypeScript unit testing framework.'
    },
    {
      date: '2013-2016',
      company: 'FIRST Robotics',
      logo: first,
      desc:
        'From 2013 to 2016, I was the lead software developer for a FIRST ' +
        'Robotics team. I worked with the team to design, build, and test a 50kg ' +
        'robot for international competition. I was responsible for developing ' +
        'critical components of the robot control system within a strict six-week ' +
        'deadline, ensuring high precision and reliability during competition.'
    }
  ];
</script>

<h3><TextScramble>Experience</TextScramble></h3>

<div class="vertical-timeline">
  {#each experiences as item (item.company)}
    <div class="timeline-item">
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <div class="date"><TextScramble>{item.date}</TextScramble></div>
        <div class="company-header">
          <img
            src={item.logo}
            alt="{item.company} logo"
            class={item.company === 'ThoughtDesign' ? 'theme-icon' : ''}
          />
          <h4><TextScramble>{item.company}</TextScramble></h4>
        </div>
        <p><TextScramble>{item.desc}</TextScramble></p>
      </div>
    </div>
  {/each}
</div>

<style>
  .vertical-timeline {
    position: relative;
    max-width: 800px;
    margin: 2rem auto;
    padding-left: 2rem;
  }

  .vertical-timeline::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(
      to bottom,
      var(--accent-primary),
      var(--accent-secondary)
    );
    border-radius: 2px;
  }

  .timeline-item {
    position: relative;
    margin-bottom: 4rem;
    text-align: left;
  }

  .timeline-item:last-child {
    margin-bottom: 0;
  }

  .timeline-marker {
    position: absolute;
    left: -2.35rem;
    top: 0.5rem;
    width: 0.8rem;
    height: 0.8rem;
    border-radius: 50%;
    background: var(--accent-primary);
    box-shadow: 0 0 10px var(--accent-primary);
    border: 2px solid var(--bg-color);
  }

  .timeline-content {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 2rem;
    transition: transform 0.3s ease;
  }

  .timeline-content:hover {
    transform: translateX(10px);
    border-color: var(--accent-primary);
  }

  .date {
    font-family: var(--font-heading);
    color: var(--accent-primary);
    font-weight: 800;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    display: inline-block;
  }

  .company-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .company-header img {
    height: 2.5rem;
    width: auto;
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.2));
  }

  .company-header h4 {
    margin: 0;
    font-size: 1.6rem;
    color: var(--text-primary);
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.8;
    font-size: 1.15rem;
  }
  @media (max-width: 600px) {
    .vertical-timeline {
      padding-left: 1.5rem;
      margin: 1rem 0;
    }

    .timeline-marker {
      left: -1.85rem;
    }

    .timeline-content {
      padding: 1.25rem;
    }

    .company-header h4 {
      font-size: 1.4rem;
    }

    p {
      font-size: 1rem;
    }
  }
</style>
