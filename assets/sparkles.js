(() => {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function toRgb(color) {
    color = (color || '').trim();
    if (color.startsWith('#')) {
      const hex = color.replace('#','');
      const full = hex.length === 3 ? hex.split('').map(c => c + c).join('') : hex;
      const num = parseInt(full, 16);
      return [ (num >> 16) & 255, (num >> 8) & 255, num & 255 ];
    }
    const m = color.match(/rgba?KATEX_INLINE_OPEN(\d+)[,\s]+(\d+)[,\s]+(\d+)/i);
    if (m) return [ +m[1], +m[2], +m[3] ];
    // fallback cyan
    return [0, 188, 212];
  }

  function mix(colorA, colorB, amount = 0.5) {
    const a = toRgb(colorA), b = toRgb(colorB);
    const r = Math.round(a[0] + (b[0] - a[0]) * amount);
    const g = Math.round(a[1] + (b[1] - a[1]) * amount);
    const bl = Math.round(a[2] + (b[2] - a[2]) * amount);
    return `rgb(${r}, ${g}, ${bl})`;
  }

  function getAccent(el) {
    let scope = el.closest('.neon-container') || document.documentElement;
    const val = getComputedStyle(scope).getPropertyValue('--accent').trim();
    return val || '#00bcd4';
  }

  function spawnSparkles(btn, { count = 12, spread, colors } = {}) {
    if (prefersReduced.matches) return;

    const rect = btn.getBoundingClientRect();
    const accent = getAccent(btn);
    const palette = colors || [accent, mix(accent, '#ffffff', 0.25), mix(accent, '#ffffff', 0.55)];

    const baseCount = +btn.dataset.sparklesCount || count;
    const radius = +btn.dataset.sparklesSpread || spread || Math.max(rect.width, rect.height) * 0.7;
    const baseSize = parseFloat(btn.dataset.sparklesSize || '7'); // px

    for (let i = 0; i < baseCount; i++) {
      const s = document.createElement('span');
      s.className = 'sparkle' + (Math.random() < 0.38 ? ' star' : '');
      const angle = Math.random() * Math.PI * 2;
      const dist = radius * (0.45 + Math.random());      // push outward
      const dx = Math.cos(angle) * dist;
      const dy = Math.sin(angle) * dist * 0.85;          // slight ellipse for variety

      const size = baseSize * (0.7 + Math.random() * 0.9);
      const spd = 420 + Math.random() * 520;             // ms
      s.style.setProperty('--dx', dx.toFixed(2) + 'px');
      s.style.setProperty('--dy', dy.toFixed(2) + 'px');
      s.style.setProperty('--spd', spd.toFixed(0) + 'ms');
      s.style.width = s.style.height = size.toFixed(1) + 'px';
      s.style.color = palette[Math.floor(Math.random() * palette.length)];

      btn.appendChild(s);
      s.addEventListener('animationend', () => s.remove());
    }
  }

  // Emit once on hover, bigger burst on click/tap
  function onEnter(e) {
    const btn = e.target.closest('.neon-container .btn.sparkles');
    if (!btn) return;
    spawnSparkles(btn, { count: 10 });
  }
  function onClick(e) {
    const btn = e.target.closest('.neon-container .btn.sparkles');
    if (!btn) return;
    spawnSparkles(btn, { count: 18 });
  }

  document.addEventListener('mouseenter', onEnter, true);
  document.addEventListener('click', onClick, true);
  document.addEventListener('touchstart', onClick, { passive: true });
})();
