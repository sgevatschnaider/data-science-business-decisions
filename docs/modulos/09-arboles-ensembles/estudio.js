/* Apoyo compartido del glosario y cuestionario. */
window.M09Study = (() => {
  'use strict';
  const memory = new Map();
  function get(key, fallback) {
    try { return localStorage.getItem(key) ?? memory.get(key) ?? fallback; }
    catch { return memory.get(key) ?? fallback; }
  }
  function set(key, value) {
    memory.set(key, value);
    try { localStorage.setItem(key, value); } catch {}
  }
  function remove(key) {
    memory.delete(key);
    try { localStorage.removeItem(key); } catch {}
  }
  function json(key, fallback) {
    try { return JSON.parse(get(key, JSON.stringify(fallback))); }
    catch { return fallback; }
  }
  function theme(value) {
    const selected = value === 'light' ? 'light' : 'dark';
    document.documentElement.dataset.theme = selected;
    set('m09-theme', selected);
    document.getElementById('themeBtn').textContent = selected === 'light' ? '🌙 Tema oscuro' : '☀️ Tema claro';
  }
  theme(get('m09-theme', 'dark'));
  document.getElementById('themeBtn').onclick = () => theme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
  const top = document.querySelector('.top');
  const measure = () => document.documentElement.style.setProperty('--study-header-height', `${top.getBoundingClientRect().height}px`);
  measure();
  if (window.ResizeObserver) new ResizeObserver(measure).observe(top);
  else window.addEventListener('resize', measure);
  return {get, set, remove, json, normalize: value => (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()};
})();
