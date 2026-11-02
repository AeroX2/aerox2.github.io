const previewPattern = /^\/(projects|labeled-media)\/(.+)\.(?:jpe?g|png|webp)$/i;
const previewWidths = [400, 640, 1200];

function previewBase(source: string) {
  const match = source.match(previewPattern);
  return match ? `/card-media/${match[1]}/${match[2]}` : null;
}

/** Returns the srcset of the WebP previews for a source image, if it has them. */
export function previewSrcset(source: string) {
  const base = previewBase(source);
  if (!base) return undefined;
  return previewWidths
    .map((width) => `${base}-${width}.webp ${width}w`)
    .join(', ');
}

/** Returns the 1200px WebP preview for a source image, for social cards. */
export function cardImage(source: string) {
  const base = previewBase(source);
  return base ? `${base}-1200.webp` : source;
}
