'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const terms = [...document.querySelectorAll('.term')];
  const units = [...document.querySelectorAll('.unit')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const key = 'uca-nn-glossary-progress-v1';
  const validIds = new Set(terms.map(t => t.id));
  let learned = new Set(), persistent = true, active = 'all', route = null;
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const searchText = new Map(terms.map(t => [t.id, normalize(t.dataset.search)]));
  const routes = {redes:['fundamentos','aprendizaje','validacion'], secuencias:['secuencias','rnn','lstm']};
  const params = new URLSearchParams(location.search);
  if (routes[params.get('recorrido')]) route = params.get('recorrido');
  if (units.some(u => u.dataset.unit === params.get('unidad'))) active = params.get('unidad');
  try {
    const raw = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(raw)) learned = new Set(raw.filter(id => validIds.has(id)));
  } catch { persistent = false; }
  let theme = 'dark';
  try { theme = localStorage.getItem('uca-nn-theme') || theme; } catch {}
  function setTheme(value) {
    theme = ['dark','light','contrast'].includes(value) ? value : 'dark';
    root.dataset.theme = theme;
    $('theme').value = theme;
    try { localStorage.setItem('uca-nn-theme', theme); } catch {}
  }
  setTheme(theme);
  $('theme').addEventListener('change', e => setTheme(e.target.value));
  function save() {
    try { localStorage.setItem(key, JSON.stringify([...learned])); }
    catch { persistent = false; }
    updateProgress();
  }
  function updateProgress() {
    $('progress').value = learned.size;
    $('progress').textContent = String(learned.size);
    $('progress-label').textContent = `${learned.size} de ${terms.length} estudiados`;
    $('storage-note').textContent = persistent ? 'El avance se guarda en este navegador.' : 'Guardado local no disponible: avance temporal durante esta visita.';
    for (const term of terms) {
      const checked = learned.has(term.id);
      term.dataset.done = String(checked);
      term.querySelector('[data-learned]').checked = checked;
    }
  }
  function apply() {
    const words = normalize($('search').value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const term of terms) {
      const inGroup = active === 'all' || term.dataset.group === active;
      const inRoute = !route || routes[route].includes(term.dataset.group);
      const match = words.every(w => searchText.get(term.id).includes(w));
      const pending = !$('pending').checked || !learned.has(term.id);
      term.hidden = !(inGroup && inRoute && match && pending);
      if (!term.hidden) count++;
    }
    for (const unit of units) unit.hidden = ![...unit.querySelectorAll('.term')].some(t => !t.hidden);
    for (const button of filters) button.setAttribute('aria-pressed', String(button.dataset.filter === active));
    $('empty').hidden = count > 0;
    const routeText = route === 'redes' ? ' · Recorrido de redes neuronales' : route === 'secuencias' ? ' · Recorrido de secuencias, RNN y LSTM' : '';
    $('result-count').textContent = `${count} de ${terms.length} conceptos${routeText}${$('pending').checked ? ' · Solo pendientes' : ''}${words.length ? ` · Búsqueda: “${$('search').value.trim()}”` : ''}`;
  }
  function clearFilters() { active = 'all'; route = null; $('search').value = ''; $('pending').checked = false; apply(); }
  filters.forEach(button => button.addEventListener('click', () => { active = button.dataset.filter; route = null; apply(); }));
  $('search').addEventListener('input', apply);
  $('pending').addEventListener('change', apply);
  $('clear').addEventListener('click', () => { $('search').value = ''; apply(); $('search').focus(); });
  $('show-all').addEventListener('click', clearFilters);
  terms.forEach(term => term.querySelector('[data-learned]').addEventListener('change', e => {
    e.target.checked ? learned.add(term.id) : learned.delete(term.id);
    save(); apply();
  }));
  $('reset-progress').addEventListener('click', () => { learned.clear(); save(); apply(); });
  function revealHash(focus = false) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const unit = target.matches('.unit') ? target : target.closest('.unit');
    const groupHeading = id.startsWith('unit-');
    if ((target.matches('.term') && target.hidden) || unit?.hidden || groupHeading) {
      clearFilters();
      if (groupHeading) { active = id.slice(5); apply(); }
    }
    if (target.matches('.term') || groupHeading) {
      target.scrollIntoView({block:'start'});
      if (focus) {
        const heading = target.matches('.term') ? target.querySelector('h3') : target;
        heading.tabIndex = -1; heading.focus({preventScroll:true});
      }
    }
  }
  window.addEventListener('hashchange', () => revealHash(true));
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (a && a.hash === location.hash) revealHash(true);
  });
  $('jump').addEventListener('change', e => { if (e.target.value) { location.hash = e.target.value; revealHash(true); } e.target.value = ''; });
  document.addEventListener('keydown', e => {
    const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '') || document.activeElement?.isContentEditable;
    if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); $('search').focus(); }
    if (e.key === 'Escape' && document.activeElement === $('search')) { $('search').value = ''; apply(); }
  });
  updateProgress(); apply();
  if (location.hash) requestAnimationFrame(() => revealHash());
  const number = (n, d = 6) => n.toLocaleString('es-AR', {minimumFractionDigits:d, maximumFractionDigits:d});
  function neuron() {
    const z = Number($('calc-logit').value), p = 1/(1+Math.exp(-z));
    $('logit-value').value = number(z, 2);
    $('probability').textContent = number(p);
    $('bce').textContent = number(Math.log1p(Math.exp(-z)));
    $('logit-gradient').textContent = number(p-1);
    $('prob-bar').style.width = `${p*100}%`;
  }
  function rnn() {
    const w = Number($('recurrent').value); let h=0; const states=[];
    for (let t=0;t<6;t++) { h=Math.tanh((t===0?1:0)+w*h); states.push(h); }
    $('recurrent-value').value = number(w, 2);
    const bars = states.map(h => { const bar = document.createElement('span'), fill=document.createElement('i'); bar.className='rnn-bar'; fill.style.height=`${Math.abs(h)*48}%`; fill.style[h>=0?'bottom':'top']='50%'; fill.style.background=h>=0?'var(--accent)':'var(--violet)'; bar.append(fill); return bar; });
    $('rnn-bars').replaceChildren(...bars);
    $('rnn-values').textContent = states.map((h,t)=>`h${t+1}=${number(h,4)}`).join(' · ');
  }
  function lstm() {
    const f=Number($('forget').value), i=Number($('write').value), retained=f*.8, written=i*.5, c=retained+written;
    $('forget-value').value=number(f,2); $('write-value').value=number(i,2);
    $('retained').textContent=number(retained,4); $('written').textContent=number(written,4);
    $('cell-result').textContent=number(c,4); $('hidden-result').value=number(.7*Math.tanh(c),4);
  }
  $('calc-logit').addEventListener('input',neuron); $('recurrent').addEventListener('input',rnn);
  ['forget','write'].forEach(id=>$(id).addEventListener('input',lstm)); neuron(); rnn(); lstm();
  let detailState = null;
  window.addEventListener('beforeprint', () => { detailState=[...document.querySelectorAll('.review,.answer')].map(d=>[d,d.open]); detailState.forEach(([d])=>d.open=true); });
  window.addEventListener('afterprint', () => { if(detailState) detailState.forEach(([d,open])=>d.open=open); detailState=null; });
  $('print').addEventListener('click',()=>window.print());
})();
