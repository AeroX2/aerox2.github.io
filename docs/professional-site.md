# Both websites: one repository and build

Run `npm ci`, then `npm run build`. Vite builds both sites with the same
installation and configuration. The build finishes by checking local asset
references, identical résumé content, and Cloudflare Pages asset limits.

| Site              | Output        | Local development | Production preview |
| ----------------- | ------------- | ----------------- | ------------------ |
| jamesridey.dev    | dist/workshop | npm run dev       | npm run preview    |
| cv.jamesridey.dev | dist/cv       | npm run dev:cv    | npm run preview:cv |

The CV remains HTML/CSS with no application JavaScript. Vite processes its
stylesheet, fonts, and images. Deploy the output folders, never raw `cv/` or
the entire repository. Each output is served at its domain's root.

## Shared résumé

`shared/James-Ridey-Resume.pdf` is the single PDF source for both builds. Vite
serves it in development and emits it as `resume-technical.pdf` for the workshop
and `James-Ridey-Resume.pdf` for the CV, preserving both existing URLs.

Update that shared file from the completed résumé project's
`output/pdf/resume-systems.pdf`. The LaTeX source remains in the résumé project;
web builds need no LaTeX installation or access to that sibling checkout.
Private interview notes and internal evidence links must not enter web assets.

## Cloudflare migration

The GitHub Actions workflow builds once and reuses the same output for both
Pages deployments. Pull requests build and validate without publishing. The
two deployments are sequential, not atomic: if the second fails, retry it or
roll back the first through Cloudflare's deployment history.

1. Create two **Direct Upload** Pages projects in the Cloudflare account that
   manages jamesridey.dev: `jamesridey-workshop` and `jamesridey-cv`, each with
   production branch `main`. Don't also enable automatic Git builds.
2. Add repository Actions secrets `CLOUDFLARE_ACCOUNT_ID` and
   `CLOUDFLARE_API_TOKEN`. Scope the token to this account with Account →
   Cloudflare Pages → Edit. Enter it through GitHub's secrets interface, not
   a tracked file or chat. If using different project names, set repository
   variables `CLOUDFLARE_WORKSHOP_PROJECT` and `CLOUDFLARE_CV_PROJECT`.
3. Push these changes. Until the migration switch is enabled, main pushes keep
   publishing `dist/workshop` to GitHub Pages. The CV is included in the build
   artifact but is not sent to the workshop domain.
4. Manually run **Build and deploy both sites** on main with the Cloudflare
   option enabled. This publishes to the two `pages.dev` domains without
   changing DNS or disabling the current GitHub Pages site. The option refers
   to migration preview URLs; these are production-branch deployments of
   the two Cloudflare projects.
5. Verify both pages.dev homepages, PDFs, images, mobile navigation, workshop
   dialogs, and direct links such as `/projects/robodog`. The workshop's
   `_redirects` rewrites its named project paths to the SPA entry; GitHub's
   existing 404 fallback remains available during migration. Rules use exact
   paths so `/projects/*` image and model assets are not rewritten.
6. Add `jamesridey.dev` to the workshop project's Custom domains and
   `cv.jamesridey.dev` to the CV project's Custom domains. Follow Cloudflare's
   DNS instructions, replacing only conflicting website records. Preserve
   MX/TXT/email records. Verify HTTPS and both public domains before cutover
   is considered complete.
7. Set repository variable `CLOUDFLARE_PAGES_ENABLED` to `true`. Subsequent main
   pushes deploy both sites to Cloudflare and skip GitHub Pages. Keep the old
   GitHub deployment available until the new domains have been verified.

For a deployment rollback, use each Pages project's previous successful
deployment. Returning to GitHub hosting also requires restoring the recorded
workshop DNS records; merely changing the workflow switch does not change DNS.

The Direct Upload projects are created and deployed:

- Workshop: https://jamesridey-workshop.pages.dev
- CV: https://jamesridey-cv.pages.dev

Both GitHub Actions secrets are configured. Both custom domains are registered
with Pages. DNS cutover requires proxied CNAME records for `@` pointing to
`jamesridey-workshop.pages.dev` and `cv` pointing to `jamesridey-cv.pages.dev`.
The Pages deployment token deliberately has no DNS permissions. Preserve email
records and record the previous website DNS values before changing them.

References:

- https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/
- https://developers.cloudflare.com/pages/configuration/custom-domains/

## Content notes

Professional and independent experience are explicitly distinguished. Preserve
the measurement limits in the performance examples, Team Brain's prototype
status, attribution to Canva's existing renderer, and the personal nature of
the hardware projects. The IBM Plex Sans licence is emitted with the CV build.
