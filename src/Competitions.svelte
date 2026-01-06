<script lang="ts">
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
  {#snippet front()}
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li>
          <i class="fa fa-star"></i>2025 - Rank 157th / 313 Finishers (Top 3% of
          4139 Registered)<br />
        </li>
        <li>
          <i class="fa fa-star"></i>2024 - Rank 190th / 275 Finishers (Top 3% of
          5324 Registered)<br />
        </li>
        <li>
          <i class="fa fa-star"></i>2023 - Rank 170th / 219 Finishers (Top 3% of
          4767 Registered)<br />
        </li>
        <li>
          <i class="fa fa-star"></i>2022 - Rank 292nd / 494 Finishers (Top 5% of
          5345 Registered)<br />
        </li>
      </ul>
    </div>
  {/snippet}
  {#snippet back()}
    <p>
      An annual reverse engineering challenge with 12 levels covering x86, .NET,
      Linux, Android, and Esolangs.
    </p>
    <p>
      The challenges required deobfuscating malware, writing custom debuggers,
      and reverse-engineering custom crypto algorithms.
    </p>
  {/snippet}
</Card>

<Card title="CySCA 2018 - Cyber Security Competition" backgroundImage={cysca}>
  {#snippet front()}
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>Rank 15/108 teams</li>
      </ul>
    </div>
  {/snippet}
  {#snippet back()}
    <p>
      An Australian Government initiative to find the next generation of cyber
      talent.
    </p>
    <p>
      I competed against 108 teams to compromise Boot2Root machines. The
      challenges involved web exploitation, network forensics, and patching
      vulnerabilities in real-time.
    </p>
  {/snippet}
</Card>

<Card title="ASEAN Australia Codeathon 2018" backgroundImage={asean}>
  {#snippet front()}
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>Overall Runner Up</li>
        <li>
          <i class="fa fa-star"></i>'Applying Blockchain Technology' Winner
        </li>
      </ul>
    </div>
  {/snippet}
  {#snippet back()}
    <p>
      A 32-hour hackathon bringing together financial intelligence units and
      developers to curb terrorism financing.
    </p>
    <p>
      My team built a blockchain-based transaction analysis tool to trace
      illicit funds across borders, securing the "Applying Blockchain
      Technology" category win.
    </p>
  {/snippet}
</Card>

<Card title="Hack Mac 2017 Competition" backgroundImage={hackmac}>
  {#snippet front()}
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>1st Place</li>
      </ul>
    </div>
  {/snippet}
  {#snippet back()}
    <p>
      A university-wide capture-the-flag event designed by Macquarie University
      IT.
    </p>
    <p>
      I placed 1st by successfully exploiting vulnerabilities in sanctioned
      university services, including privilege escalation and database injection
      challenges.
    </p>
  {/snippet}
</Card>

<Card title="USYD NCSS Python Programming Challenge" backgroundImage={ncss}>
  {#snippet front()}
    <div class="star-list">
      <ul class="list-no-space list-no-points">
        <li><i class="fa fa-star"></i>2014 - Advanced - Perfect score</li>
        <li><i class="fa fa-star"></i>2013 - Advanced - Perfect score</li>
        <li><i class="fa fa-star"></i>2012 - Intermediate - Perfect score</li>
        <li><i class="fa fa-star"></i>2011 - Advanced - Credit</li>
      </ul>
    </div>
  {/snippet}
  {#snippet back()}
    <p>
      A 5-week algorithmic programming competition run by the University of
      Sydney.
    </p>
    <p>
      I achieved a perfect score for three consecutive years in the Advanced
      stream, solving complex logic puzzles and data processing problems within
      strict memory and timing constraints.
    </p>
  {/snippet}
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
