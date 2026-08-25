const focusableSelector = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])'
].join(',');

export function focusTrap(node: HTMLElement) {
  function handleKeydown(event: KeyboardEvent) {
    if (event.key !== 'Tab') return;

    const focusable = Array.from(node.querySelectorAll<HTMLElement>(focusableSelector)).filter(
      (element) => !element.hasAttribute('hidden') && element.getClientRects().length > 0
    );
    if (!focusable.length) {
      event.preventDefault();
      node.focus();
      return;
    }

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const current = document.activeElement;

    if (event.shiftKey && (current === first || !node.contains(current))) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && (current === last || !node.contains(current))) {
      event.preventDefault();
      first.focus();
    }
  }

  node.addEventListener('keydown', handleKeydown);
  return {
    destroy() {
      node.removeEventListener('keydown', handleKeydown);
    }
  };
}
