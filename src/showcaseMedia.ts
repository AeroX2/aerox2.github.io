export type ShowcaseMedia =
  | { type: 'image'; src: string; alt: string; caption: string; wide?: boolean }
  | { type: 'video'; src: string; poster?: string; caption: string; crop?: boolean; position?: string }
  | { type: 'youtube'; src: string; title: string; caption: string }
  | { type: 'model'; src: string; poster?: string; alt: string; caption: string }
  | { type: 'robot-model'; src: string; poster?: string; alt: string; caption: string }
  | { type: 'board'; src: string; poster?: string; title: string; caption: string };

export const showcaseMedia: Record<string, ShowcaseMedia[]> = {
  robodog: [
    { type: 'image', src: '/projects/robodog-pair.jpg', alt: 'Two robot dog revisions side by side', caption: 'Successive mechanical revisions, kept around for comparison.' },
    { type: 'image', src: '/projects/robodog-controllers.jpg', alt: 'Robot dog joints with local motor controllers', caption: 'Joint-mounted controllers and the current mechanical assembly.' },
    { type: 'robot-model', src: '/models/robodog-interactive.glb', poster: '/labeled-media/img_20260708_141350321.jpg', alt: 'Interactive articulated robot dog assembly', caption: 'Interactive view of Paul Gould’s original quadruped model, prepared for the web from the Phobos URDF.' }
  ],
  'motor-controller': [
    { type: 'image', src: '/projects/motor-controller.jpg', alt: 'Custom motor controller installed beside a joint', caption: 'Compact BLDC control built for the robot dog.' },
    { type: 'board', src: '/boards/motor-controller.kicad_pcb', poster: '/projects/motor-controller.jpg', title: 'Robot-dog motor controller', caption: 'Open the real KiCad source in KiCanvas.' }
  ],
  'light-gun': [
    { type: 'model', src: '/models/light-gun.glb', poster: '/projects/light-gun-side.jpg', alt: 'Interactive wireless light gun enclosure', caption: 'Inspect the three-part enclosure.' }
  ],
  'sand-table': [
    { type: 'image', src: '/projects/sand-table-mechanism.jpg', alt: 'Printed gear train inside the sand table', caption: 'The compact polar drawing mechanism.' },
    { type: 'image', src: '/projects/sand-table.jpg', alt: 'The complete coffee-table prototype', caption: 'Built and moving, but paused while reliability problems are diagnosed.' }
  ],
  'moon-lamp': [],
  'single-key-keyboard': [],
  'brother-cart': [
    { type: 'image', src: '/projects/brother-cartridge.jpg', alt: 'Disassembled Brother embroidery cartridge', caption: 'Reverse-engineered storage hardware and a replacement cartridge.' }
  ],
  'epaper-frame': [
    { type: 'image', src: '/projects/epaper-frame.jpg', alt: 'E-paper frame showing generative artwork', caption: 'Generated images presented with the permanence of a print.' }
  ],
  'flare-on': [
    { type: 'image', src: '/labeled-media/img_20250205_194546494.jpg', alt: 'Flare-On 2024 reverse-engineering medal', caption: 'The 2024 Flare-On medal, earned by finishing the full challenge set for a fourth year.' }
  ],
  jrb8: [
    { type: 'image', src: '/projects/jrb8-still.jpg', alt: 'JRB8 running on a Tiny Tapeout board', caption: 'A home-grown CPU, toolchain, and browser programmer running in silicon.' },
    { type: 'youtube', src: 'https://www.youtube-nocookie.com/embed/FRaOzFBtV3o', title: 'Original Logisim 8-bit Fibonacci demonstration', caption: 'The original Logisim computer runs an eight-digit Fibonacci program before the design moved to HDL and silicon.' }
  ],
  wallet: [
    { type: 'image', src: '/projects/wallet.jpg', alt: 'Printed mechanical wallet prototype', caption: 'A compact card wallet explored through several retention mechanisms.', wide: true },
    { type: 'model', src: '/models/wallet.glb', poster: '/projects/wallet.jpg', alt: 'Interactive mechanical wallet model', caption: 'Inspect the wallet body and mechanism.' }
  ],
  'onnxstream-sdxl': [],
  'seed-reversal': [
    { type: 'image', src: '/projects/pack.png', alt: 'The original Minecraft pack.png landscape', caption: 'The seed-reversal work starts from the most recognisable image in Minecraft.' }
  ],
  'advent-of-code': [],
  'ftl-models': [
    { type: 'model', src: '/models/ftl-kestrel.glb', poster: '/projects/ftl-kestrel-render.png', alt: 'Interactive FTL Kestrel model', caption: 'A printable Blender interpretation of the Kestrel.' },
    { type: 'model', src: '/models/ftl-rebel-flagship.glb', poster: '/projects/ftl-rebel-flagship-render.png', alt: 'Interactive FTL Rebel Flagship model', caption: 'The Rebel Flagship translated from game artwork into a printable model.' },
    { type: 'model', src: '/models/ftl-stealth-cruiser.glb', poster: '/projects/ftl-stealth-cruiser-render.png', alt: 'Interactive FTL Stealth Cruiser model', caption: 'The Stealth Cruiser recreated as a printable Blender model.' }
  ],
  'epaper-smart-watch': [
    { type: 'image', src: '/projects/epaper-watch-schematic.svg', alt: 'Complete e-paper smart watch schematic', caption: 'The current power, display, sensing, charging, USB, and wireless design on one schematic sheet.', wide: true },
    { type: 'image', src: '/projects/epaper-watch-front.jpg', alt: 'Earlier fabricated round e-paper smart watch PCB', caption: 'The dense component side of the earlier fabricated revision.' },
    { type: 'image', src: '/projects/epaper-watch-back.jpg', alt: 'Back of an earlier round e-paper smart watch PCB', caption: 'Display and programming connections on the earlier fabricated revision.' },
    { type: 'board', src: '/boards/epaper-smart-watch.kicad_pcb', title: 'E-paper smart watch', caption: 'Inspect the real watch PCB in KiCanvas.' }
  ]
};
