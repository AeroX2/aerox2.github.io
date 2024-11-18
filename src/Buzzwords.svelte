<script>
  import nodejs from 'devicon/icons/nodejs/nodejs-original.svg';
  import csharp from 'devicon/icons/csharp/csharp-original.svg';
  import javascript from 'devicon/icons/javascript/javascript-original.svg';
  import typescript from 'devicon/icons/typescript/typescript-original.svg';
  import angular from 'devicon/icons/angularjs/angularjs-original.svg';

  import cpp from 'devicon/icons/cplusplus/cplusplus-original.svg';
  import python from 'devicon/icons/python/python-original.svg';
  import java from 'devicon/icons/java/java-original.svg';
  import android from 'devicon/icons/android/android-original.svg';
  import kotlin from 'devicon/icons/kotlin/kotlin-original.svg';
</script>

<h3>Skills</h3>
<h6>Or the buzzwords section</h6>
<div class="row">
  <div class="column center">
    <h5>I have worked with these languages in a professional setting.</h5>
  </div>
  <div class="column center">
    <h5>
      I have gained experience with these languages through personal projects.
    </h5>
  </div>
  <div class="column center">
    <h5>And I have a strong knowledge of these concepts.</h5>
  </div>
</div>

<div class="row">
  <div class="column skill-list">
    <ul>
      <li>
        <img class="dev-icon" src={nodejs} alt="NodeJS logo" />
        NodeJS
      </li>
      <li>
        <img class="dev-icon" src={csharp} alt="C# logo" />
        C#
      </li>
      <li>
        <img class="dev-icon" src={javascript} alt="Javascript logo" />
        Javascript
      </li>
      <li>
        <img class="dev-icon" src={typescript} alt="Typescript logo" />
        Typescript
      </li>
      <li>
        <img class="dev-icon" src={angular} alt="Angular logo" />
        Angular
      </li>
    </ul>
  </div>

  <div class="column skill-list">
    <ul>
      <li>
        <img class="dev-icon" src={cpp} alt="C++ logo" />
        C++
      </li>
      <li>
        <img class="dev-icon" src={python} alt="Python logo" />
        Python
      </li>
      <li>
        <img class="dev-icon" src={java} alt="Java logo" />
        Java
      </li>
      <li>
        <img class="dev-icon" src={android} alt="Android logo" />
        Android (Java)
      </li>
      <li>
        <img class="dev-icon" src={kotlin} alt="Kotlin logo" />
        Kotlin
      </li>
    </ul>
  </div>

  <div class="column skill-list">
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
  .center {
    display: flex;
    align-items: center;
  }

  .dev-icon {
    width: 1em;
    vertical-align: text-top;
  }

  .skill-list {
    display: flex;
    justify-content: center;
  }

  .skill-list ul {
    list-style-type: none;
    text-align: left;
  }

  .skill-list ul li::before {
    content: '•';
    font-size: 1em;
    color: #666;
    margin-right: 0.5em;
  }
</style>
