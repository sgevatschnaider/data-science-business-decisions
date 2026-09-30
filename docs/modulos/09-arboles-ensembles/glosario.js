(() => {
  'use strict';
  const {json, set, normalize} = M09Study;
  const KEY = 'm09-glossary-learned-v2';
  const cards = [...document.querySelectorAll('.term-card')];
  const $ = id => document.getElementById(id);
  const search = $('search'), category = $('cat'), status = $('status');
  const saved = json(KEY, []), ids = new Set(cards.map(card => card.querySelector('.learnBtn').dataset.id));
  const learned = new Set(Array.isArray(saved) ? saved.filter(id => ids.has(id)) : []);
  let flash = false;
  cards.forEach(card => card.dataset.search = normalize(card.textContent));
  function filter() {
    const query = normalize(search.value);
    let count = 0;
    cards.forEach(card => {
      const id = card.querySelector('.learnBtn').dataset.id;
      const ok = (!query || card.dataset.search.includes(query))
        && (!category.value || card.dataset.cat === category.value)
        && (!status.value || (status.value === 'learned' ? learned.has(id) : !learned.has(id)));
      card.classList.toggle('hidden', !ok);
      if (ok) count++;
    });
    $('visibleCount').textContent = count;
    $('empty').classList.toggle('hidden', count !== 0);
  }
  function syncLearned() {
    cards.forEach(card => {
      const button = card.querySelector('.learnBtn'), yes = learned.has(button.dataset.id);
      card.classList.toggle('learned', yes);
      button.textContent = yes ? '✓ Aprendido' : 'Marcar aprendido';
      button.setAttribute('aria-pressed', String(yes));
    });
    $('learnedCount').textContent = learned.size;
    set(KEY, JSON.stringify([...learned]));
    filter();
  }
  function reveal(card) {
    card.classList.toggle('revealed');
    const yes = card.classList.contains('revealed'), button = card.querySelector('.revealBtn');
    button.textContent = yes ? 'Ocultar definición' : 'Mostrar definición';
    button.setAttribute('aria-expanded', String(yes));
    if (!yes) card.querySelector('details').open = false;
  }
  cards.forEach(card => {
    const button = card.querySelector('.learnBtn');
    button.onclick = () => {
      learned.has(button.dataset.id) ? learned.delete(button.dataset.id) : learned.add(button.dataset.id);
      syncLearned();
    };
    const revealButton = document.createElement('button');
    revealButton.type = 'button';
    revealButton.className = 'revealBtn';
    revealButton.textContent = 'Mostrar definición';
    revealButton.setAttribute('aria-expanded', 'false');
    revealButton.onclick = () => reveal(card);
    card.insertBefore(revealButton, card.querySelector('details'));
    card.addEventListener('dblclick', event => {
      if (flash && !event.target.closest('button,a,summary')) reveal(card);
    });
  });
  function clearFilters() {
    search.value = category.value = status.value = '';
    filter();
  }
  search.oninput = category.onchange = status.onchange = filter;
  $('clearBtn').onclick = () => {clearFilters(); search.focus();};
  $('expandAll').onclick = () => cards.filter(card => !card.classList.contains('hidden')).forEach(card => {
    if (flash && !card.classList.contains('revealed')) reveal(card);
    card.querySelector('details').open = true;
  });
  $('collapseAll').onclick = () => cards.forEach(card => card.querySelector('details').open = false);
  $('flashBtn').onclick = () => {
    flash = !flash;
    document.body.classList.toggle('flash', flash);
    cards.forEach(card => {
      card.classList.remove('revealed');
      card.querySelector('.revealBtn').textContent = 'Mostrar definición';
      card.querySelector('.revealBtn').setAttribute('aria-expanded', 'false');
      card.querySelector('details').open = false;
    });
    $('flashBtn').textContent = flash ? 'Salir de tarjetas' : 'Modo tarjetas';
    $('flashBtn').setAttribute('aria-pressed', String(flash));
  };
  document.querySelectorAll('a[href^="#term-"]').forEach(link => link.addEventListener('click', () => {
    const target = document.getElementById(link.getAttribute('href').slice(1));
    if (target?.classList.contains('hidden')) clearFilters();
  }));
  const letters = [...new Set(cards.map(card => normalize(card.dataset.term)[0]?.toUpperCase()).filter(Boolean))].sort();
  letters.forEach(letter => {
    const button = document.createElement('button');
    button.textContent = letter;
    button.setAttribute('aria-label', `Ir a conceptos con ${letter}`);
    button.onclick = () => {
      const card = cards.find(card => normalize(card.dataset.term).startsWith(letter.toLowerCase()) && !card.classList.contains('hidden'));
      if (card) card.scrollIntoView({behavior:'smooth', block:'center'});
    };
    $('az').appendChild(button);
  });
  syncLearned();
})();
