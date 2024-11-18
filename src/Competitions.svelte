<script>
  import Card from './lib/Card.svelte';

  import flareon from './assets/images/flareon.png';
  import cysca from './assets/images/cysca.png';
  import asean from './assets/images/asean.jpg';
  import hackmac from './assets/images/hackmac.png';
  import ncss from './assets/images/ncss.png';
</script>

<!-- <div class="container"> -->
<h3>Competitions:</h3>
<h5>(tap on each card to learn more)</h5>
<Card
  title="FlareOn - Global Reverse Engineering Competition"
  backgroundImage={flareon}
>
  <div slot="front">
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li>
          <i class="fa fa-star"></i>2024 - Rank 190th (6th in Australia)<br />
        </li>
        <li><i class="fa fa-star"></i>2023 - Rank 170th<br /></li>
        <li><i class="fa fa-star"></i>2022 - Rank 292nd<br /></li>
      </ul>
    </div>
  </div>
  <div slot="back">
    <p>
      A Windows-centric reverse engineering CTF contest that features a total of
      12 challenges covering a variety of architectures from x86 on Windows,
      .NET, Linux, Android and for 2019 a NES ROM challenge.
    </p>
    <p>
      This competition revolves around reverse engineering malicious samples,
      mainly Windows, figuring out how they work and finding a certain flag in
      order to proceed to the next question.
    </p>
  </div>
</Card>

<Card title="CySCA 2018 - Cyber Security Competition" backgroundImage={cysca}>
  <div slot="front">
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>Rank 15/108 teams</li>
      </ul>
    </div>
  </div>
  <div slot="back">
    <p>
      CySCA is a hacking competition run by an alliance of the Australian
      Government, business and academic professionals who are committed to
      finding the next generation of Australian cyber security talent.
    </p>
    <p>
      The competition involves breaking into Boot2Root machines and finding
      various web exploits, design flaws, and general security vulnerabilities.
    </p>
  </div>
</Card>

<Card title="ASEAN Australia Codeathon 2018" backgroundImage={asean}>
  <div slot="front">
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>Overall runner up</li>
        <li><i class="fa fa-star"></i>Applying Blockchain Technology winner</li>
      </ul>
    </div>
  </div>
  <div slot="back">
    <p>
      Over 32 hours, the Codeathon brings together financial intelligence units
      (FIUs), banks, developers, innovators, and other partners to create
      innovative solutions for curbing terrorism financing and enhancing
      cybersecurity.
    </p>
    <p>
      A codeathon competition focused on solving complex issues related to
      terrorism financing and cybersecurity.
    </p>
  </div>
</Card>

<Card title="Hack Mac 2017 Competition" backgroundImage={hackmac}>
  <div slot="front">
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>1st place - Winning a trip to AusCERT</li>
      </ul>
    </div>
  </div>
  <div slot="back">
    <p>
      Macquarie University IT has designed and built hacking challenges for
      Macquarie University undergraduate students.
    </p>
    <p>
      A hacking competition focused on Boot2Root machines, allowing students to
      break into official Macquarie services to earn points.
    </p>
  </div>
</Card>

<Card title="USYD NCSS Python Programming Challenge" backgroundImage={ncss}>
  <div slot="front">
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>2014 - Advanced - Perfect score</li>
        <li><i class="fa fa-star"></i>2013 - Advanced - Perfect score</li>
        <li><i class="fa fa-star"></i>2012 - Intermediate - Perfect score</li>
        <li><i class="fa fa-star"></i>2011 - Advanced - Credit</li>
      </ul>
    </div>
  </div>
  <div slot="back">
    <p>
      The NCSS Challenge is a programming competition open to all school
      students and teachers. The Grok Learning team has been running coding
      competitions for over 12 years.
    </p>
    <p>
      A Python programming challenge running for 5 weeks, where a new set of
      questions is released each week and students have until the end of the
      week to complete them.
    </p>
  </div>
</Card>

<style>
  .fa-star {
    color: #ffd700;
    text-shadow: 0 0 3px #000;
    padding-right: 0.5em;
  }

  .star-list {
    text-align: left;
    margin-left: auto;
    margin-right: auto;
  }
</style>
