# James Ridey's websites

One repository and npm installation builds the workshop at `jamesridey.dev`
and the professional site at `cv.jamesridey.dev`.

```sh
npm ci
npm run build
```

Outputs are `dist/workshop` and `dist/cv`. The build validates assets, résumé
consistency, and Cloudflare Pages limits. Run `npm run check` for Svelte and
TypeScript validation.

The workshop is an Astro site (`src/pages`) that prerenders the Svelte app to
static HTML, with one page per project at `/projects/<slug>`. Project data
lives in `src/data/projects.ts`. The CV is plain HTML built by
`vite.cv.config.ts`.

Use `npm run dev` for the workshop and `npm run dev:cv` for the CV. Use
`npm run preview` and `npm run preview:cv` to inspect production outputs.
Both websites get their PDF from `shared/James-Ridey-Resume.pdf`.

GitHub Actions builds both once and deploys the matching output to each
Cloudflare Pages project. Main pushes deploy both sites; pull requests only
build and validate. GitHub Pages deployments are removed; the old site must be unpublished in
repository Settings > Pages.

See [build and migration instructions](docs/professional-site.md) for account
setup, secrets, rollout, and rollback.
