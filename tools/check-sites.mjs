import assert from 'node:assert/strict';
import { readFile, readdir, stat } from 'node:fs/promises';
import { resolve, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const resume = await readFile(resolve(root, 'shared/James-Ridey-Resume.pdf'));

async function checkFiles(directory) {
  let count = 0;
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = resolve(directory, entry.name);
    if (entry.isDirectory()) count += await checkFiles(file);
    else {
      assert(
        (await stat(file)).size <= 25 * 1024 * 1024,
        `Pages asset exceeds 25 MiB: ${file}`
      );
      count++;
    }
  }
  return count;
}

async function htmlPages(directory) {
  const pages = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = resolve(directory, entry.name);
    if (entry.isDirectory()) pages.push(...(await htmlPages(file)));
    else if (entry.name.endsWith('.html')) pages.push(file);
  }
  return pages;
}

async function resolveLocal(directory, clean) {
  const file = resolve(directory, clean.replace(/^\//, ''));
  assert(
    !relative(directory, file).startsWith('..'),
    `Asset escapes output: ${clean}`
  );
  for (const candidate of [file, `${file}.html`, resolve(file, 'index.html')]) {
    const info = await stat(candidate).catch(() => null);
    if (info?.isFile()) return candidate;
  }
  assert.fail(`Missing local asset: ${clean}`);
}

for (const site of ['workshop', 'cv']) {
  const directory = resolve(root, 'dist', site);
  const pages =
    site === 'cv'
      ? [resolve(directory, 'index.html')]
      : await htmlPages(directory);
  const html = await readFile(resolve(directory, 'index.html'), 'utf8');
  const count = await checkFiles(directory);
  assert(count <= 20000, `${site} exceeds the Pages Free file limit`);
  const pdfName =
    site === 'cv' ? 'James-Ridey-Resume.pdf' : 'resume-technical.pdf';
  assert.deepEqual(
    await readFile(resolve(directory, pdfName)),
    resume,
    `${site} résumé differs`
  );
  const cssFiles = [];
  for (const page of pages) {
    const pageHtml = await readFile(page, 'utf8');
    for (const [, url] of pageHtml.matchAll(/(?:src|href)="([^"#]+)"/g)) {
      if (/^(?:[a-z]+:|\/\/)/i.test(url)) continue;
      const clean = decodeURIComponent(url.split(/[?#]/)[0]);
      const file = await resolveLocal(directory, clean);
      if (file.endsWith('.css')) cssFiles.push(file);
    }
  }
  for (const cssFile of cssFiles) {
    const css = await readFile(cssFile, 'utf8');
    for (const [, url] of css.matchAll(/url\(["']?([^"')]+)["']?\)/g)) {
      if (/^(?:[a-z]+:|\/\/|#)/i.test(url)) continue;
      const file = url.startsWith('/')
        ? resolve(directory, url.slice(1))
        : resolve(dirname(cssFile), url);
      assert((await stat(file)).isFile(), `Missing CSS asset: ${url}`);
    }
  }
  if (site === 'cv') {
    assert(
      !/[\u00c2\u00c3\u00e2][\u0080-\u00bf\u2010-\u2122]|\ufffd/.test(html),
      'CV contains broken UTF-8 text'
    );
    assert(html.includes('cv.jamesridey.dev'), 'Missing CV canonical domain');
    await stat(resolve(directory, 'social/jrb8.webp'));
    await stat(resolve(directory, '404.html'));
  } else {
    assert(
      html.includes('class="featured-project"'),
      'Workshop index is not prerendered'
    );
    const robodog = await readFile(
      resolve(directory, 'projects/robodog.html'),
      'utf8'
    );
    assert(
      robodog.includes('<title>Robot dog'),
      'Project pages are missing their own titles'
    );
    const sitemap = await readFile(resolve(directory, 'sitemap.xml'), 'utf8');
    assert(
      sitemap.includes('/projects/robodog</loc>'),
      'Sitemap is incomplete'
    );
    await stat(resolve(directory, '404.html'));
  }
  console.log(
    `${site}: ${count} files, local assets and shared résumé verified.`
  );
}
