/* Product image tabs: no timers, telemetry, or extension emulation. */
document.querySelectorAll('[data-viewer]').forEach(viewer => {
  const tabs = [...viewer.querySelectorAll('[role="tab"]')];
  const select = tab => {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', event => {
      let next;
      const rtl = document.documentElement.dir === 'rtl';
      if (event.key === 'ArrowRight') next = index + (rtl ? -1 : 1);
      if (event.key === 'ArrowLeft') next = index + (rtl ? 1 : -1);
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      const target = tabs[(next + tabs.length) % tabs.length];
      select(target);
      target.focus();
    });
  });
  viewer.classList.add('is-ready');
});
