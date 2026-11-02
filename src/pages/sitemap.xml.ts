import type { APIRoute } from 'astro';
import { allProjects } from '../data/projects';

export const GET: APIRoute = ({ site }) => {
  const paths = [
    '/',
    ...allProjects.map((project) => `/projects/${project.slug}`)
  ];
  const urls = paths
    .map((path) => `  <url><loc>${new URL(path, site)}</loc></url>`)
    .join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;
  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' }
  });
};
