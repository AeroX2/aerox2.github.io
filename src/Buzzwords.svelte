<script lang="ts">
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
</script>

<h3 class="section-title">Technical Arsenal</h3>
<div class="buzzwords">
  <h5>Core Languages</h5>
  <div class="skill-list">
    <ul>
      <li>
        <img class="dev-icon" src={python} alt="Python logo" />
        Python
      </li>
      <li>
        <img class="dev-icon" src={java} alt="Java logo" />
        Java
      </li>
      <li>
        <img class="dev-icon" src={kotlin} alt="Kotlin logo" />
        Kotlin
      </li>
      <li>
        <img class="dev-icon" src={android} alt="Android logo" />
        Android (Java)
      </li>
      <li>
        <img class="dev-icon" src={cpp} alt="C++ logo" />
        C/C++
      </li>
      <li>
        <img class="dev-icon" src={golang} alt="Golang logo" />
        Golang
      </li>
    </ul>
  </div>

  <h5>Web & Tooling</h5>
  <div class="skill-list">
    <ul>
      <li>
        <img class="dev-icon" src={javascript} alt="Javascript logo" />
        Javascript
      </li>
      <li>
        <img class="dev-icon" src={typescript} alt="Typescript logo" />
        Typescript
      </li>
      <li>
        <img class="dev-icon" src={react} alt="React logo" />
        React
      </li>
      <li>
        <img class="dev-icon" src={angular} alt="Angular logo" />
        Angular 1/2
      </li>
      <li>
        <img class="dev-icon" src={nodejs} alt="NodeJS logo" />
        NodeJS
      </li>
      <li>
        <img class="dev-icon" src={csharp} alt="C# logo" />
        C#
      </li>
    </ul>
  </div>

  <h5>Technical Focus</h5>
  <div class="skill-list">
    <ul>
      <li>Reverse engineering</li>
      <li>Cybersecurity</li>
      <li>Datastructures</li>
      <li>Algorithms</li>
      <li>Design patterns</li>
      <li>Machine learning</li>
    </ul>
  </div>
</div>

<style>
  .buzzwords {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
    grid-column-gap: 0.8em;
    justify-items: center;
    align-items: center;
  }

  @media (min-width: 600px) {
    .buzzwords {
      grid-auto-flow: column;
      grid-template-columns: 1fr 1fr 1fr;
    }
  }

  .dev-icon {
    width: 1em;
    margin-right: 0.35em;
  }

  .skill-list {
    display: flex;
    justify-content: center;
  }

  .skill-list ul {
    list-style-type: none;
    text-align: left;
  }

  .skill-list ul li {
    display: flex;
    align-items: center;
  }

  .skill-list ul li::before {
    content: '•';
    font-size: 1em;
    color: var(--accent-primary);
    margin-right: 0.5em;
  }

  h5 {
    color: var(--text-primary);
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    border-left: 3px solid var(--accent-primary);
    padding-left: 1rem;
    text-align: left;
    width: 100%;
  }

  @media (max-width: 600px) {
    h5 {
      font-size: 1.4rem;
    }
    .skill-list ul li {
      font-size: 0.95rem;
    }
  }
</style>
