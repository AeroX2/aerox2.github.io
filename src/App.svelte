<script lang="ts">
  import { onMount, untrack } from 'svelte';
  import ProjectShowcaseDialog from './ProjectShowcaseDialog.svelte';
  import ProjectImageRotator from './ProjectImageRotator.svelte';
  import CertificateDialog from './CertificateDialog.svelte';
  import {
    drawerProjects,
    findProject,
    projectImages,
    projectMedia,
    projects,
    archive,
    type Certificate,
    type Project
  } from './data/projects';
  import nullifyLogo from './assets/nullify.svg?url';
  import canvaLogo from './assets/canva.svg?url';
  import googleLogo from './assets/google.svg?url';
  import thoughtDesignLogo from './assets/thoughtdesign.webp?url';
  import firstLogo from './assets/first.webp?url';
  import githubIcon from '@fortawesome/fontawesome-free/svgs/brands/github.svg?url';
  import linkedinIcon from '@fortawesome/fontawesome-free/svgs/brands/linkedin.svg?url';
  import emailIcon from '@fortawesome/fontawesome-free/svgs/solid/envelope.svg?url';
  import resumeIcon from '@fortawesome/fontawesome-free/svgs/solid/file-pdf.svg?url';

  let {
    initialSlug = null,
    buildYear
  }: { initialSlug?: string | null; buildYear: number } = $props();

  let year = $state(untrack(() => buildYear));

  let selectedProject = $state<Project | null>(untrack(() => findProject(initialSlug)));
  let selectedCertificate = $state<Certificate | null>(null);
  let openedProjects = $state<string[]>([]);
  let activeDocumentSection = $state<string | null>(null);
  const dialogHistoryKey = 'aerox2Dialog';
  let dialogHistoryEntryActive = false;
  const featuredProject = projects.find((project) => project.slug === 'robodog')!;
  const supportingProjects = ['motor-controller', 'epaper-smart-watch', 'led-display']
    .map((slug) => projects.find((project) => project.slug === slug))
    .filter((project): project is Project => Boolean(project));
  const featuredSlugs = new Set([featuredProject.slug, ...supportingProjects.map((project) => project.slug)]);
  const machineProjects = projects.filter((project) => !featuredSlugs.has(project.slug));

  const homeTitle = 'James Ridey — software, silicon & strange machines';

  $effect(() => {
    document.title = selectedProject ? `${selectedProject.title} — James Ridey` : homeTitle;
  });

  onMount(() => {
    year = new Date().getFullYear();

    const handlePopState = () => {
      const project = projectFromLocation();
      if (project) {
        selectedProject = project;
        selectedCertificate = null;
        dialogHistoryEntryActive = Boolean(history.state?.[dialogHistoryKey]);
        if (!openedProjects.includes(project.slug)) openedProjects = [...openedProjects, project.slug];
      } else {
        dialogHistoryEntryActive = false;
        selectedProject = null;
        selectedCertificate = null;
      }
    };

    handlePopState();
    window.addEventListener('popstate', handlePopState);

    const sectionIds = ['work', 'machine-index', 'parts', 'experience', 'contact'];
    const sections = sectionIds
      .map((id) => document.getElementById(id))
      .filter((section): section is HTMLElement => Boolean(section));
    let animationFrame: number | undefined;
    const updateActiveSection = () => {
      animationFrame = undefined;
      const current = sections.filter((section) => {
        const offset = parseFloat(getComputedStyle(section).scrollMarginTop) || 0;
        return section.getBoundingClientRect().top <= offset + 1;
      }).at(-1);
      const atPageEnd = window.scrollY + window.innerHeight >=
        document.documentElement.scrollHeight - 1;
      activeDocumentSection = (atPageEnd ? sections.at(-1) : current)?.id ?? null;
    };
    const scheduleActiveSectionUpdate = () => {
      if (animationFrame !== undefined) return;
      animationFrame = window.requestAnimationFrame(updateActiveSection);
    };

    scheduleActiveSectionUpdate();
    window.addEventListener('scroll', scheduleActiveSectionUpdate, { passive: true });
    window.addEventListener('resize', scheduleActiveSectionUpdate);
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.removeEventListener('scroll', scheduleActiveSectionUpdate);
      window.removeEventListener('resize', scheduleActiveSectionUpdate);
      if (animationFrame !== undefined) window.cancelAnimationFrame(animationFrame);
    };
  });

  function projectFromLocation() {
    const match = window.location.pathname.match(/^\/projects\/([^/.]+)/);
    return findProject(match?.[1]);
  }

  function projectLocation(slug: string) {
    return `/projects/${slug}`;
  }

  function addDialogHistoryEntry() {
    if (dialogHistoryEntryActive) return;

    const currentState = typeof history.state === 'object' && history.state ? history.state : {};
    history.pushState({ ...currentState, [dialogHistoryKey]: true }, '');
    dialogHistoryEntryActive = true;
  }

  function closeDialog() {
    if (selectedProject) {
      if (dialogHistoryEntryActive && history.state?.[dialogHistoryKey]) {
        history.back();
        return;
      }

      history.replaceState(history.state, '', '/');
      selectedProject = null;
      return;
    }

    if (dialogHistoryEntryActive && history.state?.[dialogHistoryKey]) {
      history.back();
      return;
    }

    dialogHistoryEntryActive = false;
    selectedProject = null;
    selectedCertificate = null;
  }

  function openShowcase(project: Project) {
    selectedCertificate = null;
    selectedProject = project;
    const currentState = typeof history.state === 'object' && history.state ? history.state : {};
    history.pushState(
      { ...currentState, [dialogHistoryKey]: true, projectSlug: project.slug },
      '',
      projectLocation(project.slug)
    );
    dialogHistoryEntryActive = true;
    if (!openedProjects.includes(project.slug)) openedProjects = [...openedProjects, project.slug];
  }

  function openFromLink(event: MouseEvent, project: Project) {
    const modified = event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;
    if (modified || event.button !== 0) return;
    event.preventDefault();
    openShowcase(project);
  }

  function openCertificate(certificate: Certificate) {
    selectedProject = null;
    selectedCertificate = certificate;
    addDialogHistoryEntry();
  }

  function projectMediaCount(slug: string) {
    return projectMedia(slug).length;
  }

</script>

<header class="site-header">
  <a class="wordmark" href="#top">
    <img class="site-logo" src="/site-logo.webp" width="40" height="40" alt="James Ridey" />
    <small>software / silicon / everything between</small>
  </a>
  <nav aria-label="Primary navigation">
    <a href="#work">Work</a>
    <a href="#parts">Parts drawer</a>
    <a href="#experience">Experience</a>
    <a class="nav-exit" href="/resume-technical.pdf" target="_blank" rel="noreferrer" aria-label="Resume (PDF, opens in a new tab)">
      <img src={resumeIcon} width="16" height="16" alt="" />Resume ↗
    </a>
  </nav>
</header>

<nav class="document-index" aria-label="Document index">
  <a href="#work" class:active={activeDocumentSection === 'work'} aria-current={activeDocumentSection === 'work' ? 'location' : undefined}>Work</a>
  <a href="#machine-index" class:active={activeDocumentSection === 'machine-index'} aria-current={activeDocumentSection === 'machine-index' ? 'location' : undefined}>Machines</a>
  <a href="#parts" class:active={activeDocumentSection === 'parts'} aria-current={activeDocumentSection === 'parts' ? 'location' : undefined}>Parts</a>
  <a href="#experience" class:active={activeDocumentSection === 'experience'} aria-current={activeDocumentSection === 'experience' ? 'location' : undefined}>Experience</a>
  <a href="#contact" class:active={activeDocumentSection === 'contact'} aria-current={activeDocumentSection === 'contact' ? 'location' : undefined}>Contact</a>
</nav>

<main id="top">
  <div class="project-ticker" aria-hidden="true">
    <div class="ticker-track">
      <div class="ticker-group">
        <span>Robot dog · four legs assembled</span><span>JRB8 · silicon verified</span>
        <span>Light gun · wireless path working</span><span>E-paper watch · routing version two</span>
        <span>Moon lamp · orbit nominal</span>
      </div>
      <div class="ticker-group">
        <span>Robot dog · four legs assembled</span><span>JRB8 · silicon verified</span>
        <span>Light gun · wireless path working</span><span>E-paper watch · routing version two</span>
        <span>Moon lamp · orbit nominal</span>
      </div>
    </div>
  </div>
  <section class="portfolio-hero" aria-labelledby="hero-title">
    <div class="hero-heading-row">
      <div class="hero-identity">
        <h1 id="hero-title"><span>James</span> Ridey<i>.</i></h1>
        <p class="hero-subtitle">Software engineer / hardware tinkerer</p>
      </div>
      <aside class="hero-field-notes" aria-label="Career field notes">
        <header><span>JR / operating card</span></header>
        <div class="field-note-record">
          <p><strong>2013</strong><span>Career start</span></p>
          <p><strong>FRC</strong><span>software lead / 50 kg robot</span></p>
          <p><strong>4×</strong><span>Flare-On finisher</span></p>
          <p><strong>1</strong><span>CPU in silicon</span></p>
        </div>
        <p class="field-note-history"><span>Work history</span><b>Nullify · Canva · Google ×2</b></p>
        <p class="field-note-history"><span>Current work</span><b>AI products · frontend architecture</b></p>
        <p class="field-note-history"><span>After hours</span><b>Robotics · silicon · fabrication</b></p>
      </aside>
    </div>
    <div class="hero-ledger">
      <p class="hero-intro">
        I’m a software engineer working across frontend architecture, AI products,
        and developer tools. I also design and build hardware, from custom circuit
        boards and processors to robots and embedded systems.
      </p>
    </div>
  </section>

  <section class="featured-section section-card" id="work" aria-labelledby="work-title">
    <div class="document-heading">
      <h2 id="work-title">On the bench right now</h2>
    </div>
    <div class="featured-layout">
      <a class="featured-project" href={projectLocation(featuredProject.slug)} onclick={(event) => openFromLink(event, featuredProject)}>
        <ProjectImageRotator images={projectImages(featuredProject)} alt={featuredProject.alt} position={featuredProject.imagePosition || '50% 50%'} variant="featured" />
        <span class="featured-status">In progress</span>
        <span class="featured-copy">
          <small>{featuredProject.eyebrow}</small>
          <strong>{featuredProject.title}</strong>
          <span>{featuredProject.summary}</span>
          <b class="project-open">Open project →</b>
        </span>
      </a>
      <div class="supporting-projects">
        {#each supportingProjects as project (project.slug)}
          <a class="project-link" href={projectLocation(project.slug)} onclick={(event) => openFromLink(event, project)}>
            <ProjectImageRotator images={projectImages(project)} alt={project.alt} position={project.imagePosition || '50% 50%'} variant="supporting" />
            <span>
              <small>{project.status}</small>
              <strong>{project.title}</strong>
              <em>{project.summary}</em>
              <b class="project-open">Open project →</b>
            </span>
          </a>
        {/each}
      </div>
    </div>
  </section>

  <section class="machine-index section-card" id="machine-index" aria-labelledby="machine-index-title">
    <div class="document-heading">
      <h2 id="machine-index-title">Machine index</h2>
    </div>
    <div class="machine-list">
      {#each machineProjects as project (project.slug)}
        <a class="project-link" href={projectLocation(project.slug)} onclick={(event) => openFromLink(event, project)}>
          <span class="machine-copy">
            <strong>{project.title}</strong>
            <span>{project.summary}</span>
            <b class="project-open">Open project →</b>
          </span>
          <ProjectImageRotator images={projectImages(project)} alt={project.alt} position={project.imagePosition || '50% 50%'} variant="machine" />
        </a>
      {/each}
    </div>
  </section>

  <section class="archive-section section-card" id="parts" aria-labelledby="archive-title">
    <div class="document-heading">
      <h2 id="archive-title">Parts drawer</h2>
    </div>
    <div class="parts-cabinet">
      <div class="parts-bins">
        {#each archive as item, index (item.title)}
          {#if item.slug && drawerProjects[item.slug]}
          <a class={`parts-bin bin-${index + 1}`} class:opened={openedProjects.includes(item.slug)} href={projectLocation(item.slug)} onclick={(event) => openFromLink(event, drawerProjects[item.slug!])}>
            <span class="bin-heading">
              <span class="bin-code">{String(index + 1).padStart(2, '0')} / {item.tag}</span>
              {#if projectMediaCount(item.slug)}<span class="bin-media-count">{projectMediaCount(item.slug)} {projectMediaCount(item.slug) === 1 ? 'piece' : 'pieces'}</span>{/if}
            </span>
            {#if projectImages(drawerProjects[item.slug]).length > 0 && !['seed-reversal', 'advent-of-code', 'onnxstream-sdxl'].includes(item.slug)}
              <ProjectImageRotator images={projectImages(drawerProjects[item.slug])} alt={drawerProjects[item.slug].alt} variant="drawer" />
            {:else if item.title === 'Seed reversal GPU optimization'}
              <figure class="drawer-visual pack-visual"><img src="/projects/pack.webp" width="128" height="128" alt="The original Minecraft pack.png" /><figcaption>3257840388504953787</figcaption></figure>
            {:else if item.title === 'Advent of Code'}
              <pre class="drawer-visual ascii-visual" aria-label="Festive Advent of Code ASCII art">        *
       /o\
      /@*o\
     /o**@*\
    /_*_o_*_\
       ||
  2019 — 2024</pre>
            {:else if item.title === 'OnnxStream / SDXL'}
              <pre class="drawer-visual code-visual diff-visual" aria-label="Excerpt from the merged SDXL Turbo pull request"><span class="diff-file">PR #46 · src/sd.cpp</span>
<span class="diff-del">- int dim = sdxl_params ? 128 : 64;</span>
<span class="diff-add">+ int dim = turbo ? 64 : 128;</span>
<span class="diff-add">+ if (turbo) return denoised_cond;</span>
<span class="diff-del">- float delta = -999.f / (step - 1);</span>
<span class="diff-add">+ float delta = step &gt; 1 ? -999.f / (step - 1) : 0.f;</span></pre>
            {:else if item.title === 'E-paper smart watch'}
              <div class="bin-object board" aria-hidden="true"><i></i><i></i><i></i></div>
            {:else}
              <div class="bin-object type" aria-hidden="true">{item.title.slice(0, 2)}</div>
            {/if}
            <strong>{item.title}</strong>
            <p>{item.description}</p>
            <span class="bin-open">Open project →</span>
          </a>
          {:else}
          <a class={`parts-bin bin-${index + 1}`} href={item.href} target="_blank" rel="noreferrer">
            <span class="bin-heading"><span class="bin-code">{String(index + 1).padStart(2, '0')} / {item.tag}</span></span>
            {#if item.title === 'Seed reversal GPU optimization'}
              <figure class="drawer-visual pack-visual"><img src="/projects/pack.webp" width="128" height="128" alt="The original Minecraft pack.png" /><figcaption>3257840388504953787</figcaption></figure>
            {:else if item.title === 'Advent of Code'}
              <pre class="drawer-visual ascii-visual" aria-label="Festive Advent of Code ASCII art">        *
       /o\
      /@*o\
     /o**@*\
    /_*_o_*_\
       ||
  2019 — 2024</pre>
            {:else if item.title === 'OnnxStream / SDXL'}
              <pre class="drawer-visual code-visual diff-visual" aria-label="Excerpt from the merged SDXL Turbo pull request"><span class="diff-file">PR #46 · src/sd.cpp</span>
<span class="diff-del">- int dim = sdxl_params ? 128 : 64;</span>
<span class="diff-add">+ int dim = turbo ? 64 : 128;</span>
<span class="diff-add">+ if (turbo) return denoised_cond;</span>
<span class="diff-del">- float delta = -999.f / (step - 1);</span>
<span class="diff-add">+ float delta = step &gt; 1 ? -999.f / (step - 1) : 0.f;</span></pre>
            {:else}
              <div class="bin-object type" aria-hidden="true">{item.title.slice(0, 2)}</div>
            {/if}
            <strong>{item.title}</strong>
            <p>{item.description}</p>
            <span class="bin-open">Source ↗</span>
          </a>
          {/if}
        {/each}
      </div>
    </div>
  </section>

  <section class="experience-section section-card" id="experience" aria-labelledby="experience-title">
    <div class="document-heading">
      <h2 id="experience-title">Experience + credentials</h2>
    </div>
    <div class="resume-record">
      <div class="experience-list">
        <article>
          <time>2025—now</time>
          <div class="company-name"><img src={nullifyLogo} alt="" /><h3>Nullify</h3></div>
          <p>Building AI product features and leading a ground-up rebuild of the frontend for Nullify's autonomous product-security platform.</p>
          <span>Software engineering / frontend architecture / AI</span>
        </article>
        <article>
          <time>2020—2025</time>
          <div class="company-name"><img src={canvaLogo} alt="" /><h3>Canva</h3></div>
          <p>Architected Magic Design's state layer and shipped it two weeks ahead of launch; also rebuilt marketplace filtering for 150M+ monthly users, prototyped internal knowledge search, and mentored engineers.</p>
          <span>Software engineering / AI products</span>
        </article>
        <article>
          <time>2017—2019</time>
          <div class="company-name"><img src={googleLogo} alt="" /><h3>Google</h3></div>
          <p>Built an internal Google Maps feedback tool, then ported Neighbourly to KaiOS/JioPhone within a 512 MB memory ceiling and wrote the team's first porting specification.</p>
          <span>Software engineering internships</span>
        </article>
        <article>
          <time>2014—2017</time>
          <div class="company-name"><img src={thoughtDesignLogo} alt="" /><h3>ThoughtDesign</h3></div>
          <p>Built ASP.NET MVC and Angular applications, then took ownership of Angular projects and their Protractor test infrastructure.</p>
          <span>Full-stack software engineering</span>
        </article>
        <article>
          <time>2013—2016</time>
          <div class="company-name"><img src={firstLogo} alt="" /><h3>FIRST Robotics</h3></div>
          <p>Led software for a 50 kg competition robot, built and tested under the traditional six-week deadline.</p>
          <span>Lead software developer</span>
        </article>
      </div>
      <aside class="credentials-panel" id="credentials" aria-label="Credentials and recognition">
        <div class="resume-subheading">
          <span>Selected evidence</span>
          <strong>Qualifications + recognition</strong>
        </div>
        <div class="credentials-grid">
          <article class="credential-card credential-featured credential-with-proof">
            <p class="credential-meta">PortSwigger</p>
            <h3>Burp Suite Certified Practitioner</h3>
            <ul class="credential-highlights">
              <li>Issued in 2026, valid until 2032</li>
              <li>Attack-surface discovery and defensive bypasses</li>
              <li>Out-of-band testing techniques</li>
              <li>Business-impact analysis</li>
            </ul>
            <div class="credential-actions">
            <a
              class="credential-proof"
              href="/projects/burp-suite-certified-practitioner.png"
              onclick={(event) => {
                event.preventDefault();
                openCertificate({
                  title: 'Burp Suite Certified Practitioner',
                  src: '/projects/burp-suite-certified-practitioner.png',
                  alt: 'Burp Suite Certified Practitioner certificate awarded to James Ridey'
                });
              }}
            >
              View certificate ↗
            </a>
            <a href="https://portswigger.net/web-security/e/c/a2836e9325092f5f" target="_blank" rel="noreferrer">Verify credential ↗</a>
            </div>
          </article>
          <article class="credential-card credential-with-proof">
            <p class="credential-meta">Reverse engineering / security</p>
            <h3>Flare-On + offensive IoT</h3>
            <ul class="credential-highlights">
              <li>Four-time Flare-On finisher</li>
              <li>157th of 4,100+ entrants in 2025</li>
              <li>Completed DEF CON’s three-day Offensive IoT Exploitation course in firmware and hardware reverse engineering</li>
            </ul>
            <div class="credential-actions">
            <a
              class="credential-proof"
              href="/projects/offensive-iot-certificate.jpg"
              onclick={(event) => {
                event.preventDefault();
                openCertificate({
                  title: 'Offensive IoT Exploitation',
                  src: '/projects/offensive-iot-certificate.jpg',
                  alt: 'DEF CON Offensive IoT Exploitation certificate awarded to James Ridey'
                });
              }}
            >
              View certificate ↗
            </a>
            </div>
          </article>
          <article class="credential-card">
            <p class="credential-meta">Macquarie University</p>
            <h3>Software Design</h3>
            <ul class="credential-highlights">
              <li>Bachelor of Engineering (Honours)</li>
              <li>Studied from 2016 to 2020</li>
              <li>Head of Computing Award in five semesters, for the highest academic mark in the cohort</li>
            </ul>
          </article>
          <article class="credential-card">
            <p class="credential-meta">Competitions</p>
            <h3>Built and tested under pressure</h3>
            <ul class="credential-highlights">
              <li>Hack Mac — first place</li>
              <li>ASEAN–Australia Codeathon — runner-up</li>
              <li>CySCA — 17th of 108 teams nationally</li>
            </ul>
          </article>
        </div>
      </aside>
    </div>
  </section>

  <section class="contact-section section-card" id="contact" aria-labelledby="contact-title">
    <h2 id="contact-title">End of website. <span>Not of projects<i>.</i></span></h2>
    <p>Follow the builds, browse the half-finished experiments, or open an issue when I have wired something backwards.</p>
    <div class="contact-actions">
      <a class="button primary" href="https://github.com/AeroX2" target="_blank" rel="noreferrer"><img src={githubIcon} alt="" />GitHub ↗</a>
      <a class="button secondary" href="https://linkedin.com/in/james-ridey" target="_blank" rel="noreferrer"><img src={linkedinIcon} alt="" />LinkedIn ↗</a>
      <a class="button secondary" href="mailto:james@ridey.email"><img src={emailIcon} alt="" />Email ↗</a>
      <a class="button secondary" href="/resume-technical.pdf" target="_blank" rel="noreferrer" aria-label="Resume (PDF, opens in a new tab)"><img src={resumeIcon} alt="" />Resume ↗</a>
    </div>
  </section>
</main>

<footer>
  <span>© {year} James Ridey</span>
  <span>Designed in code. Tested on hardware. No robots were emotionally harmed.</span>
  <a href="#top">Back to top ↑</a>
</footer>

{#if selectedProject}
  <ProjectShowcaseDialog
    project={selectedProject}
    media={[
      ...projectMedia(selectedProject.slug),
      ...(projectMedia(selectedProject.slug).length === 0
        && selectedProject.slug !== 'advent-of-code'
        ? [{ type: 'image' as const, src: selectedProject.image, alt: selectedProject.alt, caption: selectedProject.summary }]
        : [])
    ]}
    onclose={closeDialog}
  />
{/if}

{#if selectedCertificate}
  <CertificateDialog
    title={selectedCertificate.title}
    src={selectedCertificate.src}
    alt={selectedCertificate.alt}
    onclose={closeDialog}
  />
{/if}
