import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig, type Plugin } from 'vite';

const path = (relative: string) =>
  fileURLToPath(new URL(relative, import.meta.url));

const resumeName = 'James-Ridey-Resume.pdf';
const resumeSource = 'shared/James-Ridey-Resume.pdf';

const files: Record<string, string> = {
  [resumeName]: resumeSource,
  'robots.txt': 'cv/robots.txt',
  'sitemap.xml': 'cv/sitemap.xml',
  '404.html': 'cv/404.html',
  'social/jrb8.webp': 'cv/assets/jrb8.webp',
  'FONT-LICENSE.txt': 'cv/assets/FONT-LICENSE.txt'
};

/** Emits the CV's static files and serves the shared résumé in development. */
function siteFiles(): Plugin {
  let building = false;
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
        if (name !== resumeName) return next();
        response.setHeader('Content-Type', 'application/pdf');
        response.setHeader('Cache-Control', 'no-cache');
        response.end(readFileSync(path(resumeSource)));
      });
    }
  };
}

export default defineConfig({
  root: path('cv'),
  publicDir: false,
  plugins: [siteFiles()],
  build: {
    outDir: path('dist/cv'),
    emptyOutDir: true
  }
});
