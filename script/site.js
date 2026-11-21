function enableShowcase(viewer) {
  const list = viewer.querySelector('.mode-list');
  const tabs = [...list.querySelectorAll('a')];
  const panels = tabs.map(tab => document.getElementById(tab.hash.slice(1)));
  list.setAttribute('role', 'tablist');
  list.setAttribute('aria-orientation', 'vertical');

  function select(index) {
    tabs.forEach((tab, i) => {
      const selected = i === index;
      tab.tabIndex = selected ? 0 : -1;
      tab.setAttribute('aria-selected', String(selected));
      panels[i].hidden = !selected;
    });
  }
  tabs.forEach((tab, index) => {
    const panel = panels[index];
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panel.id);
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', tab.id);
    panel.tabIndex = 0;
    tab.addEventListener('click', event => {
      event.preventDefault();
      select(index);
    });
    tab.addEventListener('keydown', event => {
      if (event.key === ' ') {
        event.preventDefault();
        select(index);
        return;
      }
      const forward = document.documentElement.dir === 'rtl' ? -1 : 1;
      const next = {
        ArrowUp: index - 1, ArrowDown: index + 1,
        ArrowLeft: index - forward, ArrowRight: index + forward,
        Home: 0, End: tabs.length - 1
      }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      const target = (next + tabs.length) % tabs.length;
      select(target);
      tabs[target].focus();
    });
  });
  function followAnchor() {
    const index = tabs.findIndex(tab => tab.hash === location.hash);
    if (index >= 0) select(index);
    return index >= 0;
  }
  if (!followAnchor()) select(1);
  window.addEventListener('hashchange', followAnchor);
}

function enableDemo(stage) {
  const filter = stage.querySelector('select');
  const list = stage.querySelector('.order-list');
  const refresh = stage.querySelector('.refresh-orders');
  const player = stage.querySelector('.demo-player');
  const play = player.querySelector('[data-play]');
  const countdown = player.querySelector('bdi');
  const products = JSON.parse(stage.dataset.products);
  const orders = [0, 3, 1, 2, 4, 5].map((item, index) => ({
    id: 1048 - index,
    product: products[item],
    shipped: item >= 3
  }));
  let latest = 1048;
  let timer;
  let remaining = 3;

  function render() {
    const visible = orders.filter(order => filter.value === 'all' || !order.shipped).slice(0, 3);
    list.replaceChildren(...visible.map(order => {
      const row = document.createElement('li');
      const id = document.createElement('bdi');
      const name = document.createElement('strong');
      const status = document.createElement('span');
      id.textContent = '#' + order.id;
      name.textContent = order.product;
      status.textContent = order.shipped ? stage.dataset.shipped : stage.dataset.pending;
      row.append(id, name, status);
      return row;
    }));
  }
  function resetClock() {
    remaining = 3;
    countdown.textContent = '00:03';
  }
  function stop() {
    clearInterval(timer);
    timer = undefined;
    stage.classList.remove('running');
    play.querySelector('span').textContent = play.dataset.start;
    resetClock();
  }
  refresh.addEventListener('click', () => {
    latest += 1;
    orders.unshift({ id: latest, product: products[(latest - 1049 + 3) % products.length], shipped: false });
    if (orders.length > 8) orders.pop();
    render();
    list.firstElementChild.classList.add('arrived');
  });
  filter.addEventListener('change', render);
  play.addEventListener('click', () => {
    if (timer !== undefined) {
      stop();
      return;
    }
    stage.classList.add('running');
    play.querySelector('span').textContent = play.dataset.stop;
    refresh.click();
    timer = setInterval(() => {
      remaining -= 1;
      if (remaining === 0) {
        refresh.click();
        resetClock();
      } else {
        countdown.textContent = '00:0' + remaining;
      }
    }, 1000);
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => { if (!entry.isIntersecting) stop(); }).observe(stage);
  }
  filter.disabled = refresh.disabled = false;
  render();
  player.hidden = false;
}

document.querySelectorAll('[data-viewer]').forEach(enableShowcase);
document.querySelectorAll('[data-demo]').forEach(enableDemo);
