<script lang="ts">
  import TextScramble from './lib/TextScramble.svelte';
  import nodejs from 'devicon/icons/nodejs/nodejs-original.svg';
  import csharp from 'devicon/icons/csharp/csharp-original.svg';
  import javascript from 'devicon/icons/javascript/javascript-original.svg';
  import typescript from 'devicon/icons/typescript/typescript-original.svg';
  import react from 'devicon/icons/react/react-original.svg';
  import angular from 'devicon/icons/angularjs/angularjs-original.svg';
  import cpp from 'devicon/icons/cplusplus/cplusplus-original.svg';
  import golang from 'devicon/icons/go/go-original.svg';
  import python from 'devicon/icons/python/python-original.svg';
  import java from 'devicon/icons/java/java-original.svg';
  import android from 'devicon/icons/android/android-original.svg';
  import kotlin from 'devicon/icons/kotlin/kotlin-original.svg';
  interface Skill {
    name: string;
    icon?: string;
  }

  interface SkillGroup {
    name: string;
    skills: Skill[];
  }

  const skillGroups: SkillGroup[] = [
    {
      name: 'Core Languages',
      skills: [
        { name: 'Python', icon: python },
        { name: 'Java', icon: java },
        { name: 'Kotlin', icon: kotlin },
        { name: 'Android', icon: android },
        { name: 'C/C++', icon: cpp },
        { name: 'Go', icon: golang }
      ]
    },
    {
      name: 'Web & Tooling',
      skills: [
        { name: 'Javascript', icon: javascript },
        { name: 'Typescript', icon: typescript },
        { name: 'React', icon: react },
        { name: 'Angular', icon: angular },
        { name: 'NodeJS', icon: nodejs },
        { name: 'C#', icon: csharp }
      ]
    },
    {
      name: 'Expertise',
      skills: [
        { name: 'Reverse Engineering' },
        { name: 'Cybersecurity' },
        { name: 'Algorithms' },
        { name: 'Machine Learning' },
        { name: 'System Design' },
        { name: 'Memory Forensics' }
      ]
    }
  ];
</script>

<div class="skill-cloud-container">
  <h3 class="section-title"><TextScramble>Technical Arsenal</TextScramble></h3>

  <div class="skill-groups">
    {#each skillGroups as group}
      <div class="group-container">
        <h5 class="group-label"><TextScramble>{group.name}</TextScramble></h5>
        <div class="cloud-wrapper">
          {#each group.skills as skill}
            <div class="skill-chip">
              {#if skill.icon}
                <img
                  class="skill-icon"
                  src={skill.icon}
                  alt="{skill.name} logo"
                />
              {/if}
              <span><TextScramble>{skill.name}</TextScramble></span>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .skill-cloud-container {
    padding: 1rem 0;
  }

  .section-title {
    text-align: center;
    margin-bottom: 3rem;
  }

  .skill-groups {
    display: flex;
    flex-direction: column;
    gap: 3rem;
  }

  .group-label {
    font-size: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    text-align: center;
    opacity: 0.7;
  }

  .cloud-wrapper {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
    max-width: 900px;
    margin: 0 auto;
  }

  .skill-chip {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    padding: 0.6rem 1.2rem;
    border-radius: 100px;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    cursor: default;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    font-weight: 500;
    color: var(--text-primary);
  }

  .skill-chip:hover {
    transform: translateY(-5px) scale(1.05);
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--accent-primary);
    box-shadow: 0 10px 20px rgba(0, 242, 255, 0.15);
  }

  .skill-icon {
    width: 1.4rem;
    height: 1.4rem;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  }

  @media (max-width: 600px) {
    .cloud-wrapper {
      gap: 0.6rem;
    }
    .skill-chip {
      padding: 0.4rem 0.9rem;
      font-size: 0.9rem;
    }
    .skill-icon {
      width: 1.1rem;
      height: 1.1rem;
    }
  }
</style>
