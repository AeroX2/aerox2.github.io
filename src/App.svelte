<script lang="ts">
  import ProjectShowcaseDialog from './ProjectShowcaseDialog.svelte';
  import ProjectImageRotator from './ProjectImageRotator.svelte';
  import CertificateDialog from './CertificateDialog.svelte';
  import { showcaseMedia } from './showcaseMedia';
  import { generatedShowcaseMedia } from './generatedShowcaseMedia';
  import nullifyLogo from './assets/nullify.svg';
  import canvaLogo from './assets/canva.svg';
  import googleLogo from './assets/google.svg';
  import thoughtDesignLogo from './assets/thoughtdesign.png';
  import firstLogo from './assets/first.png';

  type Project = {
    slug: string;
    title: string;
    eyebrow: string;
    category: string;
    status: string;
    image: string;
    imagePosition?: string;
    alt: string;
    summary: string;
    note: string;
    tags: string[];
    href?: string;
    hrefLabel?: string;
    storyPath?: string;
    links?: { label: string; href: string }[];
    credit?: { label: string; href: string };
    journeyEyebrow?: string;
    journeyTitle?: string;
    journey?: { label: string; title: string; description: string }[];
    rotation: string;
  };

  type Certificate = {
    title: string;
    src: string;
    alt: string;
  };

  const projects: Project[] = [
    {
      slug: 'jrb8',
      title: 'JRB8 computer',
      eyebrow: 'A computer, the long way around',
      category: 'Low-level',
      status: 'Working silicon',
      image: '/projects/jrb8-board-cover.webp',
      alt: 'The JRB8 computer running on a Tiny Tapeout demonstration board',
      summary:
        'An 8-bit computer designed in Logisim, ported to Verilog, and manufactured through Tiny Tapeout.',
      note:
        'This began in high school after NAND2Tetris: first a Logisim machine and hand-designed control words, then an assembler and real programs, HDL and FPGA experiments, and finally a manufactured TinyTapeout CPU with its own language and browser toolchain.',
      tags: ['Verilog', 'CPU design', 'Compilers'],
      href: 'https://github.com/AeroX2/tt06-jrb8-computer',
      links: [
        { label: 'Original Logisim computer', href: 'https://github.com/AeroX2/8-bit-computer' },
        { label: 'TinyTapeout JRB8', href: 'https://github.com/AeroX2/tt06-jrb8-computer' }
      ],
      journeyEyebrow: 'One idea, carried for years',
      journeyTitle: 'From gates to silicon',
      journey: [
        { label: 'High school', title: 'Learn the machine', description: 'Worked through NAND2Tetris and started treating a computer as something that could be understood gate by gate.' },
        { label: 'Logisim Evolution', title: 'Design an architecture', description: 'Built the CPU, instruction set, control ROM, ALU and jump behaviour; the exported tables map 256 eight-bit control rows and a later 998-row sixteen-bit instruction/control exploration.' },
        { label: 'Software', title: 'Make it programmable', description: 'Wrote an assembler and programs including Fibonacci, prime generation, memory tests and an eight-digit Fibonacci implementation.' },
        { label: 'HDL + FPGA', title: 'Leave the simulator', description: 'Moved the design into hardware-description languages, tested components, and used FPGA boards to validate the computer before fabrication.' },
        { label: 'TinyTapeout', title: 'Manufacture the idea', description: 'Ported JRB8 to silicon, added SPI program storage, a small JRP language, compiler, tests, and a WebSerial compile-flash-run tool.' }
      ],
      rotation: '-0.35deg'
    },
    {
      slug: 'led-display',
      title: 'LED clock',
      eyebrow: 'A clock that kept evolving',
      category: 'Hardware',
      status: 'Built / continuously revised',
      image: '/labeled-media/img_20230129_213119097.jpg',
      alt: 'A large HUB75 LED clock showing a colourful clock face',
      summary: 'A large networked HUB75 clock that grew from a bleeding low-resolution prototype into a polished clock, visualiser, and animation surface.',
      note: 'The hardware, ESP driver, web interface, enclosure, brightness behaviour, animations, and content all changed across several physical versions.',
      tags: ['ESP32', 'HUB75', 'Web UI'],
      journeyEyebrow: '2019–2026 / commit history',
      journeyTitle: 'From clock to canvas',
      journey: [
        { label: 'Sep 2019', title: 'Put time on the wall', description: 'The first commit was already a working NTP clock, followed immediately by a split between display code and animation code.' },
        { label: '2021', title: 'Build clock two', description: 'A second physical version added updated clock models and over-the-air firmware support.' },
        { label: 'Jan 2023', title: 'Modernise the firmware', description: 'The project moved to PlatformIO, adopted a newer matrix library, and restored time, colour, and remote debugging on the rebuilt display.' },
        { label: 'Mar–Jun 2025', title: 'Make version two physical', description: 'New enclosure models tightened the display fit while a 60 fps cap and ghosting fixes improved the panel itself.' },
        { label: '2025–2026', title: 'Treat it as a surface', description: 'Animations, web serving, fonts, transitions, time sync, and daylight-saving behaviour were separated and refined into the current clock.' }
      ],
      rotation: '0.2deg'
    },
    {
      slug: 'robodog',
      title: 'Robot dog',
      eyebrow: 'Four legs, many revisions',
      category: 'Hardware',
      status: 'In progress',
      image: '/labeled-media/img_20260708_141350321.jpg',
      imagePosition: '50% 50%',
      alt: 'The nearly complete blue and white robot dog with its aluminium frame assembled',
      summary:
        'A build of Paul Gould’s open-source 3D-printed BLDC quadruped, with my controller, wiring, aluminium frame, and adaptations.',
      note:
        'The mechanical model and original quadruped design are Paul Gould’s. My work here is the physical build, controller electronics, wiring, aluminium structure, and the adaptations needed to bring it together.',
      tags: ['Robotics', 'CAD', 'BLDC'],
      href: 'https://github.com/AeroX2/robodog',
      links: [
        { label: 'My build repository', href: 'https://github.com/AeroX2/robodog' },
        { label: 'Original quadruped design', href: 'https://hackaday.io/project/184292-1000-3d-printed-bldc-quadruped-robot' }
      ],
      credit: {
        label: 'Original quadruped and 3D model by Paul Gould',
        href: 'https://hackaday.io/project/184292-1000-3d-printed-bldc-quadruped-robot'
      },
      storyPath: '/projects/robodog',
      journeyEyebrow: '2025–current / CAD + build history',
      journeyTitle: 'From open design to four legs',
      journey: [
        { label: 'Apr 2025', title: 'Start from the open design', description: 'The build began from Paul Gould’s open-source 3D-printed BLDC quadruped and its published mechanical model.' },
        { label: 'Rigging', title: 'Prepare it for simulation', description: 'The credited mechanical model moved into Phobos, where its body and leg parts became an articulated robot hierarchy.' },
        { label: 'Simulation', title: 'Add physical rules', description: 'Collision shapes, inertia, and bone links were corrected so the model behaved like hardware rather than loose meshes.' },
        { label: 'Jul 2025', title: 'Rework the rear leg', description: 'Back-leg geometry and exported meshes changed as the printed mechanism met real joint spacing and motion.' },
        { label: 'Current build', title: 'Assemble the aluminium body', description: 'Printed joints, brushless drives, wiring, and an aluminium spine turned the model into the current four-legged prototype.' }
      ],
      rotation: '0.25deg'
    },
    {
      slug: 'motor-controller',
      title: 'Custom motor controller',
      eyebrow: 'The nervous system for the dog',
      category: 'Hardware',
      status: 'Bench testing',
      image: '/projects/motor-controller.jpg',
      alt: 'A custom motor controller wired into a robot joint',
      summary:
        'A compact STM32-based BLDC servo controller with magnetic sensing, CAN-FD, and a custom bootloader path.',
      note:
        'The board is adapted for assembly-friendly parts and runs SimpleFOC. Firmware updates can travel over CAN-FD, which is much nicer than dismantling a leg for every flash.',
      tags: ['KiCad', 'STM32', 'CAN-FD'],
      href: 'https://github.com/AeroX2/moteus-controller',
      storyPath: '/projects/motor-controller',
      journeyEyebrow: '2023–2026 / commit history',
      journeyTitle: 'From schematic to networked servo',
      journey: [
        { label: 'Aug 2023', title: 'Draw the controller', description: 'The first board established the compact STM32 motor-control architecture and then pared back component cost.' },
        { label: '2024', title: 'Bring up power and CAN', description: 'Op-amps, undervoltage lockout, and thermistor circuits were fixed before CAN and the first motor rotation came alive.' },
        { label: 'Jul 2025', title: 'Close the current loop', description: 'Current sensing reached a working state, CAN-FD support landed, and a terminal interface made live motor control practical.' },
        { label: 'Feb–Apr 2026', title: 'Tune it like a servo', description: 'Moteus motors, current control, live PID commands, flash-backed settings, and startup alignment turned bring-up into repeatable control.' },
        { label: 'May 2026', title: 'Flash every leg over CAN', description: 'OpenBLT uploads, per-board identities, bus-off recovery, and target discovery completed the networked firmware path.' }
      ],
      rotation: '-0.2deg'
    },
    {
      slug: 'light-gun',
      title: 'Wireless light gun',
      eyebrow: 'IR tracking without the cable',
      category: 'Hardware',
      status: 'Working prototype',
      image: '/projects/light-gun-side.jpg',
      alt: 'A white, purple, and black custom wireless light gun',
      summary:
        'An OpenFIRE-based light gun with ESP-NOW, a dedicated wireless dongle, on-device display, and printed enclosure.',
      note:
        'The complete input path combines IR position tracking, filtering, calibration, buttons, force feedback, wireless transport, and USB HID output.',
      tags: ['ESP32', 'IR tracking', '3D printing'],
      href: 'https://github.com/AeroX2/OpenFIRE-Wireless',
      storyPath: '/projects/light-gun',
      journeyEyebrow: 'Aug 2025 / commit history',
      journeyTitle: 'From cable cut to arcade ready',
      journey: [
        { label: '8 Aug', title: 'Fork the wired foundation', description: 'The work began by translating and reshaping OpenFIRE until the wireless variant compiled.' },
        { label: '9 Aug', title: 'Connect the pedal', description: 'The pedal established the first radio link while the gun-side transport was still being brought up.' },
        { label: '15 Aug', title: 'Make the whole path work', description: 'Tracking, buttons, recoil data, ESP-NOW transport, and USB output finally operated as one wireless system.' },
        { label: '17 Aug', title: 'Add feedback and controls', description: 'The on-device display came online alongside trigger, docking-mode, and pause-to-hold fixes.' },
        { label: '21–25 Aug', title: 'Finish the arcade edges', description: 'Pedal handling, serial performance, MAMEHooker commands, and printable enclosure files completed the working prototype.' }
      ],
      rotation: '0.3deg'
    },
    {
      slug: 'epaper-smart-watch',
      title: 'E-paper smart watch',
      eyebrow: 'A low-power computer for the wrist',
      category: 'Hardware',
      status: 'In progress',
      image: '/projects/epaper-watch-front.jpg',
      alt: 'A compact round custom e-paper smart watch circuit board',
      summary:
        'A custom round smartwatch built around a 1.1-inch e-paper display, Bluetooth MCU, sensors, charging, and power management.',
      note:
        'The board compresses the display power supply, wireless MCU, flash, environmental sensing, motion sensing, battery monitoring, charging, buttons, and USB into a wearable round layout.',
      tags: ['KiCad', 'E-paper', 'Embedded'],
      href: 'https://github.com/AeroX2/epaper-smart-watch',
      journeyEyebrow: '2024–2026 / commit history',
      journeyTitle: 'Shrinking a computer onto a wrist',
      journey: [
        { label: 'Nov 2024', title: 'Lay out the round board', description: 'The first PCB packed display power, controls, charging, sensors, and the wireless MCU into the watch outline.' },
        { label: 'Feb 2025', title: 'Prepare it for fabrication', description: 'The accelerometer changed, power traces thickened, button pulls were corrected, and the board was prepared for JLCPCB.' },
        { label: 'May 2025', title: 'Start the firmware', description: 'The first code established the embedded side of the project after the hardware design pass.' },
        { label: 'Jun 2026', title: 'Bring up the display', description: 'A driver for the ET011TJ1 e-paper panel landed with KiCad 9 migration notes and a consolidated respin ECO.' },
        { label: 'Jul 2026', title: 'Route version two', description: 'Several routing passes converted the respin into a fully routed board ready for verification.' }
      ],
      rotation: '-0.25deg'
    },
    {
      slug: 'single-key-keyboard',
      title: 'Single-key keyboard',
      eyebrow: 'Product scope: aggressively controlled',
      category: 'Oddities',
      status: 'Built',
      image: '/projects/single-key-keyboard.jpg',
      alt: 'Two tiny round purple circuit boards, one fitted with a blue keycap',
      summary:
        'A complete keyboard with one key, built around a tiny custom round circuit board.',
      note:
        'It solves the difficult “too many keys” problem while making every other keyboard problem considerably worse. The firmware is written in assembly.',
      tags: ['Assembly', 'PCB design', 'USB'],
      href: 'https://github.com/AeroX2/single-key-keyboard',
      journeyEyebrow: 'Aug–Sep 2023 / commit history',
      journeyTitle: 'One key, all the firmware',
      journey: [
        { label: '6 Aug', title: 'Design the tiny board', description: 'The project started with the round PCB and the deliberately excessive hardware required to support one key.' },
        { label: '24 Aug', title: 'Find a USB path', description: 'Bootloader experiments moved through megaTinyCore before settling on tinyAVR V-USB support.' },
        { label: '25 Aug', title: 'Become a keyboard', description: 'The firmware compiled against the correct board revision and the single key finally produced keyboard input.' },
        { label: '31 Aug', title: 'Work on two operating systems', description: 'A combined keyboard and serial device survived its second attempt and worked on both Linux and Windows.' },
        { label: 'Sep 2023', title: 'Leave Arduino behind', description: 'The final firmware moved to native code, added configurable strings and EEPROM storage, and squeezed in a longer keyboard string.' }
      ],
      rotation: '0.4deg'
    },
    {
      slug: 'brother-cart',
      title: 'Brother cartridge emulator',
      eyebrow: 'Reverse engineering, but make it embroidery',
      category: 'Reverse engineering',
      status: 'Open source',
      image: '/labeled-media/20220322_172518.jpg',
      alt: 'A Brother embroidery cartridge connected to a hand-wired Arduino Mega reader',
      summary:
        'A hardware and software investigation into the proprietary cartridges used by older Brother embroidery machines.',
      note:
        'The project decodes the cartridge format and emulates the original hardware. The practical result is loading custom designs without hunting down increasingly rare plastic cartridges.',
      tags: ['C++', 'Protocols', 'Embroidery'],
      href: 'https://github.com/AeroX2/brother-cart-emulator',
      journeyEyebrow: '2022–2024 / commit history',
      journeyTitle: 'From mystery cartridge to open format',
      journey: [
        { label: 'Jul 2022', title: 'Read the original cartridge', description: 'The first code and PlatformIO conversion turned the hand-wired reader into a repeatable way to inspect the proprietary storage.' },
        { label: 'Sep 2022', title: 'Build the replacement', description: 'The cartridge hardware was simplified by removing unnecessary diodes while retaining the interface the machine expected.' },
        { label: 'Nov 2022', title: 'Crack the software path', description: 'A Python cracking tool joined the hardware work so imported designs could be understood and prepared outside the machine.' },
        { label: 'Mar 2023', title: 'Document the patches', description: 'Patch behaviour and the surrounding reverse-engineering process were clarified so the method could be reproduced.' },
        { label: 'Aug–Oct 2024', title: 'Make the tooling robust', description: 'Community work added sanity checks, verbose diagnostics, multiple card sizes, command-line options, clearer offsets, and stronger error handling.' }
      ],
      rotation: '-0.3deg'
    },
    {
      slug: 'sand-table',
      title: 'Sand table',
      eyebrow: 'A coffee table that draws',
      category: 'Oddities',
      status: 'Paused',
      image: '/projects/sand-table.jpg',
      alt: 'A round glass coffee table with a drawing mechanism underneath',
      summary:
        'A kinetic coffee table that moves a hidden magnet to draw slow, geometric patterns through sand.',
      note:
        'The mechanism was built and moved, but reliability problems put the project on hold. The useful next chapter is diagnosing it rather than pretending it reached a polished ending.',
      tags: ['Motion control', '3D printing', 'Furniture'],
      href: 'https://github.com/AeroX2/sand-table',
      storyPath: '/projects/sand-table',
      journeyEyebrow: '2024–2025 / commit history',
      journeyTitle: 'From coffee table to drawing machine',
      journey: [
        { label: 'Jun 2024', title: 'Test the mechanism', description: 'The earliest model explored the basic motion layout and the motor-driven gear train beneath the glass.' },
        { label: 'Jul 2024', title: 'Move the design to FreeCAD', description: 'The mechanical work switched tools so dimensions, constraints, and revisions could be managed more deliberately.' },
        { label: 'Sep 2024', title: 'Converge on a layout', description: 'Successive updates narrowed the mechanism toward a design that could actually fit inside the table.' },
        { label: 'Apr 2025', title: 'Choose a single-arm SCARA', description: 'The drawing mechanism simplified to a single arm and gained the first committed control code.' },
        { label: 'May 2025', title: 'Build, learn, pause', description: 'Final model updates produced the physical prototype; motion worked, but reliability issues made the next step diagnosis rather than polish.' }
      ],
      rotation: '0.15deg'
    },
    {
      slug: 'moon-lamp',
      title: 'Moon lamp',
      eyebrow: 'The moon, now with firmware',
      category: 'Oddities',
      status: 'Built',
      image: '/projects/moon-lamp.jpg',
      alt: 'A large illuminated moon globe on a yellow custom stand',
      summary:
        'A large illuminated lunar globe on a custom printed stand, because ordinary lamps were apparently solved already.',
      note:
        'The finished object hides a less glamorous stack of lighting experiments, printed fixtures, cable routing, and several versions of the top mount.',
      tags: ['Lighting', 'Fabrication', 'ESP'],
      href: 'https://makerworld.com/en/models/1541080-moon-globe-holder-with-motor#profileId-1617374',
      hrefLabel: 'MakerWorld',
      links: [
        { label: 'MakerWorld model', href: 'https://makerworld.com/en/models/1541080-moon-globe-holder-with-motor#profileId-1617374' }
      ],
      journeyEyebrow: 'Physical revisions / build evidence',
      journeyTitle: 'Making the moon turn',
      journey: [
        { label: 'Lighting tests', title: 'Find the right glow', description: 'Early experiments balanced enough internal light for the lunar relief without turning the globe into a featureless white ball.' },
        { label: 'Globe print', title: 'Print the moon in one piece', description: 'The revised globe became a continuous thin-walled print so its surface texture could carry through the light.' },
        { label: 'Stand', title: 'Give it a physical base', description: 'A weighted printed stand established the height, cable route, and visual proportions of the finished lamp.' },
        { label: 'Drive', title: 'Hide the rotation mechanism', description: 'A printed bearing ring, motor, and lighting mount were packed directly beneath the removable globe.' },
        { label: 'Finished build', title: 'Let the moon orbit', description: 'The assembled lamp combined the illuminated globe, concealed wiring, and slow motor drive into the final rotating object.' }
      ],
      rotation: '-0.15deg'
    },
    {
      slug: 'epaper-frame',
      title: 'Ethereal ink frame',
      eyebrow: 'Generative art with a slow refresh rate',
      category: 'Oddities',
      status: 'Built',
      image: '/projects/epaper-frame.jpg',
      alt: 'A white e-paper picture frame showing generative science-fiction artwork',
      summary:
        'A framed e-paper display for generated artwork: quiet, persistent, and a little uncanny.',
      note:
        'The display turns the limitations of e-paper into the point. Images arrive slowly, remain without power, and feel more like prints than screens.',
      tags: ['E-paper', 'Generative art', 'Web'],
      href: 'https://github.com/AeroX2/ethereal-ink-frame',
      journeyEyebrow: 'Dec 2023–Feb 2024 / commit history',
      journeyTitle: 'From generated image to quiet print',
      journey: [
        { label: '17 Dec', title: 'Start the image service', description: 'The first backend established the path from a generated image to something the frame could consume.' },
        { label: '19 Dec', title: 'Build the controls', description: 'The web interface took shape while test images exposed the practical limits of the display pipeline.' },
        { label: '21 Dec', title: 'Make images e-paper ready', description: 'Dithering, paths, image browsing, forms, and BMP output were wired into one working flow.' },
        { label: '22 Dec', title: 'Close the loop', description: 'The first complete version connected the interface, processing, storage, and frame output end to end.' },
        { label: 'Jan–Feb 2024', title: 'Refine the character', description: 'Cleaner data handling and a better dither algorithm shifted the result from a screen preview toward something that reads like a print.' }
      ],
      rotation: '0.35deg'
    }
  ];

  const archive = [
    {
      title: 'Nintendo DS repair',
      description: 'Hot-air connector replacement followed by a full screen, touch, and audio test.',
      href: 'https://github.com/AeroX2',
      tag: 'Repair',
      slug: 'nintendo-ds'
    },
    {
      title: 'Flare-On',
      description: 'Four years of reverse-engineering challenges, suspicious binaries, and physical medals.',
      href: 'https://flare-on.com/',
      tag: 'Reverse engineering',
      slug: 'flare-on'
    },
    {
      title: 'OnnxStream / SDXL',
      description: 'Contributed Stable Diffusion XL and SDXL Turbo support to a tiny inference engine that runs on a Raspberry Pi Zero 2.',
      href: 'https://github.com/vitoplantamura/OnnxStream',
      tag: 'C++ + ML',
      slug: 'onnxstream-sdxl'
    },
    {
      title: 'Seed reversal GPU optimization',
      description: 'Split seed and tree computation into separate CUDA kernels, more than doubling performance and making the search practical.',
      href: 'https://github.com/pack-png-mods/seed-reversal-gpu/pull/10',
      tag: 'CUDA',
      slug: 'seed-reversal'
    },
    {
      title: 'Advent of Code',
      description: 'Several years of puzzle solving across Python, Kotlin, Go, and Nim.',
      href: 'https://github.com/AeroX2?tab=repositories&q=advent-of-code',
      tag: '2019—2024',
      slug: 'advent-of-code'
    },
    {
      title: 'FTL ship models',
      description: 'Printable Blender models of the Kestrel, Rebel Flagship, and Stealth Cruiser from FTL.',
      href: 'https://github.com/AeroX2/ftl-models',
      tag: 'Blender',
      slug: 'ftl-models'
    },
    {
      title: 'Mechanical wallet',
      description: 'A compact printed card wallet explored through several sliding and retention mechanisms.',
      href: 'https://github.com/AeroX2/wallet',
      tag: 'FreeCAD',
      slug: 'wallet'
    },
    {
      title: 'Side quests',
      description: 'Internet-controlled blinds, reactive TV lighting, infrared photography, clocks, kitchen assistants, and assorted bench experiments.',
      href: 'https://github.com/AeroX2',
      tag: 'Assorted',
      slug: 'side-quests'
    }
  ];

  const drawerProjects: Record<string, Project> = {
    'nintendo-ds': {
      slug: 'nintendo-ds', title: 'Nintendo DS repair', eyebrow: 'Hot air and very small connectors', category: 'Hardware', status: 'Repaired',
      image: '/labeled-media/img_20250910_104542261.jpg', alt: 'An opened Nintendo DS during repair', summary: 'A broken display connector replaced with hot air and careful board work.',
      note: 'The final test exercised both displays, touch input, buttons, and audio—the useful proof that the repair was more than a neat solder joint.', tags: ['Repair', 'Hot air', 'Diagnostics'], rotation: '0deg'
    },
    'flare-on': {
      slug: 'flare-on', title: 'Flare-On', eyebrow: 'Four years of suspicious binaries', category: 'Reverse engineering', status: '4× finisher',
      image: '/labeled-media/img_20250205_194546494.jpg', alt: 'A Flare-On reverse engineering medal', summary: 'Annual reverse-engineering challenges spanning Windows internals, obfuscation, cryptography, virtual machines, and more.',
      note: 'The medals are the compact evidence; the interesting part is repeatedly learning unfamiliar systems quickly enough to finish every challenge.', tags: ['Reverse engineering', 'Security', 'Binary analysis'], href: 'https://flare-on.com/', rotation: '0deg'
    },
    'onnxstream-sdxl': {
      slug: 'onnxstream-sdxl', title: 'OnnxStream / SDXL', eyebrow: 'Large models, tiny memory budget', category: 'Low-level', status: 'Open-source contribution',
      image: '/projects/epaper-frame.jpg', alt: 'A compact generative-art display', summary: 'SDXL and SDXL Turbo running through a deliberately small, stream-oriented C++ inference engine.',
      note: 'I contributed SDXL Turbo support to OnnxStream. The project keeps memory use low enough for Stable Diffusion XL to run on a Raspberry Pi Zero 2 by streaming model weights and carefully controlling intermediate tensors.', tags: ['C++', 'ONNX', 'SDXL', 'Raspberry Pi'], href: 'https://github.com/vitoplantamura/OnnxStream',
      links: [
        { label: 'Upstream repository', href: 'https://github.com/vitoplantamura/OnnxStream' },
        { label: 'SDXL Turbo pull request', href: 'https://github.com/vitoplantamura/OnnxStream/pull/46' },
        { label: 'My fork', href: 'https://github.com/AeroX2/OnnxStream' }
      ], rotation: '0deg'
    },
    'seed-reversal': {
      slug: 'seed-reversal', title: 'Seed reversal GPU optimization', eyebrow: 'Searching Minecraft terrain backwards', category: 'Low-level', status: 'Merged contribution',
      image: '/projects/pack.png', alt: 'The original Minecraft pack.png landscape', summary: 'CUDA work that made a large Minecraft seed search practical instead of merely possible.',
      note: 'The optimization separated seed filtering from tree-position work so each CUDA kernel could do a narrower job. That more than doubled throughput and cut enough wasted computation to make the full search useful.', tags: ['CUDA', 'GPU compute', 'Reverse engineering'], href: 'https://github.com/pack-png-mods/seed-reversal-gpu/pull/10',
      links: [
        { label: 'My fork', href: 'https://github.com/AeroX2/seed-reversal-gpu' },
        { label: 'Merged pull request', href: 'https://github.com/pack-png-mods/seed-reversal-gpu/pull/10' }
      ], rotation: '0deg'
    },
    'advent-of-code': {
      slug: 'advent-of-code', title: 'Advent of Code', eyebrow: 'December, repeatedly', category: 'Low-level', status: '2019—2024',
      image: '/projects/jrb8-still.jpg', alt: 'A home-built computer representing low-level puzzle work', summary: 'Several years of small, sharp programming puzzles across Python, Kotlin, Go, and Nim.',
      note: 'These are compact experiments in parsing, graph search, simulation, dynamic programming, and whatever odd constraint the day introduces. Changing languages keeps the annual routine useful as a way to learn rather than just race.', tags: ['Python', 'Kotlin', 'Go', 'Nim'], href: 'https://github.com/AeroX2/advent-of-code-2024',
      links: [
        { label: '2024', href: 'https://github.com/AeroX2/advent-of-code-2024' },
        { label: '2023', href: 'https://github.com/AeroX2/advent-of-code-2023' },
        { label: '2022', href: 'https://github.com/AeroX2/advent-of-code-2022' },
        { label: '2021', href: 'https://github.com/AeroX2/advent-of-code-2021' },
        { label: '2020', href: 'https://github.com/AeroX2/advent-of-code-2020' },
        { label: '2019', href: 'https://github.com/AeroX2/advent-of-code-2019' }
      ], rotation: '0deg'
    },
    'side-quests': {
      slug: 'side-quests', title: 'Side quests', eyebrow: 'The rest of the workbench', category: 'Oddities', status: 'Assorted',
      image: '/labeled-media/20211226_144000.jpg', alt: 'A workbench covered in electronics and tools', summary: 'Smaller builds, repairs, experiments, and ideas that do not need a dedicated project card to be worth showing.',
      note: 'This drawer includes internet-controlled blinds, reactive TV lighting, infrared photography, air-quality clocks, a mechanical segment clock, and kitchen-assistant experiments.', tags: ['Electronics', 'Fabrication', 'Curiosity'], rotation: '0deg'
    },
    'ftl-models': {
      slug: 'ftl-models', title: 'FTL ship models', eyebrow: 'Game art made physical', category: 'Oddities', status: 'Printable',
      image: '/projects/ftl-kestrel-render.png', alt: 'A rendered printable model of the Kestrel from FTL', summary: 'Printable Blender models of the Kestrel, Rebel Flagship, and Stealth Cruiser from FTL.',
      note: 'The models translate flat in-game ship artwork into objects that still read correctly from every angle.', tags: ['Blender', '3D printing', 'FTL'], href: 'https://github.com/AeroX2/ftl-models', rotation: '0deg'
    },
    wallet: {
      slug: 'wallet', title: 'Mechanical wallet', eyebrow: 'Pocket-sized mechanism study', category: 'Oddities', status: 'Prototype',
      image: '/projects/wallet.jpg', alt: 'A printed mechanical wallet', summary: 'A compact printed card wallet explored through several sliding and retention mechanisms.',
      note: 'This is the kind of small object where tenths of a millimetre, print direction, and the feel of one moving part become the whole project.', tags: ['FreeCAD', '3D printing', 'Mechanisms'], href: 'https://makerworld.com/en/models/1373651-slider-wallet-based-off-cascade-wallet',
      links: [
        { label: 'MakerWorld model', href: 'https://makerworld.com/en/models/1373651-slider-wallet-based-off-cascade-wallet' },
        { label: 'GitHub source', href: 'https://github.com/AeroX2/wallet' }
      ], rotation: '0deg'
    }
  };

  let selectedProject = $state<Project | null>(null);
  let selectedCertificate = $state<Certificate | null>(null);
  let openedProjects = $state<string[]>([]);
  const currentYear = new Date().getFullYear();
  const yearsBuilding = currentYear - 2013;
  const featuredProject = projects.find((project) => project.slug === 'robodog')!;
  const supportingProjects = ['motor-controller', 'epaper-smart-watch', 'led-display']
    .map((slug) => projects.find((project) => project.slug === slug))
    .filter((project): project is Project => Boolean(project));
  const featuredSlugs = new Set([featuredProject.slug, ...supportingProjects.map((project) => project.slug)]);
  const machineProjects = projects.filter((project) => !featuredSlugs.has(project.slug));

  function openShowcase(project: Project) {
    selectedProject = project;
    if (!openedProjects.includes(project.slug)) openedProjects = [...openedProjects, project.slug];
  }

  function projectMediaCount(slug: string) {
    return (showcaseMedia[slug]?.length || 0) + (generatedShowcaseMedia[slug]?.length || 0);
  }

  function projectImages(project: Project) {
    const media = [...(showcaseMedia[project.slug] || []), ...(generatedShowcaseMedia[project.slug] || [])];
    const candidates = [
      { src: project.image, alt: project.alt },
      ...media.flatMap((item) => {
        if (item.type === 'image') return [{ src: item.src, alt: item.alt }];
        if ('poster' in item && item.poster) return [{ src: item.poster, alt: 'alt' in item ? item.alt : project.alt }];
        return [];
      })
    ];
    return candidates.filter((image, index) => candidates.findIndex((candidate) => candidate.src === image.src) === index);
  }

</script>

<svelte:head>
  <title>James Ridey — software, silicon & strange machines</title>
  <meta
    name="description"
    content="James Ridey builds software, custom electronics, computers, robots, and strange machines."
  />
</svelte:head>

<header class="site-header">
  <a class="wordmark" href="#top" aria-label="James Ridey, back to top">
    <span>JR</span>
    <small>software / silicon / strange machines</small>
  </a>
  <nav aria-label="Primary navigation">
    <a href="#work">Work</a>
    <a href="#parts">Parts drawer</a>
    <a href="#experience">Experience</a>
    <a class="nav-exit" href="https://github.com/AeroX2" target="_blank" rel="noreferrer">
      GitHub ↗
    </a>
  </nav>
</header>

<main id="top">
  <section class="portfolio-hero" aria-labelledby="hero-title">
    <div class="hero-heading-row">
      <div class="hero-identity">
        <p class="kicker"><span></span> Software engineer / hardware tinkerer</p>
        <h1 id="hero-title"><span>James</span> Ridey<i>.</i></h1>
      </div>
      <aside class="hero-field-notes" aria-label="Career field notes">
        <header><span>JR / operating card</span><b>Currently building</b></header>
        <div class="field-note-record">
          <p><strong>{yearsBuilding} yrs</strong><span>building software + hardware</span></p>
          <p><strong>50 kg</strong><span>FRC competition robot</span></p>
          <p><strong>4×</strong><span>Flare-On finisher</span></p>
          <p><strong>1</strong><span>CPU in silicon</span></p>
        </div>
        <p class="field-note-history"><span>Work history</span><b>Nullify · Canva · Google ×2</b></p>
        <p class="field-note-history"><span>Current work</span><b>AI products · frontend architecture</b></p>
        <p class="field-note-history"><span>After hours</span><b>Robotics · silicon · fabrication</b></p>
      </aside>
    </div>
    <div class="hero-ledger">
      <p class="hero-intro">
        I build the AI features and frontend foundations behind <strong>Nullify’s</strong>
        product-security platform. After hours: processors, robots, circuit boards,
        reverse-engineering tools, and one moon lamp.
      </p>
    </div>
  </section>

  <div class="project-ticker" aria-hidden="true">
    <div class="ticker-track">
      <div class="ticker-group">
        <span>Robot dog · four legs assembled</span><span>JRB8 · silicon verified</span>
        <span>Light gun · wireless path working</span><span>E-paper watch · routing version two</span>
        <span>Moon lamp · orbit nominal</span>
      </div>
      <div class="ticker-group">
        <span>Robot dog · four legs assembled</span><span>JRB8 · silicon verified</span>
        <span>Light gun · wireless path working</span><span>E-paper watch · routing version two</span>
        <span>Moon lamp · orbit nominal</span>
      </div>
    </div>
  </div>

  <section class="featured-section" id="work" aria-labelledby="work-title">
    <div class="document-heading">
      <h2 id="work-title">On the bench right now</h2>
    </div>
    <div class="featured-layout">
      <button class="featured-project" type="button" onclick={() => openShowcase(featuredProject)}>
        <ProjectImageRotator images={projectImages(featuredProject)} alt={featuredProject.alt} position={featuredProject.imagePosition || '50% 50%'} variant="featured" />
        <span class="featured-status">In progress</span>
        <span class="featured-copy">
          <small>{featuredProject.eyebrow}</small>
          <strong>{featuredProject.title}</strong>
          <span>{featuredProject.summary}</span>
        </span>
      </button>
      <div class="supporting-projects">
        {#each supportingProjects as project (project.slug)}
          <button type="button" onclick={() => openShowcase(project)}>
            <ProjectImageRotator images={projectImages(project)} alt={project.alt} position={project.imagePosition || '50% 50%'} variant="supporting" />
            <span>
              <small>{project.status}</small>
              <strong>{project.title}</strong>
              <em>{project.summary}</em>
            </span>
          </button>
        {/each}
      </div>
    </div>
  </section>

  <section class="machine-index" aria-labelledby="machine-index-title">
    <div class="document-heading">
      <h2 id="machine-index-title">Machine index</h2>
      <p>Finished, unfinished, and technically alive</p>
    </div>
    <div class="machine-list">
      {#each machineProjects as project (project.slug)}
        <button type="button" onclick={() => openShowcase(project)} aria-label={`Open ${project.title} showcase`}>
          <span class="machine-copy">
            <strong>{project.title}</strong>
            <span>{project.summary}</span>
          </span>
          <ProjectImageRotator images={projectImages(project)} alt={project.alt} position={project.imagePosition || '50% 50%'} variant="machine" />
        </button>
      {/each}
    </div>
  </section>

  <section class="archive-section" id="parts" aria-labelledby="archive-title">
    <div class="document-heading archive-heading">
      <h2 id="archive-title">Parts drawer</h2>
      <p>Contributions / models / smaller experiments</p>
    </div>
    <div class="parts-cabinet">
      <div class="parts-bins">
        {#each archive as item, index (item.title)}
          {#if item.slug && drawerProjects[item.slug]}
          <button class={`parts-bin bin-${index + 1}`} class:opened={openedProjects.includes(item.slug)} type="button" onclick={() => openShowcase(drawerProjects[item.slug!])}>
            <span class="bin-code">{String(index + 1).padStart(2, '0')} / {item.tag}</span>
            {#if projectMediaCount(item.slug)}<span class="bin-media-count">{projectMediaCount(item.slug)} pieces</span>{/if}
            {#if projectImages(drawerProjects[item.slug]).length > 0 && !['seed-reversal', 'advent-of-code', 'onnxstream-sdxl'].includes(item.slug)}
              <ProjectImageRotator images={projectImages(drawerProjects[item.slug])} alt={drawerProjects[item.slug].alt} variant="drawer" />
            {:else if item.title === 'Seed reversal GPU optimization'}
              <figure class="drawer-visual pack-visual"><img src="/projects/pack.png" alt="The original Minecraft pack.png" /><figcaption>3257840388504953787</figcaption></figure>
            {:else if item.title === 'Advent of Code'}
              <pre class="drawer-visual ascii-visual" aria-label="Festive Advent of Code ASCII art">        *
       /o\
      /@*o\
     /o**@*\
    /_*_o_*_\
       ||
  2019 — 2024</pre>
            {:else if item.title === 'OnnxStream / SDXL'}
              <pre class="drawer-visual code-visual diff-visual" aria-label="Excerpt from the merged SDXL Turbo pull request"><span class="diff-file">PR #46 · src/sd.cpp</span>
<span class="diff-del">- int dim = sdxl_params ? 128 : 64;</span>
<span class="diff-add">+ int dim = turbo ? 64 : 128;</span>
<span class="diff-add">+ if (turbo) return denoised_cond;</span>
<span class="diff-del">- float delta = -999.f / (step - 1);</span>
<span class="diff-add">+ float delta = step &gt; 1 ? -999.f / (step - 1) : 0.f;</span></pre>
            {:else if item.title === 'E-paper smart watch'}
              <div class="bin-object board" aria-hidden="true"><i></i><i></i><i></i></div>
            {:else}
              <div class="bin-object type" aria-hidden="true">{item.title.slice(0, 2)}</div>
            {/if}
            <strong>{item.title}</strong>
            <p>{item.description}</p>
            <span class="bin-open">Inspect ↗</span>
          </button>
          {:else}
          <a class={`parts-bin bin-${index + 1}`} href={item.href} target="_blank" rel="noreferrer">
            <span class="bin-code">{String(index + 1).padStart(2, '0')} / {item.tag}</span>
            {#if item.title === 'Seed reversal GPU optimization'}
              <figure class="drawer-visual pack-visual"><img src="/projects/pack.png" alt="The original Minecraft pack.png" /><figcaption>3257840388504953787</figcaption></figure>
            {:else if item.title === 'Advent of Code'}
              <pre class="drawer-visual ascii-visual" aria-label="Festive Advent of Code ASCII art">        *
       /o\
      /@*o\
     /o**@*\
    /_*_o_*_\
       ||
  2019 — 2024</pre>
            {:else if item.title === 'OnnxStream / SDXL'}
              <pre class="drawer-visual code-visual diff-visual" aria-label="Excerpt from the merged SDXL Turbo pull request"><span class="diff-file">PR #46 · src/sd.cpp</span>
<span class="diff-del">- int dim = sdxl_params ? 128 : 64;</span>
<span class="diff-add">+ int dim = turbo ? 64 : 128;</span>
<span class="diff-add">+ if (turbo) return denoised_cond;</span>
<span class="diff-del">- float delta = -999.f / (step - 1);</span>
<span class="diff-add">+ float delta = step &gt; 1 ? -999.f / (step - 1) : 0.f;</span></pre>
            {:else}
              <div class="bin-object type" aria-hidden="true">{item.title.slice(0, 2)}</div>
            {/if}
            <strong>{item.title}</strong>
            <p>{item.description}</p>
            <span class="bin-open">Source ↗</span>
          </a>
          {/if}
        {/each}
      </div>
    </div>
  </section>

  <section class="experience-section" id="experience" aria-labelledby="experience-title">
    <div class="section-heading">
      <div>
        <p class="section-label">Work history / qualifications / recognition</p>
        <h2 id="experience-title">Experience + credentials</h2>
      </div>
      <p>The work, followed by the evidence.</p>
    </div>
    <div class="resume-record">
      <div class="experience-list">
        <article>
          <time>2025—now</time>
          <div class="company-name"><img src={nullifyLogo} alt="" /><h3>Nullify</h3></div>
          <p>Building AI product features and leading a ground-up rebuild of the frontend for Nullify's autonomous product-security platform.</p>
          <span>Software engineering / frontend architecture / AI</span>
        </article>
        <article>
          <time>2020—2025</time>
          <div class="company-name"><img src={canvaLogo} alt="" /><h3>Canva</h3></div>
          <p>Architected Magic Design's state layer and shipped it two weeks ahead of launch; also rebuilt marketplace filtering for 150M+ monthly users, prototyped internal knowledge search, and mentored engineers.</p>
          <span>Software engineering / AI products</span>
        </article>
        <article>
          <time>2017—2019</time>
          <div class="company-name"><img src={googleLogo} alt="" /><h3>Google</h3></div>
          <p>Built an internal Google Maps feedback tool, then ported Neighbourly to KaiOS/JioPhone within a 512 MB memory ceiling and wrote the team's first porting specification.</p>
          <span>Software engineering internships</span>
        </article>
        <article>
          <time>2014—2017</time>
          <div class="company-name"><img src={thoughtDesignLogo} alt="" /><h3>ThoughtDesign</h3></div>
          <p>Built ASP.NET MVC and Angular applications, then took ownership of Angular projects and their Protractor test infrastructure.</p>
          <span>Full-stack software engineering</span>
        </article>
        <article>
          <time>2013—2016</time>
          <div class="company-name"><img src={firstLogo} alt="" /><h3>FIRST Robotics</h3></div>
          <p>Led software for a 50 kg competition robot, built and tested under the traditional six-week deadline.</p>
          <span>Lead software developer</span>
        </article>
      </div>
      <aside class="credentials-panel" id="credentials" aria-label="Credentials and recognition">
        <div class="resume-subheading">
          <span>Selected evidence</span>
          <strong>Qualifications + recognition</strong>
        </div>
        <div class="credentials-grid">
          <article class="credential-card credential-featured credential-with-proof">
            <p class="credential-meta">PortSwigger / issued 2026 / valid to 2032</p>
            <h3>Burp Suite Certified Practitioner</h3>
            <p>Demonstrated practical web-security testing across attack-surface discovery, defensive bypasses, out-of-band techniques, and business-impact analysis.</p>
            <a
              class="credential-proof"
              href="/projects/burp-suite-certified-practitioner.png"
              aria-label="Open the Burp Suite Certified Practitioner certificate"
              onclick={(event) => {
                event.preventDefault();
                selectedCertificate = {
                  title: 'Burp Suite Certified Practitioner',
                  src: '/projects/burp-suite-certified-practitioner.png',
                  alt: 'Burp Suite Certified Practitioner certificate awarded to James Ridey'
                };
              }}
            >
              <img src="/projects/burp-suite-certified-practitioner.png" alt="Burp Suite Certified Practitioner certificate awarded to James Ridey" />
              <span>View certificate ↗</span>
            </a>
            <a href="https://portswigger.net/web-security/e/c/a2836e9325092f5f" target="_blank" rel="noreferrer">Verify credential ↗</a>
          </article>
          <article class="credential-card credential-with-proof">
            <p class="credential-meta">Reverse engineering / security</p>
            <h3>Flare-On + offensive IoT</h3>
            <p>Four-time Flare-On finisher, ranked 157th of more than 4,100 entrants in 2025. Completed DEF CON's three-day Offensive IoT Exploitation course in firmware and hardware reverse engineering.</p>
            <a
              class="credential-proof"
              href="/projects/offensive-iot-certificate.jpg"
              aria-label="Open the Offensive IoT Exploitation certificate"
              onclick={(event) => {
                event.preventDefault();
                selectedCertificate = {
                  title: 'Offensive IoT Exploitation',
                  src: '/projects/offensive-iot-certificate.jpg',
                  alt: 'DEF CON Offensive IoT Exploitation certificate awarded to James Ridey'
                };
              }}
            >
              <img src="/projects/offensive-iot-certificate-thumb.jpg" alt="DEF CON Offensive IoT Exploitation certificate awarded to James Ridey" />
              <span>View certificate ↗</span>
            </a>
          </article>
          <article class="credential-card">
            <p class="credential-meta">Macquarie University / 2016—2020</p>
            <h3>BEng (Honours), Software Design</h3>
            <p>Received the Head of Computing Award in five semesters for the highest academic mark in the cohort.</p>
          </article>
          <article class="credential-card">
            <p class="credential-meta">Competitions</p>
            <h3>Built and tested under pressure</h3>
            <p>Hack Mac first place, ASEAN–Australia Codeathon runner-up, and 17th of 108 teams nationally in CySCA.</p>
          </article>
        </div>
      </aside>
    </div>
  </section>

  <section class="contact-section" aria-labelledby="contact-title">
    <p class="section-label">End of document</p>
    <h2 id="contact-title">End of website. <span>Not of projects</span><i>.</i></h2>
    <p>Follow the builds, browse the half-finished experiments, or open an issue when I have wired something backwards.</p>
    <div class="contact-actions">
      <a class="button primary" href="https://github.com/AeroX2" target="_blank" rel="noreferrer">GitHub ↗</a>
      <a class="button secondary" href="https://linkedin.com/in/james-ridey" target="_blank" rel="noreferrer">LinkedIn ↗</a>
      <a class="button secondary" href="mailto:james@ridey.email">Email ↗</a>
    </div>
  </section>
</main>

<footer>
  <span>© {new Date().getFullYear()} James Ridey</span>
  <span>Designed in code. Tested on hardware. No robots were emotionally harmed.</span>
  <a href="#top">Back to top ↑</a>
</footer>

{#if selectedProject}
  <ProjectShowcaseDialog
    project={selectedProject}
    media={[
      ...(showcaseMedia[selectedProject.slug] || []),
      ...(generatedShowcaseMedia[selectedProject.slug] || []),
      ...(!showcaseMedia[selectedProject.slug] && !generatedShowcaseMedia[selectedProject.slug]
        ? [{ type: 'image' as const, src: selectedProject.image, alt: selectedProject.alt, caption: selectedProject.summary }]
        : [])
    ]}
    onclose={() => (selectedProject = null)}
  />
{/if}

{#if selectedCertificate}
  <CertificateDialog
    title={selectedCertificate.title}
    src={selectedCertificate.src}
    alt={selectedCertificate.alt}
    onclose={() => (selectedCertificate = null)}
  />
{/if}
