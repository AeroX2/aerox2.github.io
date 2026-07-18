import { createReadStream, existsSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const toolRoot = fileURLToPath(new URL('.', import.meta.url));
const repoRoot = resolve(toolRoot, '..', '..');
const labelsPath = join(repoRoot, 'docs', 'media-labels.json');
const sourceFlag = process.argv.indexOf('--source');
const sourceDir = resolve(sourceFlag >= 0 ? process.argv[sourceFlag + 1] : 'C:\\Users\\James\\Downloads\\my-projects');
const portFlag = process.argv.indexOf('--port');
const port = Number(portFlag >= 0 ? process.argv[portFlag + 1] : 4174);
const supported = new Set(['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov', '.m4v', '.webm']);

if (!existsSync(sourceDir)) throw new Error(`Media source does not exist: ${sourceDir}`);

const contentTypes = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp',
  '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.m4v': 'video/mp4', '.webm': 'video/webm'
};

const projects = [
  'Robot dog', 'Motor controller', 'Wireless light gun', 'Sand table', 'Moon lamp', 'E-paper smart watch',
  'Ethereal ink frame', 'JRB8 computer', 'Single-key keyboard', 'Brother cartridge emulator', 'Mechanical wallet',
  'FTL models', 'LED display', 'Nintendo DS', 'Advent of Code', 'Flare-On', 'Other / unknown'
];

function loadLabels() {
  try { return JSON.parse(readFileSync(labelsPath, 'utf8')); }
  catch { return { version: 1, updatedAt: null, labels: {} }; }
}

function listItems() {
  const { readdirSync } = awaitImportFs();
  return readdirSync(sourceDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && supported.has(extname(entry.name).toLowerCase()))
    .map((entry) => {
      const stat = statSync(join(sourceDir, entry.name));
      const extension = extname(entry.name).toLowerCase();
      return { name: entry.name, kind: ['.mp4', '.mov', '.m4v', '.webm'].includes(extension) ? 'video' : 'image', size: stat.size, modified: stat.mtimeMs };
    })
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
}

function awaitImportFs() {
  // Kept synchronous so rescans are deterministic and instant for this small collection.
  return { readdirSync: (path, options) => readDir(path, options) };
}

import { readdirSync as readDir } from 'node:fs';

function json(response, status, value) {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  response.end(JSON.stringify(value));
}

function serveFile(response, path, request) {
  const stat = statSync(path);
  const type = contentTypes[extname(path).toLowerCase()] || 'application/octet-stream';
  const range = request.headers.range;
  if (range) {
    const [startText, endText] = range.replace('bytes=', '').split('-');
    const start = Number(startText);
    const end = endText ? Number(endText) : Math.min(start + 4 * 1024 * 1024 - 1, stat.size - 1);
    response.writeHead(206, { 'Content-Type': type, 'Accept-Ranges': 'bytes', 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Content-Length': end - start + 1 });
    createReadStream(path, { start, end }).pipe(response);
    return;
  }
  response.writeHead(200, { 'Content-Type': type, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes' });
  createReadStream(path).pipe(response);
}

const server = createServer((request, response) => {
  const url = new URL(request.url, `http://${request.headers.host}`);
  if (request.method === 'GET' && url.pathname === '/api/items') {
    const data = loadLabels();
    return json(response, 200, { sourceDir, labelsPath, projects, items: listItems(), ...data });
  }
  if (request.method === 'POST' && url.pathname === '/api/labels') {
    let body = '';
    request.on('data', (chunk) => { body += chunk; if (body.length > 5_000_000) request.destroy(); });
    request.on('end', () => {
      try {
        const incoming = JSON.parse(body);
        const validNames = new Set(listItems().map((item) => item.name));
        const labels = Object.fromEntries(Object.entries(incoming.labels || {}).filter(([name]) => validNames.has(name)));
        const data = { version: 1, updatedAt: new Date().toISOString(), labels };
        writeFileSync(labelsPath, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
        json(response, 200, { ok: true, updatedAt: data.updatedAt });
      } catch (error) { json(response, 400, { ok: false, error: error.message }); }
    });
    return;
  }
  if (request.method === 'GET' && url.pathname.startsWith('/media/')) {
    const name = basename(decodeURIComponent(url.pathname.slice('/media/'.length)));
    const path = join(sourceDir, name);
    if (!supported.has(extname(name).toLowerCase()) || !existsSync(path)) return json(response, 404, { error: 'Media not found' });
    return serveFile(response, path, request);
  }
  const staticName = url.pathname === '/' ? 'index.html' : basename(url.pathname);
  const staticPath = join(toolRoot, staticName);
  if (['index.html', 'app.js', 'style.css'].includes(staticName) && existsSync(staticPath)) return serveFile(response, staticPath, request);
  return json(response, 404, { error: 'Not found' });
});

server.listen(port, '127.0.0.1', () => {
  console.log(`\nMedia labeler: http://127.0.0.1:${port}`);
  console.log(`Source: ${sourceDir}`);
  console.log(`Labels: ${labelsPath}\n`);
});
