(()=>{'use strict';
const cards=[...document.querySelectorAll('.video-card')],ids=cards.map(c=>c.dataset.id),filters=[...document.querySelectorAll('[data-filter]')],search=document.getElementById('searchVideos');
const player=document.getElementById('reproductor'),playerBox=document.getElementById('playerContainer'),fallback=document.getElementById('youtubeFallback');
let active='todos',current=-1,lastTrigger=null;const storagePrefix='m10-videos-v1:';
function read(key){try{return localStorage.getItem(storagePrefix+key);}catch(e){return null}}
function write(key,val){try{localStorage.setItem(storagePrefix+key,val);}catch(e){}}
let theme=read('theme')==='light'?'light':'dark';
function setTheme(v){theme=v;document.documentElement.dataset.theme=v;document.getElementById('themeToggle').textContent=v==='dark'?'☀ Modo claro':'◐ Modo oscuro';write('theme',v);}
setTheme(theme);document.getElementById('themeToggle').addEventListener('click',()=>setTheme(theme==='dark'?'light':'dark'));
let done=new Set;try{const s=JSON.parse(read('watched')||'[]');if(Array.isArray(s))done=new Set(s.filter(x=>ids.includes(x)));}catch(e){}
function paintDone(){document.querySelectorAll('[data-watched]').forEach(ch=>ch.checked=done.has(ch.dataset.watched));document.getElementById('progressText').textContent=`${done.size} de ${ids.length} estudiados`;document.getElementById('progressFill').style.width=`${done.size/ids.length*100}%`;if(current>=0){let id=ids[current];document.getElementById('watchedCurrent').textContent=done.has(id)?'✓ Estudiado · desmarcar':'Marcar como estudiado';}}
function saveDone(){write('watched',JSON.stringify([...done]));paintDone();if(active==='pendientes')applyFilters()}
function toggleDone(id){if(done.has(id))done.delete(id);else done.add(id);saveDone()}
document.querySelectorAll('[data-watched]').forEach(ch=>ch.addEventListener('change',()=>toggleDone(ch.dataset.watched)));
paintDone();document.getElementById('watchedCurrent').addEventListener('click',()=>{if(current>=0)toggleDone(ids[current]);});
function applyFilters(){const q=search.value.trim().toLocaleLowerCase('es');let n=0;cards.forEach(c=>{const flag=active==='todos'||active===c.dataset.cat||(active==='pendientes'&&!done.has(c.dataset.id));c.hidden=!(flag&&(!q||c.dataset.search.includes(q)));if(!c.hidden)n++;});filters.forEach(b=>b.setAttribute('aria-pressed',String(active===b.dataset.filter)));document.getElementById('filterStatus').textContent=`${n} de ${cards.length} videos visibles`;document.getElementById('emptyState').hidden=n!==0;document.querySelectorAll('.video-group').forEach(g=>{g.hidden=!g.querySelector('.video-card:not([hidden])')});}
filters.forEach(btn=>btn.addEventListener('click',()=>{active=btn.dataset.filter;applyFilters()}));search.addEventListener('input',applyFilters);
function revealHash(){const e=location.hash?document.getElementById(decodeURIComponent(location.hash.slice(1))):null;if(e?.classList.contains('video-card')&&e.hidden){active='todos';search.value='';applyFilters()}}
window.addEventListener('hashchange',revealHash);revealHash();applyFilters();
const registry=new Map(cards.map(c=>[c.dataset.id,c]));
function youtubeLink(id,start){const url=new URL('https://www.youtube.com/watch');url.searchParams.set('v',id);if(start>0)url.searchParams.set('t',`${start}s`);return url.href;}
function play(id,start=0,trigger=null){const c=registry.get(id);if(!c||!(/^[A-Za-z0-9_-]{11}$/.test(c.dataset.video))||!Number.isSafeInteger(start)||start<0)return;current=ids.indexOf(id);lastTrigger=trigger;
const vid=c.dataset.video,heading=c.querySelector('h3')?.textContent||id;
const url=new URL(`https://www.youtube-nocookie.com/embed/${vid}`);
// No end= parameter: playback proceeds to the end of the original video.
url.searchParams.set('rel','0');url.searchParams.set('cc_load_policy','1');url.searchParams.set('cc_lang_pref','es');url.searchParams.set('playsinline','1');if(start)url.searchParams.set('start',String(start));
const frame=document.createElement('iframe');frame.title=`Video ${id}: ${heading}`;frame.src=url.href;frame.loading='eager';frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';
playerBox.replaceChildren(frame);document.getElementById('watchTitle').textContent=`${id} · ${heading}`;document.getElementById('watchMeta').textContent=`${c.querySelector('.byline strong')?.textContent||''} · ${start>0?'Desde '+formatTime(start):'Desde el comienzo'} · sin límite de reproducción`;
document.getElementById('watchFit').textContent=c.querySelector('.evaluation p:first-child')?.textContent.replace(/^Por qué se eligió:\s*/,'')||'';
document.getElementById('watchLimits').textContent=c.querySelector('.evaluation p:nth-child(2)')?.textContent.replace(/^Precaución docente:\s*/,'')||'';
document.getElementById('watchQuestion').textContent=c.querySelector('.reflect')?.textContent.replace(/^Para explicar:\s*/,'')||'';
fallback.href=youtubeLink(vid,start);document.getElementById('playerSlides').href=c.querySelector('.slide-ref')?.nextElementSibling?.href||c.querySelector('.card-actions a[href*=".pdf"]')?.href||'guia.html';
document.getElementById('playerLab').href=c.querySelector('.card-actions a[href*="simuladores/"]')?.href||'simulacion.html';
player.hidden=false;paintDone();player.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});document.getElementById('closePlayer').focus({preventScroll:true});
}
function formatTime(v){return `${String(Math.floor(v/60)).padStart(2,'0')}:${String(v%60).padStart(2,'0')}`;}
for(const btn of document.querySelectorAll('[data-play]'))btn.addEventListener('click',()=>play(btn.dataset.play,Number(btn.dataset.start||0),btn));
function close(){playerBox.replaceChildren();player.hidden=true;current=-1;if(lastTrigger?.isConnected)lastTrigger.focus();}
document.getElementById('closePlayer').addEventListener('click',close);
document.getElementById('prevVideo').addEventListener('click',()=>current>0&&play(ids[current-1]));document.getElementById('nextVideo').addEventListener('click',()=>current<ids.length-1&&play(ids[current+1]));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!player.hidden)close();});
window.M10VideoCatalog={get videos(){return ids.slice()},get current(){return current<0?null:ids[current]},get filter(){return active},get theme(){return theme},get watched(){return [...done]},play,close};
})();