const state = {
  items: [], labels: {}, projects: [], index: 0, filter: 'crop-review', grid: false,
  saveTimer: null, carriedProject: '', crop: null, mediaSize: null
};

const $ = (selector) => document.querySelector(selector);
const mediaUrl = (name) => `/media/${encodeURIComponent(name)}`;
const current = () => state.items[state.index];
const labelFor = (name) => state.labels[name] || {};
const fullCrop = () => ({ left: 0, top: 0, right: 1, bottom: 1 });
const clamp = (value, minimum, maximum) => Math.max(minimum, Math.min(maximum, value));
const excludedByNote = (label) => /\b(ignore|dont use|do not use|bad image|bad video|not a great video|wouldn.t use)\b/i.test(`${label.caption || ''} ${label.notes || ''}`);
const isIncluded = (label) => Boolean(label.caption) && label.usage !== 'skip' && !excludedByNote(label);

async function load() {
  const data = await fetch('/api/items').then((response) => response.json());
  Object.assign(state, { items: data.items, labels: data.labels || {}, projects: data.projects });
  $('#source').textContent = data.sourceDir;
  $('#projects').innerHTML = data.projects.map((project) => `<option value="${escapeHtml(project)}"></option>`).join('');
  const first = filteredItems()[0];
  if (first) state.index = state.items.findIndex((item) => item.name === first.name);
  render();
}

function normaliseCrop(crop) {
  if (!crop) return fullCrop();
  const left = clamp(Number(crop.left) || 0, 0, 0.99);
  const top = clamp(Number(crop.top) || 0, 0, 0.99);
  const right = clamp(Number(crop.right) || 1, left + 0.01, 1);
  const bottom = clamp(Number(crop.bottom) || 1, top + 0.01, 1);
  return { left, top, right, bottom };
}

function filteredItems() {
  return state.items.filter((item) => {
    const label = labelFor(item.name);
    if (state.filter === 'crop-review') return isIncluded(label) && !label.cropReviewed;
    if (state.filter === 'unlabelled') return !label.caption && !label.usage;
    if (state.filter === 'included') return isIncluded(label);
    if (state.filter === 'skip') return label.usage === 'skip';
    return true;
  });
}

function selectByName(name) {
  capture();
  const index = state.items.findIndex((item) => item.name === name);
  if (index >= 0) { state.index = index; state.grid = false; render(); }
}

function render() {
  const item = current();
  $('.workspace').hidden = state.grid;
  $('#contactSheet').hidden = !state.grid;
  const labels = Object.values(state.labels);
  const labelled = labels.filter((label) => label.caption || label.usage).length;
  const included = labels.filter(isIncluded).length;
  const cropReviewed = labels.filter((label) => isIncluded(label) && label.cropReviewed).length;
  const percent = included ? Math.round(cropReviewed / included * 100) : 0;
  $('#progressText').textContent = `${cropReviewed}/${included} crops reviewed · ${labelled}/${state.items.length} labelled`;
  $('#progressBar').style.width = `${percent}%`;
  $('#rail').innerHTML = filteredItems().map((entry) => {
    const label = labelFor(entry.name);
    const status = label.usage === 'skip' ? 'skip' : label.cropReviewed ? 'crop-ok' : label.usage ? 'labelled' : '';
    const thumb = entry.kind === 'image'
      ? `<img loading="lazy" src="${mediaUrl(entry.name)}" alt="" />`
      : '<span class="video-thumb">▶</span>';
    return `<button class="rail-item ${entry.name === item?.name ? 'active' : ''}" data-name="${escapeHtml(entry.name)}">${thumb}<span><strong>${escapeHtml(entry.name)}</strong><small>${escapeHtml(label.project || entry.kind)}</small></span><i class="${status}"></i></button>`;
  }).join('');
  $('#rail').querySelectorAll('[data-name]').forEach((button) => button.addEventListener('click', () => selectByName(button.dataset.name)));
  if (!item) {
    $('#mediaFrame').innerHTML = '<p class="empty-state">No media matches this filter.</p>';
    $('#videoControls').hidden = true;
    return;
  }

  const label = labelFor(item.name);
  state.crop = normaliseCrop(label.crop);
  state.mediaSize = null;
  $('#filename').textContent = item.name;
  $('#fileMeta').textContent = `${item.kind} · ${formatBytes(item.size)} · ${state.index + 1} of ${state.items.length}${label.cropReviewed ? ' · crop reviewed' : ''}`;
  $('#project').value = label.project || ($('#carry').checked ? state.carriedProject : '');
  $('#usage').value = label.usage || '';
  $('#caption').value = label.caption || '';
  $('#notes').value = label.notes || '';
  renderMedia(item);
  renderContactSheet();
  document.querySelector(`[data-name="${CSS.escape(item.name)}"]`)?.scrollIntoView({ block: 'nearest' });
}

function renderMedia(item) {
  const source = mediaUrl(item.name);
  const media = item.kind === 'image'
    ? `<img id="cropMedia" src="${source}" alt="Current media" />`
    : `<video id="cropMedia" src="${source}" controls muted playsinline preload="metadata"></video>`;
  $('#mediaFrame').innerHTML = `${media}<div id="cropBox" class="crop-box" tabindex="0" aria-label="Crop selection"><i data-handle="nw"></i><i data-handle="ne"></i><i data-handle="se"></i><i data-handle="sw"></i></div>`;
  const element = $('#cropMedia');
  const ready = () => {
    const width = item.kind === 'image' ? element.naturalWidth : element.videoWidth;
    const height = item.kind === 'image' ? element.naturalHeight : element.videoHeight;
    if (!width || !height) return;
    state.mediaSize = { width, height };
    fitMediaFrame();
    enforceSelectedAspect();
    installCropDrag();
    setupVideoControls(item, element);
  };
  element.addEventListener(item.kind === 'image' ? 'load' : 'loadedmetadata', ready, { once: true });
  if ((item.kind === 'image' && element.complete) || (item.kind === 'video' && element.readyState >= 1)) ready();
}

function setupVideoControls(item, element) {
  const controls = $('#videoControls');
  controls.hidden = item.kind !== 'video';
  if (item.kind !== 'video') return;
  const scrub = $('#videoScrub');
  scrub.max = String(element.duration || 1);
  scrub.value = String(element.currentTime || 0);
  const updateTime = () => {
    scrub.value = String(element.currentTime);
    $('#videoTime').textContent = `${formatTime(element.currentTime)} / ${formatTime(element.duration)}`;
    $('#playPause').textContent = element.paused ? 'Play' : 'Pause';
    const previewVideo = $('#cropPreview video');
    if (previewVideo?.readyState >= 1 && Number.isFinite(element.currentTime)) previewVideo.currentTime = element.currentTime;
  };
  element.addEventListener('timeupdate', updateTime);
  element.addEventListener('play', updateTime);
  element.addEventListener('pause', updateTime);
  updateTime();
}

function fitMediaFrame() {
  if (!state.mediaSize) return;
  const area = $('#mediaArea').getBoundingClientRect();
  const scale = Math.min((area.width - 28) / state.mediaSize.width, (area.height - 28) / state.mediaSize.height);
  const frame = $('#mediaFrame');
  frame.style.width = `${Math.max(1, state.mediaSize.width * scale)}px`;
  frame.style.height = `${Math.max(1, state.mediaSize.height * scale)}px`;
}

function cropValues() {
  return {
    x: state.crop.left,
    y: state.crop.top,
    width: state.crop.right - state.crop.left,
    height: state.crop.bottom - state.crop.top
  };
}

function setCrop({ x, y, width, height }) {
  width = clamp(width, 0.01, 1);
  height = clamp(height, 0.01, 1);
  x = clamp(x, 0, 1 - width);
  y = clamp(y, 0, 1 - height);
  state.crop = { left: x, top: y, right: x + width, bottom: y + height };
  updateCropUi();
}

function lockedNormalisedAspect() {
  const value = $('#cropAspect').value;
  if (!state.mediaSize || value === 'free') return null;
  return Number(value) / (state.mediaSize.width / state.mediaSize.height);
}

function enforceSelectedAspect() {
  const ratio = lockedNormalisedAspect();
  if (!ratio) return updateCropUi();
  const crop = cropValues();
  let width = crop.width;
  let height = width / ratio;
  if (height > crop.height) {
    height = crop.height;
    width = height * ratio;
  }
  const centerX = crop.x + crop.width / 2;
  const centerY = crop.y + crop.height / 2;
  setCrop({ x: centerX - width / 2, y: centerY - height / 2, width, height });
}

function lockResizeToAspect(start, handle, width, height, useWidth) {
  const ratio = lockedNormalisedAspect();
  if (!ratio) return { x: start.x, y: start.y, width, height };

  if (useWidth) height = width / ratio;
  else width = height * ratio;

  const fixedRight = start.x + start.width;
  const fixedBottom = start.y + start.height;
  let x = handle.includes('w') ? fixedRight - width : start.x;
  let y = handle.includes('n') ? fixedBottom - height : start.y;
  const maxWidth = handle.includes('w') ? fixedRight : 1 - start.x;
  const maxHeight = handle.includes('n') ? fixedBottom : 1 - start.y;
  const scale = Math.min(1, maxWidth / width, maxHeight / height);
  width *= scale;
  height *= scale;
  x = handle.includes('w') ? fixedRight - width : start.x;
  y = handle.includes('n') ? fixedBottom - height : start.y;
  return { x, y, width, height };
}

function updateCropUi() {
  if (!state.crop || !state.mediaSize) return;
  const crop = cropValues();
  const box = $('#cropBox');
  box.style.left = `${crop.x * 100}%`;
  box.style.top = `${crop.y * 100}%`;
  box.style.width = `${crop.width * 100}%`;
  box.style.height = `${crop.height * 100}%`;
  $('#cropX').value = (crop.x * 100).toFixed(1);
  $('#cropX').max = ((1 - crop.width) * 100).toFixed(1);
  $('#cropY').value = (crop.y * 100).toFixed(1);
  $('#cropY').max = ((1 - crop.height) * 100).toFixed(1);
  $('#cropWidth').value = (crop.width * 100).toFixed(1);
  $('#cropWidth').max = ((1 - crop.x) * 100).toFixed(1);
  $('#cropHeight').value = (crop.height * 100).toFixed(1);
  $('#cropHeight').max = ((1 - crop.y) * 100).toFixed(1);

  const outputWidth = Math.round(state.mediaSize.width * crop.width);
  const outputHeight = Math.round(state.mediaSize.height * crop.height);
  $('#cropReadout').textContent = `${outputWidth} × ${outputHeight} · ${Math.round(crop.x * 100)}%, ${Math.round(crop.y * 100)}%`;
  renderCropPreview(crop);
}

function renderCropPreview(crop) {
  const item = current();
  const preview = $('#cropPreview');
  const outputAspect = state.mediaSize.width * crop.width / (state.mediaSize.height * crop.height);
  preview.style.aspectRatio = String(outputAspect);
  const source = mediaUrl(item.name);
  if (preview.dataset.name !== item.name) {
    const visual = item.kind === 'image'
      ? `<img src="${source}" alt="Crop preview" />`
      : `<video src="${source}" muted playsinline preload="metadata"></video>`;
    preview.innerHTML = visual;
    preview.dataset.name = item.name;
  }
  const element = preview.firstElementChild;
  element.style.width = `${100 / crop.width}%`;
  element.style.height = `${100 / crop.height}%`;
  element.style.left = `${-crop.x / crop.width * 100}%`;
  element.style.top = `${-crop.y / crop.height * 100}%`;
}

function installCropDrag() {
  const box = $('#cropBox');
  if (box.dataset.ready) return;
  box.dataset.ready = 'true';
  box.addEventListener('pointerdown', (event) => {
    event.preventDefault();
    const frame = $('#mediaFrame');
    const start = cropValues();
    const handle = event.target.dataset.handle || 'move';
    const origin = { x: event.clientX, y: event.clientY };
    box.setPointerCapture(event.pointerId);

    const move = (nextEvent) => {
      const dx = (nextEvent.clientX - origin.x) / frame.clientWidth;
      const dy = (nextEvent.clientY - origin.y) / frame.clientHeight;
      if (handle === 'move') return setCrop({ ...start, x: start.x + dx, y: start.y + dy });
      let { x, y, width, height } = start;
      if (handle.includes('e')) width += dx;
      if (handle.includes('s')) height += dy;
      if (handle.includes('w')) { x += dx; width -= dx; }
      if (handle.includes('n')) { y += dy; height -= dy; }
      if (width < 0.01) { if (handle.includes('w')) x = start.x + start.width - 0.01; width = 0.01; }
      if (height < 0.01) { if (handle.includes('n')) y = start.y + start.height - 0.01; height = 0.01; }
      const useWidth = Math.abs(nextEvent.clientX - origin.x) >= Math.abs(nextEvent.clientY - origin.y);
      setCrop(lockedNormalisedAspect() ? lockResizeToAspect(start, handle, width, height, useWidth) : { x, y, width, height });
    };
    const finish = () => {
      box.removeEventListener('pointermove', move);
      box.removeEventListener('pointerup', finish);
      box.removeEventListener('pointercancel', finish);
      capture();
    };
    box.addEventListener('pointermove', move);
    box.addEventListener('pointerup', finish);
    box.addEventListener('pointercancel', finish);
  });
}

function applyAspect(value) {
  if (!state.mediaSize || value === 'free') return;
  const desired = Number(value);
  const mediaAspect = state.mediaSize.width / state.mediaSize.height;
  let width = 1;
  let height = mediaAspect / desired;
  if (height > 1) { height = 1; width = desired / mediaAspect; }
  const currentCrop = cropValues();
  const centerX = currentCrop.x + currentCrop.width / 2;
  const centerY = currentCrop.y + currentCrop.height / 2;
  setCrop({ x: centerX - width / 2, y: centerY - height / 2, width, height });
  capture();
}

function renderContactSheet() {
  $('#contactSheet').hidden = !state.grid;
  $('.workspace').hidden = state.grid;
  if (!state.grid) return;
  $('#contactSheet').innerHTML = filteredItems().map((item) => {
    const label = labelFor(item.name);
    const status = label.usage === 'skip' ? 'skip' : label.cropReviewed ? 'crop-ok' : label.usage ? 'labelled' : '';
    const visual = item.kind === 'image' ? `<img loading="lazy" src="${mediaUrl(item.name)}" alt="" />` : '<div class="video-thumb">▶</div>';
    return `<button class="contact-card ${status}" data-contact="${escapeHtml(item.name)}">${visual}<span>${escapeHtml(item.name)}${label.project ? ` · ${escapeHtml(label.project)}` : ''}</span></button>`;
  }).join('');
  $('#contactSheet').querySelectorAll('[data-contact]').forEach((button) => button.addEventListener('click', () => selectByName(button.dataset.contact)));
}

function capture(cropReviewed) {
  const item = current(); if (!item) return;
  const project = $('#project').value.trim();
  const previous = labelFor(item.name);
  state.labels[item.name] = {
    ...previous,
    project,
    usage: $('#usage').value,
    caption: $('#caption').value.trim(),
    notes: $('#notes').value.trim(),
    kind: item.kind,
    crop: normaliseCrop(state.crop),
    cropReviewed: cropReviewed ?? previous.cropReviewed ?? false
  };
  if ($('#carry').checked && project) state.carriedProject = project;
  scheduleSave();
}

function scheduleSave() {
  $('#saveState').textContent = 'Saving';
  clearTimeout(state.saveTimer);
  state.saveTimer = setTimeout(async () => {
    const response = await fetch('/api/labels', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ labels: state.labels })
    });
    $('#saveState').textContent = response.ok ? 'Saved' : 'Error';
  }, 180);
}

function move(amount) {
  capture();
  state.index = Math.max(0, Math.min(state.items.length - 1, state.index + amount));
  render();
}

function finishCrop(useFullFrame = false) {
  const oldIndex = state.index;
  if (useFullFrame) state.crop = fullCrop();
  capture(true);
  const queue = filteredItems();
  const next = queue.find((item) => state.items.findIndex((entry) => entry.name === item.name) > oldIndex) || queue[0];
  state.index = next ? state.items.findIndex((item) => item.name === next.name) : -1;
  render();
}

$('#labelForm').addEventListener('submit', (event) => { event.preventDefault(); move(1); });
$('#previous').addEventListener('click', () => move(-1));
$('#next').addEventListener('click', () => move(1));
$('#filter').addEventListener('change', (event) => {
  capture();
  state.filter = event.target.value;
  const first = filteredItems()[0];
  if (first) state.index = state.items.findIndex((item) => item.name === first.name);
  render();
});
$('#gridToggle').addEventListener('click', () => { state.grid = !state.grid; $('#gridToggle').textContent = state.grid ? 'Focused view' : 'Contact sheet'; render(); });
$('#cropAspect').addEventListener('change', (event) => applyAspect(event.target.value));
$('#fullFrame').addEventListener('click', () => finishCrop(true));
$('#saveCrop').addEventListener('click', () => finishCrop(false));
$('#playPause').addEventListener('click', () => {
  const video = $('#cropMedia');
  if (!(video instanceof HTMLVideoElement)) return;
  if (video.paused) video.play(); else video.pause();
});
$('#videoScrub').addEventListener('input', (event) => {
  const video = $('#cropMedia');
  if (video instanceof HTMLVideoElement) video.currentTime = Number(event.target.value);
});
for (const field of ['project', 'usage', 'caption', 'notes']) $(`#${field}`).addEventListener('change', () => capture());
for (const field of ['cropX', 'cropY', 'cropWidth', 'cropHeight']) {
  $(`#${field}`).addEventListener('input', () => {
    const crop = cropValues();
    let nextCrop = {
      x: Number($('#cropX').value) / 100,
      y: Number($('#cropY').value) / 100,
      width: Number($('#cropWidth').value) / 100,
      height: Number($('#cropHeight').value) / 100
    };
    const ratio = lockedNormalisedAspect();
    if (ratio && field === 'cropWidth') nextCrop.height = nextCrop.width / ratio;
    if (ratio && field === 'cropHeight') nextCrop.width = nextCrop.height * ratio;
    setCrop(nextCrop);
  });
  $(`#${field}`).addEventListener('change', () => capture());
}

window.addEventListener('resize', fitMediaFrame);
window.addEventListener('keydown', (event) => {
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
  const shortcuts = { '1': 'hero', '2': 'showcase', '3': 'drawer', '4': 'texture', '5': 'reference', '0': 'skip' };
  if (shortcuts[event.key]) { $('#usage').value = shortcuts[event.key]; capture(); move(1); event.preventDefault(); }
  if (event.key === 'ArrowRight') { move(1); event.preventDefault(); }
  if (event.key === 'ArrowLeft') { move(-1); event.preventDefault(); }
});

function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB']; let value = bytes; let unit = 0;
  while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit++; }
  return `${value.toFixed(unit ? 1 : 0)} ${units[unit]}`;
}

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return '0:00';
  const minutes = Math.floor(seconds / 60);
  return `${minutes}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[character]);
}

load();
