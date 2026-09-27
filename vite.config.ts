import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig, type Plugin } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

const path = (relative: string) =>
  fileURLToPath(new URL(relative, import.meta.url));

// A single committed PDF supplies both sites, including the existing workshop URL.
function siteFiles(cv: boolean): Plugin {
  let building = false;
  const files: Record<string, string> = cv
    ? {
        'James-Ridey-Resume.pdf': 'shared/James-Ridey-Resume.pdf',
        'robots.txt': 'cv/robots.txt',
        'sitemap.xml': 'cv/sitemap.xml',
        '404.html': 'cv/404.html',
        'social/jrb8.webp': 'cv/assets/jrb8.webp',
        'FONT-LICENSE.txt': 'cv/assets/FONT-LICENSE.txt'
      }
    : { 'resume-technical.pdf': 'shared/James-Ridey-Resume.pdf' };
  return {
    name: 'site-files',
    configResolved(config) {
      building = config.command === 'build';
    },
    buildStart() {
      if (!building) return;
      for (const [fileName, source] of Object.entries(files)) {
        this.emitFile({
          type: 'asset',
          fileName,
          source: readFileSync(path(source))
        });
      }
    },
    configureServer(server) {
      server.middlewares.use((request, response, next) => {
        const name = new URL(
          request.url || '/',
          'http://localhost'
        ).pathname.slice(1);
        if (name !== (cv ? 'James-Ridey-Resume.pdf' : 'resume-technical.pdf'))
          return next();
        response.setHeader('Content-Type', 'application/pdf');
        response.setHeader('Cache-Control', 'no-cache');
        response.end(readFileSync(path('shared/James-Ridey-Resume.pdf')));
      });
    }
  };
}

export default defineConfig(({ mode }) => {
  const cv = mode === 'cv';
  return {
    root: cv ? path('cv') : path('.'),
    publicDir: cv ? false : path('public'),
    plugins: cv ? [siteFiles(true)] : [svelte(), siteFiles(false)],
    build: {
      outDir: path(cv ? 'dist/cv' : 'dist/workshop'),
      emptyOutDir: true
    }
  };
});
