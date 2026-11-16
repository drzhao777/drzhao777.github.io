/* Runs before layout so a saved theme is applied before first paint. */
(() => {
  const root = document.documentElement;
  const modes = ['system', 'light', 'dark'];
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let mode = 'system';
  try { mode = localStorage.getItem('academic-theme') || mode; } catch {}
  if (!modes.includes(mode)) mode = 'system';
  function apply() {
    root.dataset.mode = mode;
    root.dataset.theme = mode === 'system' ? (media.matches ? 'dark' : 'light') : mode;
    const b = document.querySelector('.theme');
    if (b) {
      const msg = 'Theme: ' + mode + '. Switch to ' + modes[(modes.indexOf(mode)+1)%3];
      b.title = msg; b.setAttribute('aria-label',msg);
    }
  }
  apply();
  media.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', () => {
    // Directory links on GitHub Pages; explicit index files for an offline preview.
    if (location.protocol === 'file:') document.querySelectorAll('a[href]').forEach(a => {
      const href = a.getAttribute('href');
      if (!/^(?:[a-z]+:|\/\/)/i.test(href) && href.endsWith('/')) a.setAttribute('href', href + 'index.html');
    });
    const menu = document.querySelector('.menu'), nav = document.querySelector('.nav-links');
    function show(open) { nav.classList.toggle('open',open); menu.setAttribute('aria-expanded',String(open)); }
    menu.addEventListener('click', () => show(!nav.classList.contains('open')));
    document.addEventListener('keydown', e => {
      if(e.key === 'Escape' && nav.classList.contains('open')) { show(false); menu.focus(); }
    });
    document.querySelector('.theme').addEventListener('click', () => {
      mode = modes[(modes.indexOf(mode)+1)%3]; apply();
      try { localStorage.setItem('academic-theme',mode); } catch {}
    });
    apply();
    const bar = document.querySelector('.read-progress'), top = document.querySelector('.to-top');
    function progress() {
      const max = root.scrollHeight - innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.max(0, Math.min(1, scrollY/max)) : 0) + ')';
      top.hidden = scrollY < 350;
    }
    top.addEventListener('click', () => window.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));
    addEventListener('scroll', progress, {passive:true}); addEventListener('resize',progress);
    addEventListener('load',progress); progress();
  });
})();
