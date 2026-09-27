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

## Cloudflare deployment

GitHub Actions builds once and deploys both outputs to Cloudflare Pages on main
pushes and manual runs. Pull requests only build and validate. The GitHub Pages
workflow job is removed; no migration switch is required. GitHub rejected API
deactivation (HTTP 422). Unpublish the old deployment in repository Settings >
Pages using the menu next to the live-site URL.

- Workshop: https://jamesridey.dev (project `jamesridey-workshop`)
- CV: https://cv.jamesridey.dev (project `jamesridey-cv`)

Both custom domains have been verified over HTTPS. DNS uses proxied CNAMEs to
`jamesridey-workshop.pages.dev` and `jamesridey-cv.pages.dev` respectively.
The `www` domain redirects to the root domain.

Repository secrets are `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`.
The token needs Account / Cloudflare Pages / Edit for that account, but no DNS
permissions. Optional repository variables `CLOUDFLARE_WORKSHOP_PROJECT` and
`CLOUDFLARE_CV_PROJECT` override project names. These are Direct Upload projects;
do not enable a second automatic Git build in Cloudflare.

Deployments are sequential, not atomic. If the second fails, retry the failed
job or roll back the first using Cloudflare deployment history. The workshop's
`_redirects` rewrites exact project paths to `/` without rewriting asset paths.
Verify project links and PDF downloads after deployments.

The latest deployment attempt failed authentication. Live sites were uploaded
through the CLI; CI deployment still needs verification after correcting the
repository API token.

References:

- https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/
- https://developers.cloudflare.com/pages/configuration/custom-domains/

## Content notes

Professional and independent experience are explicitly distinguished. Preserve
the measurement limits in the performance examples, Team Brain's prototype
status, attribution to Canva's existing renderer, and the personal nature of
the hardware projects. The IBM Plex Sans licence is emitted with the CV build.
