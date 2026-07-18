<script lang="ts">
  import { onMount } from 'svelte';
  import ModelViewer from './lib/ModelViewer.svelte';
  import RobodogViewer from './lib/RobodogViewer.svelte';
  import KiCanvasViewer from './lib/KiCanvasViewer.svelte';
  import type { ShowcaseMedia } from './showcaseMedia';

  type ProjectView = {
    title: string;
    eyebrow: string;
    status: string;
    summary: string;
    note: string;
    tags: string[];
    href?: string;
    links?: { label: string; href: string }[];
    credit?: { label: string; href: string };
    journeyEyebrow?: string;
    journeyTitle?: string;
    journey?: { label: string; title: string; description: string }[];
  };

  let {
    project,
    media,
    onclose
  }: { project: ProjectView; media: ShowcaseMedia[]; onclose: () => void } =
    $props();
  let dialogElement: HTMLDivElement;

  const mediaPriority = (item: ShowcaseMedia) => {
    if (item.type === 'model' || item.type === 'robot-model' || item.type === 'board') return 0;
    if (item.type === 'image') return 1;
    return 2;
  };

  const orderedMedia = $derived(
    media
      .filter(
        (item, index, items) =>
          items.findIndex((candidate) => candidate.type === item.type && candidate.src === item.src) === index
      )
      .map((item, index) => ({ item, index }))
      .sort((a, b) => mediaPriority(a.item) - mediaPriority(b.item) || a.index - b.index)
      .map(({ item }) => item)
  );

  onMount(() => {
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    dialogElement.focus();
    return () => {
      document.body.style.overflow = previous;
    };
  });
</script>

<svelte:window onkeydown={(event) => event.key === 'Escape' && onclose()} />

<div
  class="dialog-backdrop"
  role="presentation"
  onclick={(event) => event.target === event.currentTarget && onclose()}
>
  <div
    class="showcase-dialog"
    role="dialog"
    aria-modal="true"
    aria-labelledby="showcase-title"
    tabindex="-1"
    bind:this={dialogElement}
  >
    <header>
      <div>
        <span>{project.status}</span>
        <p>{project.eyebrow}</p>
        {#if orderedMedia.length}
          <small>{orderedMedia.length} media pieces</small>
        {:else}
          <small>Project note</small>
        {/if}
      </div>
      <button
        type="button"
        onclick={onclose}
        aria-label="Close project showcase">Close ×</button
      >
    </header>
    <div class="showcase-intro">
      <h2 id="showcase-title">{project.title}</h2>
      <div>
        <p>{project.summary}</p>
        <p>{project.note}</p>
        {#if project.credit}
          <p class="project-credit">
            Model credit:
            <a href={project.credit.href} target="_blank" rel="noreferrer">{project.credit.label} ↗</a>
          </p>
        {/if}
      </div>
      <ul>
        {#each project.tags as tag (tag)}<li>{tag}</li>{/each}
      </ul>
    </div>
    {#if project.journey}
      <section class="continuity" aria-labelledby="continuity-title">
        <div class="continuity-heading">
          <span>{project.journeyEyebrow || 'Build history'}</span>
          <h3 id="continuity-title">{project.journeyTitle || 'How it evolved'}</h3>
        </div>
        <div class="continuity-track">
          {#each project.journey as chapter (chapter.title)}
            <article>
              <span>{chapter.label}</span>
              <h4>{chapter.title}</h4>
              <p>{chapter.description}</p>
            </article>
          {/each}
        </div>
      </section>
    {/if}
    <div class="showcase-media">
      {#each orderedMedia as item, index (`${item.type}-${item.src}`)}
        <article
          class:wide={item.type === 'video' ||
            item.type === 'model' ||
            item.type === 'robot-model' ||
            item.type === 'board' ||
            (item.type === 'image' && item.wide)}
        >
          {#if item.type === 'image'}
            <img
              src={item.src}
              alt={item.alt}
              loading={index === 0 ? 'eager' : 'lazy'}
            />
          {:else if item.type === 'video'}
            <video
              controls
              preload="metadata"
              poster={item.poster}
              class:cropped={item.crop}
              style:object-position={item.position || '50% 50%'}
              ><source src={item.src} type="video/mp4" /></video
            >
          {:else if item.type === 'youtube'}
            <iframe
              src={item.src}
              title={item.title}
              loading="lazy"
              referrerpolicy="strict-origin-when-cross-origin"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
            ></iframe>
          {:else if item.type === 'model'}
            <ModelViewer
              src={item.src}
              poster={item.poster}
              alt={item.alt}
              caption={item.caption}
            />
          {:else if item.type === 'robot-model'}
            <RobodogViewer
              src={item.src}
              poster={item.poster}
              alt={item.alt}
              caption={item.caption}
            />
          {:else}
            <KiCanvasViewer
              src={item.src}
              poster={item.poster}
              title={item.title}
            />
          {/if}
          {#if item.type === 'image' || item.type === 'video' || item.type === 'youtube'}<p>
              {item.caption}
            </p>{/if}
        </article>
      {/each}
    </div>
    <footer>
      <span>Project specimen / selected evidence</span>
      <div class="source-links">
        {#if project.links}
          {#each project.links as link (link.href)}<a
              href={link.href}
              target="_blank"
              rel="noreferrer">{link.label} ↗</a
            >{/each}
        {:else if project.href}<a
            href={project.href}
            target="_blank"
            rel="noreferrer">Source and files ↗</a
          >{/if}
      </div>
    </footer>
  </div>
</div>

<style>
  .dialog-backdrop {
    position: fixed;
    z-index: 100;
    inset: 0;
    padding: 24px;
    overflow: auto;
    background: rgba(10, 18, 35, 0.78);
    backdrop-filter: blur(9px);
  }
  .showcase-dialog {
    position: relative;
    width: min(1120px, 100%);
    margin: 2vh auto;
    padding: 24px;
    color: var(--ink);
    background: var(--paper-bright);
    box-shadow: 18px 18px 0 var(--acid);
    animation: unfold-sheet 280ms cubic-bezier(0.22, 0.75, 0.22, 1) both;
  }
  .showcase-dialog::after {
    position: absolute;
    top: 0;
    right: 0;
    width: 46px;
    height: 46px;
    background: linear-gradient(135deg, #d4dce3 0 48%, #aebbc7 49% 52%, var(--paper) 53%);
    clip-path: polygon(100% 0, 0 0, 100% 100%);
    filter: drop-shadow(-3px 4px 2px rgba(21, 27, 42, 0.16));
    content: '';
    pointer-events: none;
  }
  @keyframes unfold-sheet {
    from {
      opacity: 0;
      transform: perspective(1200px) rotateX(-2deg) translateY(18px) scale(0.985);
      transform-origin: 50% 0;
    }
    to {
      opacity: 1;
      transform: none;
    }
  }
  header,
  footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    border-bottom: 1px solid var(--ink);
    padding-bottom: 18px;
  }
  header div {
    display: flex;
    gap: 12px;
    align-items: center;
  }
  header span,
  header p,
  header small,
  header button,
  footer,
  li {
    font-family: 'Recursive Variable', monospace;
    font-variation-settings: 'MONO' 1;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  header span {
    padding: 6px 8px;
    color: white;
    background: var(--orange);
    font-size: 9px;
    font-weight: 800;
  }
  header p {
    font-size: 9px;
    font-weight: 700;
  }
  header small {
    color: var(--muted);
    font-size: 8px;
  }
  header button {
    border: 0;
    padding: 10px;
    background: transparent;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
  }
  .showcase-intro {
    padding: clamp(38px, 7vw, 80px) 0 45px;
  }
  h2 {
    max-width: 850px;
    font-size: clamp(56px, 9vw, 112px);
    line-height: 0.85;
  }
  .showcase-intro > div {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
    max-width: 900px;
    margin: 40px 0 0 auto;
  }
  .showcase-intro > div p {
    font-size: 17px;
    line-height: 1.52;
  }
  .showcase-intro > div p + p {
    color: var(--muted);
  }
  .showcase-intro > div .project-credit {
    grid-column: 1 / -1;
    padding: 12px 14px;
    border-left: 4px solid var(--orange);
    color: var(--ink);
    background: rgba(232, 255, 98, 0.34);
    font-family: 'Recursive Variable', monospace;
    font-size: 10px;
    font-variation-settings: 'MONO' 1;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .project-credit a {
    color: var(--blue-dark);
    text-underline-offset: 3px;
  }
  ul {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin: 26px 0 0 auto;
    max-width: 900px;
    list-style: none;
  }
  li {
    padding: 6px 8px;
    border: 1px solid var(--ink);
    font-size: 8px;
    font-weight: 750;
  }
  .showcase-media {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }
  .continuity {
    margin: 0 0 50px;
    padding: 26px 0 0;
    border-top: 2px solid var(--ink);
  }
  .continuity-heading {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 30px;
    margin-bottom: 22px;
  }
  .continuity-heading span,
  .continuity-track article > span {
    color: var(--orange);
    font-family: 'Recursive Variable', monospace;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .continuity-heading h3 {
    font-size: clamp(29px, 4vw, 48px);
  }
  .continuity-track {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    border: 1px solid var(--ink);
  }
  .continuity-track article {
    position: relative;
    padding: 18px 14px 22px;
    background: var(--paper);
  }
  .continuity-track article + article {
    border-left: 1px solid var(--ink);
  }
  .continuity-track article::before {
    position: absolute;
    top: -5px;
    left: 14px;
    width: 9px;
    height: 9px;
    border: 1px solid var(--ink);
    border-radius: 50%;
    background: var(--acid);
    content: '';
  }
  .continuity-track h4 {
    margin-top: 13px;
    font-family: 'Recursive Variable', sans-serif;
    font-size: 18px;
    line-height: 1;
  }
  .continuity-track p {
    margin-top: 10px;
    color: var(--muted);
    font-size: 11px;
    line-height: 1.4;
  }
  .showcase-media article {
    min-width: 0;
    padding: 10px;
    background: var(--paper);
    border: 1px solid rgba(21, 27, 42, 0.45);
  }
  .showcase-media article.wide {
    grid-column: 1 / -1;
  }
  img {
    display: block;
    width: 100%;
    height: clamp(260px, 26vw, 360px);
    margin: 0 auto;
    object-fit: contain;
    background: #cbd2d8;
  }
  video {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: contain;
    background: #151b2a;
  }
  video.cropped {
    max-width: 760px;
    margin-inline: auto;
    aspect-ratio: 4 / 3;
    object-fit: cover;
  }
  iframe {
    display: block;
    width: 100%;
    height: clamp(260px, 26vw, 360px);
    border: 0;
    background: #151b2a;
  }
  .showcase-media article > p {
    padding: 12px 4px 4px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.45;
  }
  footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-top: 28px;
    padding: 14px 12px;
    color: var(--paper-bright);
    background: var(--ink);
    border-top: 0;
    border-bottom: 0;
    font-size: 9px;
    font-weight: 700;
  }
  footer a {
    color: var(--acid);
  }
  .source-links {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: flex-end;
  }
  @media (max-width: 800px) {
    .continuity-track {
      grid-template-columns: 1fr;
    }
    .continuity-track article + article {
      border-top: 1px solid var(--ink);
      border-left: 0;
    }
  }
  @media (max-width: 650px) {
    .dialog-backdrop {
      padding: 0;
    }
    .showcase-dialog {
      margin: 0;
      min-height: 100vh;
      padding: 16px;
      box-shadow: none;
    }
    footer {
      align-items: flex-start;
      flex-direction: column;
    }
    .source-links {
      justify-content: flex-start;
    }
    .showcase-dialog::after {
      width: 34px;
      height: 34px;
    }
    header div p {
      display: none;
    }
    .showcase-intro > div,
    .showcase-media {
      grid-template-columns: 1fr;
    }
    .showcase-media article.wide {
      grid-column: auto;
    }
    .continuity-heading {
      display: block;
    }
    .continuity-heading h3 {
      margin-top: 8px;
    }
    footer > span {
      display: none;
    }
  }
</style>
