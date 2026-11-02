const rotationInterval = 9_000;
const listeners = new Set<() => void>();
let timer: ReturnType<typeof setInterval> | undefined;

function tick() {
  if (document.hidden) return;
  for (const listener of listeners) listener();
}

/**
 * Calls the listener on one shared tick, so that every image rotator on the
 * page swaps at the same time. Returns a function that removes the listener.
 */
export function onRotationTick(listener: () => void) {
  listeners.add(listener);
  timer ??= setInterval(tick, rotationInterval);

  return () => {
    listeners.delete(listener);
    if (listeners.size > 0 || timer === undefined) return;
    clearInterval(timer);
    timer = undefined;
  };
}
