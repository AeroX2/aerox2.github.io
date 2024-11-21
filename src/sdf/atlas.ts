import fontData from '../assets/font.json';
import fontAtlas from '../assets/font.png';

type Glyph = {
  unicode: number;
  advance: number;
  totalScaledAdvance: number;
  atlasBounds?: { left: number; bottom: number; right: number; top: number };
  planeBounds?: { left: number; bottom: number; right: number; top: number };
};

export class Atlas {
  createTexture(s: string): Promise<HTMLImageElement> {
    const glyphs: Glyph[] = [];
    let totalWidth = 0;
    let previousGlyph: Glyph | undefined;
    for (const c of s) {
      const glyphData =
        fontData.glyphs.find((o) => o.unicode == c.charCodeAt(0)) ??
        fontData.glyphs[0];
      const glyph = { ...glyphData, totalScaledAdvance: 0 };

      const w =
        (glyph.atlasBounds?.right ?? 0) - (glyph.atlasBounds?.left ?? 0);
      if (!previousGlyph) {
        totalWidth += w;
        glyph.totalScaledAdvance = 0;
      } else {
        const sp = previousGlyph.advance * fontData.atlas.size;
        totalWidth += w;
        glyph.totalScaledAdvance += previousGlyph.totalScaledAdvance + sp;
      }

      const kernel = fontData.kerning.find(
        (o) =>
          o.unicode1 == previousGlyph?.unicode && o.unicode2 == glyph.unicode
      );
      if (kernel) {
        glyph.advance += kernel.advance;
      }

      glyphs.push(glyph);
      previousGlyph = glyph;
    }

    const fontAtlasImage = new Image();
    fontAtlasImage.src = fontAtlas;

    return new Promise((resolve) => {
      fontAtlasImage.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = totalWidth;
        const hh = fontData.metrics.lineHeight * fontData.atlas.size;
        canvas.height = hh * 2;

        const ctx = canvas.getContext('2d');
        if (ctx == null) return;

        for (const glyph of glyphs) {
          const { left, right, top, bottom } = glyph.atlasBounds ?? {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          };
          const w = fontAtlasImage.width;
          const h = fontAtlasImage.height;

          const sx = left;
          const sy = h - top;
          const sw = right - left;
          const sh = top - bottom;
          const x = glyph.totalScaledAdvance;
          const y =
            hh - sh - (glyph.planeBounds?.bottom ?? 0) * fontData.atlas.size;

          ctx.drawImage(fontAtlasImage, sx, sy, sw, sh, x, y, sw, sh);
        }

        const img = new Image();
        img.src = canvas.toDataURL();
        document.body.prepend(img);
        resolve(img);
      };
    });
  }
}
