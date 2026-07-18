<script lang="ts">
  import { onDestroy, tick } from 'svelte';
  import type { Mesh, Object3D, Quaternion, Vector3 } from 'three';

  let {
    src,
    poster,
    alt,
    caption
  }: { src: string; poster?: string; alt: string; caption: string } = $props();

  type Joint = {
    id: string;
    label: string;
    min: number;
    max: number;
  };

  type Leg = {
    name: string;
    code: string;
    joints: Joint[];
  };

  const legs: Leg[] = [
    {
      name: 'Front left',
      code: 'FL',
      joints: [
        { id: 'front_left_top_leg_link_joint', label: 'Hip', min: -30, max: 90 },
        { id: 'front_left_mid_leg_link_joint', label: 'Knee', min: -90, max: 50 },
        { id: 'front_left_bot_leg_link_joint', label: 'Ankle', min: -60, max: 160 }
      ]
    },
    {
      name: 'Front right',
      code: 'FR',
      joints: [
        { id: 'front_right_top_leg_link_joint', label: 'Hip', min: -90, max: 30 },
        { id: 'front_right_mid_leg_link_joint', label: 'Knee', min: -50, max: 90 },
        { id: 'front_right_bot_leg_link_joint', label: 'Ankle', min: -160, max: 60 }
      ]
    },
    {
      name: 'Rear left',
      code: 'RL',
      joints: [
        { id: 'back_left_top_leg_link_joint', label: 'Hip', min: -30, max: 90 },
        { id: 'back_left_mid_leg_link_joint', label: 'Knee', min: -90, max: 50 },
        { id: 'back_left_bot_leg_link_joint', label: 'Ankle', min: -60, max: 160 }
      ]
    },
    {
      name: 'Rear right',
      code: 'RR',
      joints: [
        { id: 'back_right_top_leg_link_joint', label: 'Hip', min: -90, max: 30 },
        { id: 'back_right_mid_leg_link_joint', label: 'Knee', min: -50, max: 90 },
        { id: 'back_right_bot_leg_link_joint', label: 'Ankle', min: -160, max: 60 }
      ]
    }
  ];

  const initialAngles = Object.fromEntries(
    legs.flatMap((leg) => leg.joints.map((joint) => [joint.id, 0]))
  );

  let canvasMount: HTMLDivElement;
  let started = $state(false);
  let loading = $state(false);
  let ready = $state(false);
  let error = $state('');
  let angles = $state<Record<string, number>>({ ...initialAngles });
  let applyJointRotation: ((id: string, value: number) => void) | undefined;
  let disableAutoRotate: (() => void) | undefined;
  let cleanupViewer: (() => void) | undefined;

  function setJoint(id: string, value: number) {
    angles[id] = value;
    disableAutoRotate?.();
    applyJointRotation?.(id, value);
  }

  function resetPose() {
    for (const id of Object.keys(initialAngles)) {
      angles[id] = 0;
      applyJointRotation?.(id, 0);
    }
  }

  async function activate() {
    if (started) return;
    started = true;
    loading = true;
    await tick();

    try {
      const THREE = await import('three');
      const [{ GLTFLoader }, { OrbitControls }] = await Promise.all([
        import('three/examples/jsm/loaders/GLTFLoader.js'),
        import('three/examples/jsm/controls/OrbitControls.js')
      ]);

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(34, 1, 0.01, 100);
      camera.position.set(3.6, 2.35, 4.3);

      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.outputColorSpace = THREE.SRGBColorSpace;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.12;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFShadowMap;
      canvasMount.appendChild(renderer.domElement);

      scene.add(new THREE.HemisphereLight(0xf4f7ff, 0x263044, 2.1));
      const keyLight = new THREE.DirectionalLight(0xffffff, 3.5);
      keyLight.position.set(4, 6, 3);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.set(1024, 1024);
      scene.add(keyLight);

      const rimLight = new THREE.DirectionalLight(0x6d87ff, 2.2);
      rimLight.position.set(-4, 2, -4);
      scene.add(rimLight);

      const floor = new THREE.Mesh(
        new THREE.CircleGeometry(3.3, 64),
        new THREE.ShadowMaterial({ color: 0x151b2a, opacity: 0.18 })
      );
      floor.rotation.x = -Math.PI / 2;
      floor.receiveShadow = true;
      scene.add(floor);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.07;
      controls.target.set(0, 0.72, 0);
      controls.minDistance = 2.4;
      controls.maxDistance = 8;
      controls.autoRotate = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      controls.autoRotateSpeed = 0.65;
      disableAutoRotate = () => (controls.autoRotate = false);
      controls.addEventListener('start', disableAutoRotate);

      const gltf = await new GLTFLoader().loadAsync(src);
      const model = gltf.scene;
      model.traverse((child: Object3D) => {
        if ('isMesh' in child && child.isMesh) {
          const mesh = child as Mesh;
          mesh.castShadow = true;
          mesh.receiveShadow = true;
        }
      });

      let bounds = new THREE.Box3().setFromObject(model);
      const size = bounds.getSize(new THREE.Vector3());
      model.scale.setScalar(2.75 / Math.max(size.x, size.y, size.z));
      model.updateMatrixWorld(true);
      bounds = new THREE.Box3().setFromObject(model);
      const center = bounds.getCenter(new THREE.Vector3());
      model.position.x -= center.x;
      model.position.z -= center.z;
      model.position.y -= bounds.min.y;
      scene.add(model);

      const jointNodes = new Map<string, Object3D>();
      const baseRotations = new Map<string, Quaternion>();
      const jointAxes = new Map<string, Vector3>();
      for (const leg of legs) {
        for (const joint of leg.joints) {
          const node = model.getObjectByName(`control__${joint.id}`);
          if (!node) continue;
          jointNodes.set(joint.id, node);
          baseRotations.set(joint.id, node.quaternion.clone());

          // Blender exports the URDF's Z-up coordinates as glTF Y-up.
          // Convert the axis stored in the node extras instead of rotating
          // around Three.js local Z, which leaves every joint 90 degrees off.
          const [x, y, z] = Array.isArray(node.userData.joint_axis)
            ? node.userData.joint_axis
            : [0, 0, 1];
          jointAxes.set(joint.id, new THREE.Vector3(x, z, -y).normalize());
        }
      }

      const jointTurn = new THREE.Quaternion();
      applyJointRotation = (id, value) => {
        const node = jointNodes.get(id);
        const baseRotation = baseRotations.get(id);
        const jointAxis = jointAxes.get(id);
        if (!node || !baseRotation || !jointAxis) return;
        jointTurn.setFromAxisAngle(jointAxis, THREE.MathUtils.degToRad(value));
        node.quaternion.copy(baseRotation).multiply(jointTurn);
        node.updateMatrixWorld(true);
      };

      if (jointNodes.size !== 12) {
        throw new Error(`Expected 12 articulated joints, found ${jointNodes.size}.`);
      }

      const resize = () => {
        const width = canvasMount.clientWidth;
        const height = canvasMount.clientHeight;
        if (!width || !height) return;
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      };
      const resizeObserver = new ResizeObserver(resize);
      resizeObserver.observe(canvasMount);
      resize();

      let frame = 0;
      const render = () => {
        frame = requestAnimationFrame(render);
        controls.update();
        renderer.render(scene, camera);
      };
      render();

      cleanupViewer = () => {
        cancelAnimationFrame(frame);
        resizeObserver.disconnect();
        controls.removeEventListener('start', disableAutoRotate!);
        controls.dispose();
        renderer.dispose();
        renderer.domElement.remove();
      };
      loading = false;
      ready = true;
    } catch (reason) {
      console.error(reason);
      error = 'The articulated model could not be loaded.';
      loading = false;
    }
  }

  onDestroy(() => cleanupViewer?.());
</script>

<figure class="dog-viewer">
  <div class="viewer-stage">
    <div class="canvas-mount" bind:this={canvasMount} aria-label={ready ? alt : undefined}></div>
    {#if !started}
      <button class="viewer-poster" onclick={activate} aria-label={`Load articulated 3D model: ${alt}`}>
        {#if poster}<img src={poster} alt="" />{/if}
        <span><b>12-axis model</b> Load joint controls</span>
      </button>
    {:else if loading}
      <div class="viewer-status"><span></span>Assembling articulation…</div>
    {:else if error}
      <div class="viewer-status error">{error}</div>
    {:else}
      <div class="orbit-note">Drag to orbit · scroll to zoom</div>
    {/if}
  </div>

  {#if ready}
    <section class="joint-console" aria-label="Robot dog joint controls">
      <header>
        <div><span>Joint console</span><b>12 DOF</b></div>
        <button type="button" onclick={resetPose}>Zero all joints</button>
      </header>
      <div class="leg-grid">
        {#each legs as leg (leg.code)}
          <fieldset>
            <legend><b>{leg.code}</b><span>{leg.name}</span></legend>
            {#each leg.joints as joint (joint.id)}
              <label>
                <span>{joint.label}</span>
                <input
                  type="range"
                  min={joint.min}
                  max={joint.max}
                  step="1"
                  value={angles[joint.id]}
                  oninput={(event) => setJoint(joint.id, Number(event.currentTarget.value))}
                />
                <output>{angles[joint.id]}°</output>
              </label>
            {/each}
          </fieldset>
        {/each}
      </div>
    </section>
  {/if}

  <figcaption>
    <span>URDF articulation / drag to orbit</span>
    {caption}
  </figcaption>
</figure>

<style>
  .dog-viewer {
    margin: 0;
  }

  .viewer-stage {
    position: relative;
    height: clamp(430px, 55vw, 650px);
    overflow: hidden;
    border: 1px solid var(--ink);
    background:
      linear-gradient(rgba(48, 79, 211, 0.11) 1px, transparent 1px),
      linear-gradient(90deg, rgba(48, 79, 211, 0.11) 1px, transparent 1px),
      #e5e9ef;
    background-size: 28px 28px;
  }

  .canvas-mount,
  .canvas-mount :global(canvas) {
    display: block;
    width: 100%;
    height: 100%;
  }

  .viewer-poster {
    position: absolute;
    inset: 0;
    display: grid;
    width: 100%;
    padding: 0;
    overflow: hidden;
    border: 0;
    color: var(--paper-bright);
    background: var(--ink);
    cursor: pointer;
  }

  .viewer-poster img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.58) saturate(0.72);
    transition: filter 250ms ease, transform 350ms ease;
  }

  .viewer-poster:hover img {
    filter: brightness(0.68) saturate(0.9);
    transform: scale(1.015);
  }

  .viewer-poster span {
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 190px;
    padding: 14px 18px;
    border: 1px solid var(--paper-bright);
    background: rgba(21, 27, 42, 0.88);
    font-family: 'Recursive Variable', monospace;
    font-size: 10px;
    font-weight: 720;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    transform: translate(-50%, -50%);
  }

  .viewer-poster b {
    display: block;
    margin-bottom: 4px;
    color: var(--acid);
    font-size: 8px;
  }

  .viewer-status {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: var(--ink);
    font-family: 'Recursive Variable', monospace;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.07em;
    text-transform: uppercase;
  }

  .viewer-status span {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--orange);
    animation: pulse 900ms ease-in-out infinite alternate;
  }

  .viewer-status.error {
    color: var(--orange);
  }

  .orbit-note {
    position: absolute;
    right: 12px;
    bottom: 12px;
    padding: 7px 9px;
    color: var(--paper-bright);
    background: rgba(21, 27, 42, 0.8);
    font-family: 'Recursive Variable', monospace;
    font-size: 8px;
    font-weight: 720;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    pointer-events: none;
  }

  .joint-console {
    border: 1px solid var(--ink);
    border-top: 0;
    background: var(--ink);
    color: var(--paper-bright);
  }

  .joint-console > header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.25);
  }

  .joint-console header div {
    display: flex;
    align-items: center;
    gap: 9px;
  }

  .joint-console header span,
  .joint-console header b,
  .joint-console button,
  legend,
  label {
    font-family: 'Recursive Variable', monospace;
    font-variation-settings: 'MONO' 1;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .joint-console header span {
    font-size: 9px;
    font-weight: 780;
  }

  .joint-console header b {
    padding: 3px 5px;
    color: var(--ink);
    background: var(--acid);
    font-size: 7px;
  }

  .joint-console button {
    border: 0;
    color: var(--paper-bright);
    background: transparent;
    font-size: 8px;
    font-weight: 720;
    cursor: pointer;
  }

  .joint-console button:hover {
    color: var(--acid);
  }

  .leg-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  fieldset {
    min-width: 0;
    padding: 12px;
    border: 0;
  }

  fieldset:nth-child(even) {
    border-left: 1px solid rgba(255, 255, 255, 0.25);
  }

  fieldset:nth-child(n + 3) {
    border-top: 1px solid rgba(255, 255, 255, 0.25);
  }

  legend {
    display: flex;
    align-items: baseline;
    gap: 7px;
    width: 100%;
    margin-bottom: 8px;
    color: rgba(255, 255, 255, 0.62);
    font-size: 7px;
  }

  legend b {
    color: var(--orange);
    font-size: 10px;
  }

  label {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr) 38px;
    align-items: center;
    gap: 8px;
    min-height: 30px;
    font-size: 7px;
    font-weight: 650;
  }

  input[type='range'] {
    width: 100%;
    height: 2px;
    accent-color: var(--acid);
    cursor: ew-resize;
  }

  output {
    color: var(--acid);
    font-variant-numeric: tabular-nums;
    text-align: right;
  }

  figcaption {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    padding: 12px 0 0;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.4;
  }

  figcaption span {
    color: var(--blue-dark);
    font-family: 'Recursive Variable', monospace;
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  @keyframes pulse {
    to {
      opacity: 0.32;
      transform: scale(0.72);
    }
  }

  @media (max-width: 650px) {
    .viewer-stage {
      height: 390px;
    }

    .leg-grid {
      grid-template-columns: 1fr;
    }

    fieldset:nth-child(even) {
      border-left: 0;
    }

    fieldset + fieldset {
      border-top: 1px solid rgba(255, 255, 255, 0.25);
    }

    figcaption {
      display: block;
    }

    figcaption span {
      display: block;
      margin-bottom: 6px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .viewer-poster img,
    .viewer-status span {
      transition: none;
      animation: none;
    }
  }
</style>
