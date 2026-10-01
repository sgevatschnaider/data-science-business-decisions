(()=>{'use strict';
const cards=Array.from(document.querySelectorAll('.video-card'));
const filters=Array.from(document.querySelectorAll('[data-filter]'));
const filterBar=document.querySelector('.filters');
function filter(value){let count=0;cards.forEach(card=>{card.hidden=value!=='todos'&&card.dataset.category!==value;if(!card.hidden)count++;});filters.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.filter===value)));document.getElementById('filter-status').textContent=`${count} de ${cards.length} videos visibles.`;}
if(filterBar)filterBar.hidden=false;
filters.forEach(button=>button.addEventListener('click',()=>filter(button.dataset.filter)));
function revealHash(){const target=document.getElementById(location.hash.slice(1));if(target&&target.classList.contains('video-card')&&target.hidden){filter('todos');target.scrollIntoView({block:'start'});}}
window.addEventListener('hashchange',revealHash);
document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{const target=document.getElementById(link.hash.slice(1));if(target&&target.classList.contains('video-card')&&target.hidden)filter('todos');}));
const player=document.getElementById('reproductor');const container=document.getElementById('player-container');let lastTrigger=null;
document.querySelectorAll('[data-video]').forEach(button=>{button.hidden=false;button.addEventListener('click',()=>{
 const {video,start,end,label}=button.dataset;
 if(!/^[A-Za-z0-9_-]+$/.test(video)||!/^\d+$/.test(start)||!/^\d+$/.test(end)||Number(end)<=Number(start))return;
 const url=new URL(`https://www.youtube-nocookie.com/embed/${video}`);
 url.search=new URLSearchParams({start,end,rel:'0',cc_load_policy:'1',cc_lang_pref:'es'}).toString();
 const iframe=document.createElement('iframe');iframe.src=url.href;iframe.title=label;iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';
 container.replaceChildren(iframe);document.getElementById('player-title').textContent=label;document.getElementById('player-fallback').href=`https://www.youtube.com/watch?v=${video}&t=${start}s`;lastTrigger=button;player.hidden=false;player.scrollIntoView({behavior:'smooth',block:'start'});document.getElementById('close-player').focus({preventScroll:true});
});});
function closePlayer(){container.replaceChildren();player.hidden=true;if(lastTrigger)lastTrigger.focus();}
document.getElementById('close-player').addEventListener('click',closePlayer);
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!player.hidden)closePlayer();});
})();
