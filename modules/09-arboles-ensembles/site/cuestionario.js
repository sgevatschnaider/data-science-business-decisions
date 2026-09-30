(() => {
  'use strict';
  const {json, set, remove, normalize} = M09Study;
  const KEY = 'm09-quiz-state-v2';
  const cards = [...document.querySelectorAll('.qcard')];
  const $ = id => document.getElementById(id);
  const search = $('search'), category = $('cat'), difficulty = $('diff');
  const saved = json(KEY, {});
  let state = saved && !Array.isArray(saved) && typeof saved === 'object' ? saved : {};
  let onlyPending = false, focus = false;
  cards.forEach(card => card.dataset.search = normalize(card.textContent));
  const visible = () => cards.filter(card => !card.classList.contains('hidden'));
  function chooseQuestion(randomize = false) {
    const pool = visible(), current = cards.find(card => card.classList.contains('focus'));
    let selected = pool.includes(current) && !randomize ? current : null;
    if (!selected && pool.length) {
      const candidates = randomize && pool.length > 1 ? pool.filter(card => card !== current) : pool;
      selected = candidates[Math.floor(Math.random() * candidates.length)];
    }
    cards.forEach(card => card.classList.toggle('focus', focus && card === selected));
    if (focus && selected && selected !== current) selected.querySelector('details').open = false;
    if (selected && randomize) {
      selected.querySelector('details').open = false;
      selected.scrollIntoView({behavior:'smooth', block:'center'});
      selected.focus({preventScroll:true});
    }
    $('randomBtn').disabled = !pool.length;
  }
  function filter() {
    const query = normalize(search.value);
    cards.forEach(card => {
      const ok = (!query || card.dataset.search.includes(query))
        && (!category.value || card.dataset.cat === category.value)
        && (!difficulty.value || card.dataset.diff === difficulty.value)
        && (!onlyPending || state[card.dataset.id] !== 'mastered');
      card.classList.toggle('hidden', !ok);
    });
    $('visibleQ').textContent = visible().length;
    $('empty').classList.toggle('hidden', visible().length !== 0);
    chooseQuestion();
  }
  function sync() {
    let mastered = 0, review = 0;
    cards.forEach(card => {
      const value = state[card.dataset.id] || 'pending';
      card.classList.toggle('mastered', value === 'mastered');
      card.classList.toggle('review', value === 'review');
      card.querySelector('.stateLabel').textContent = value === 'mastered' ? '✓ Dominada' : value === 'review' ? '↺ Repasar' : 'Pendiente';
      card.querySelector('.masterBtn').setAttribute('aria-pressed', String(value === 'mastered'));
      card.querySelector('.reviewBtn').setAttribute('aria-pressed', String(value === 'review'));
      if (value === 'mastered') mastered++;
      if (value === 'review') review++;
    });
    $('done').textContent = mastered;
    $('reviewCount').textContent = review;
    $('bar').style.width = `${100 * mastered / cards.length}%`;
    filter();
  }
  function setState(id, value) {
    if (state[id] === value) delete state[id];
    else state[id] = value;
    set(KEY, JSON.stringify(state));
    sync();
  }
  cards.forEach(card => {
    card.tabIndex = -1;
    card.querySelector('.reviewBtn').onclick = () => setState(card.dataset.id, 'review');
    card.querySelector('.masterBtn').onclick = () => setState(card.dataset.id, 'mastered');
  });
  search.oninput = category.onchange = difficulty.onchange = filter;
  $('pendingBtn').onclick = () => {
    onlyPending = !onlyPending;
    $('pendingBtn').textContent = onlyPending ? 'Mostrar todas' : 'Solo pendientes';
    $('pendingBtn').setAttribute('aria-pressed', String(onlyPending));
    filter();
  };
  $('clearBtn').onclick = () => {
    search.value = category.value = difficulty.value = '';
    onlyPending = false;
    $('pendingBtn').textContent = 'Solo pendientes';
    $('pendingBtn').setAttribute('aria-pressed', 'false');
    filter();
    search.focus();
  };
  $('showAll').onclick = () => visible().filter(card => !focus || card.classList.contains('focus')).forEach(card => card.querySelector('details').open = true);
  $('hideAll').onclick = () => cards.forEach(card => card.querySelector('details').open = false);
  $('randomBtn').onclick = () => {
    if (focus) chooseQuestion(true);
    else {
      const pool = visible();
      if (!pool.length) return;
      const card = pool[Math.floor(Math.random() * pool.length)];
      card.scrollIntoView({behavior:'smooth', block:'center'});
      card.focus({preventScroll:true});
    }
  };
  $('focusBtn').onclick = () => {
    focus = !focus;
    document.body.classList.toggle('focusmode', focus);
    $('focusBtn').textContent = focus ? 'Salir de examen' : 'Modo examen';
    $('focusBtn').setAttribute('aria-pressed', String(focus));
    $('randomBtn').textContent = focus ? 'Otra pregunta' : 'Pregunta aleatoria';
    chooseQuestion(focus);
  };
  $('resetProgress').onclick = () => {
    if (confirm('¿Reiniciar todo el progreso guardado?')) {
      state = {};
      remove(KEY);
      sync();
    }
  };
  sync();
})();
