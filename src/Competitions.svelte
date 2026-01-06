<script lang="ts">
  import Card from './lib/Card.svelte';
  import TextScramble from './lib/TextScramble.svelte';

  import flareon from './assets/images/flareon.png';
  import cysca from './assets/images/cysca.png';
  import asean from './assets/images/asean.jpg';
  import hackmac from './assets/images/hackmac.png';
  import ncss from './assets/images/ncss.png';
</script>

<!-- <div class="container"> -->
<h3><TextScramble>Competitions</TextScramble></h3>
<h6 class="sub-text">
  <TextScramble>(tap or hover on each card to learn more)</TextScramble>
</h6>

<div class="bento-grid">
  <div class="bento-item large">
    <Card
      title="FlareOn - Global Reverse Engineering Competition"
      backgroundImage={flareon}
    >
      {#snippet front()}
        <div class="star-list">
          <ul class="list-no-space list-no-points">
            <li>
              <i class="fa fa-star"></i>2025 - Rank 157th / 313 Finishers<br />
            </li>
            <li>
              <i class="fa fa-star"></i>2024 - Rank 190th / 275 Finishers<br />
            </li>
            <li>
              <i class="fa fa-star"></i>2023 - Rank 170th / 219 Finishers<br />
            </li>
            <li>
              <i class="fa fa-star"></i>2022 - Rank 292nd / 494 Finishers<br />
            </li>
          </ul>
        </div>
      {/snippet}
      {#snippet back()}
        <p>
          An annual reverse engineering challenge covering x86, .NET, Linux,
          Android, and Esolangs.
        </p>
        <p>
          Required deobfuscating malware, writing custom debuggers, and
          reverse-engineering custom crypto.
        </p>
      {/snippet}
    </Card>
  </div>

  <div class="bento-item">
    <Card
      title="CySCA 2018 - Cyber Security Competition"
      backgroundImage={cysca}
    >
      {#snippet front()}
        <div class="star-list">
          <ul class="list-no-space list-no-points">
            <li><i class="fa fa-star"></i>Rank 15/108 teams</li>
          </ul>
        </div>
      {/snippet}
      {#snippet back()}
        <p>Australian Government initiative to find cyber talent.</p>
        <p>
          Compromised Boot2Root machines via web exploitation and forensics.
        </p>
      {/snippet}
    </Card>
  </div>

  <div class="bento-item">
    <Card title="ASEAN Australia Codeathon 2018" backgroundImage={asean}>
      {#snippet front()}
        <div class="star-list">
          <ul class="list-no-space list-no-points">
            <li><i class="fa fa-star"></i>Overall Runner Up</li>
            <li><i class="fa fa-star"></i>'Blockchain Tech' Winner</li>
          </ul>
        </div>
      {/snippet}
      {#snippet back()}
        <p>32-hour hackathon to curb terrorism financing.</p>
        <p>Built a blockchain tool to trace illicit funds.</p>
      {/snippet}
    </Card>
  </div>

  <div class="bento-item">
    <Card title="Hack Mac 2017 Competition" backgroundImage={hackmac}>
      {#snippet front()}
        <div class="star-list">
          <ul class="list-no-space list-no-points">
            <li><i class="fa fa-star"></i>1st Place</li>
          </ul>
        </div>
      {/snippet}
      {#snippet back()}
        <p>University-wide CTF event by Macquarie IT.</p>
        <p>Exploited university services via priv-esc and SQLi.</p>
      {/snippet}
    </Card>
  </div>

  <div class="bento-item">
    <Card title="USYD NCSS Python Challenge" backgroundImage={ncss}>
      {#snippet front()}
        <div class="star-list">
          <ul class="list-no-space list-no-points">
            <li><i class="fa fa-star"></i>2014 - Advanced - Perfect</li>
            <li><i class="fa fa-star"></i>2013 - Advanced - Perfect</li>
            <li><i class="fa fa-star"></i>2012 - Intermediate - Perfect</li>
          </ul>
        </div>
      {/snippet}
      {#snippet back()}
        <p>Algorithmic competition by USYD.</p>
        <p>Perfect scores for 3 years solving complex logic puzzles.</p>
      {/snippet}
    </Card>
  </div>
</div>

<style>
  .bento-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin-top: 1rem;
  }

  .bento-item {
    width: 100%;
  }

  .bento-item.large {
    grid-column: span 2;
  }

  @media (max-width: 768px) {
    .bento-grid {
      grid-template-columns: 1fr;
    }
    .bento-item.large {
      grid-column: span 1;
    }
  }

  .sub-text {
    color: var(--text-secondary);
    margin-bottom: 2rem;
    font-weight: 400;
  }

  .fa-star {
    color: #ffd700;
    text-shadow: 0 0 3px #000;
    padding-right: 0.5em;
  }

  .star-list {
    text-align: left;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    white-space: normal;
  }
</style>
