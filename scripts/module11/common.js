'use strict';
(()=>{const root=document.documentElement,sel=document.getElementById('theme');let theme='dark';try{theme=localStorage.getItem('uca-nn-theme')||theme;}catch{}if(!['light','dark','contrast'].includes(theme))theme='dark';function set(t){root.dataset.theme=t;if(sel)sel.value=t;try{localStorage.setItem('uca-nn-theme',t);}catch{}document.dispatchEvent(new Event('themechange'));}set(theme);if(sel)sel.onchange=()=>set(sel.value);})();
window.toggleFullscreen=async element=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await element.requestFullscreen();}catch(e){const p=document.getElementById('error');if(p)p.textContent='La pantalla completa no está disponible en este navegador. Podés continuar con el visor normal.';}};

// Conserva el avance independiente de los recursos históricos del módulo.
document.querySelectorAll('[data-progress-item]').forEach(e=>{const key='uca-nn-progress-'+e.dataset.progressItem;try{e.checked=localStorage.getItem(key)==='true';}catch{}e.addEventListener('change',()=>{try{localStorage.setItem(key,String(e.checked));}catch{}});});
