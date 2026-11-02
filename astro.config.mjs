import { copyFile, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

const resumeSource = fileURLToPath(
  new URL('./shared/James-Ridey-Resume.pdf', import.meta.url)
);
const resumeName = 'resume-technical.pdf';

/**
 * Serves the shared résumé in development and copies it into the build.
 * @returns {import('astro').AstroIntegration}
 */
function sharedResume() {
  return {
    name: 'shared-resume',
    hooks: {
      'astro:server:setup': ({ server }) => {
        server.middlewares.use(async (request, response, next) => {
          const { pathname } = new URL(request.url || '/', 'http://localhost');
          if (pathname !== `/${resumeName}`) return next();
          response.setHeader('Content-Type', 'application/pdf');
          response.setHeader('Cache-Control', 'no-cache');
          response.end(await readFile(resumeSource));
        });
      },
      'astro:build:done': async ({ dir }) => {
        await copyFile(resumeSource, new URL(resumeName, dir));
      }
    }
  };
}

export default defineConfig({
  site: 'https://jamesridey.dev',
  outDir: './dist/workshop',
  trailingSlash: 'never',
  build: {
    format: 'file',
    inlineStylesheets: 'always'
  },
  integrations: [svelte(), sharedResume()]
});
