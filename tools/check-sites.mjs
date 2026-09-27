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

for (const site of ['workshop', 'cv']) {
  const directory = resolve(root, 'dist', site);
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
  for (const [, url] of html.matchAll(/(?:src|href)="([^"#]+)"/g)) {
    if (/^(?:[a-z]+:|\/\/)/i.test(url)) continue;
    const clean = decodeURIComponent(url.split(/[?#]/)[0]);
    const file = resolve(directory, clean.replace(/^\//, ''));
    assert(
      !relative(directory, file).startsWith('..'),
      `Asset escapes output: ${url}`
    );
    assert((await stat(file)).isFile(), `Missing ${site} asset: ${url}`);
    if (file.endsWith('.css')) cssFiles.push(file);
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
    assert(html.includes('cv.jamesridey.dev'), 'Missing CV canonical domain');
    await stat(resolve(directory, 'social/jrb8.webp'));
    await stat(resolve(directory, '404.html'));
  } else {
    const redirects = await readFile(resolve(directory, '_redirects'), 'utf8');
    assert(redirects.includes('/projects/robodog / 200'));
  }
  console.log(
    `${site}: ${count} files, local assets and shared résumé verified.`
  );
}
