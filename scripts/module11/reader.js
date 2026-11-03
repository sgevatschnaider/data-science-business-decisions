'use strict';
(()=>{
 const $=id=>document.getElementById(id),D=window.DECK,slides=D.slides;
 let q=new URLSearchParams(location.search),n=Math.max(1,Math.min(slides.length,Number(q.get('slide'))||1));
 if(q.get('route')==='essential')$('route').value='essential';
 function route(){return $('route').value==='essential'?slides.filter(s=>s.essential).map(s=>s.number):slides.map(s=>s.number);}
 function toc(){const term=$('search').value.toLocaleLowerCase('es');$('toc').replaceChildren();for(const s of slides){if($('route').value==='essential'&&!s.essential)continue;if(term&&!`${s.title} ${s.transcript} ${s.notes}`.toLocaleLowerCase('es').includes(term))continue;let b=document.createElement('button');b.type='button';b.textContent=`${String(s.number).padStart(2,'0')} · ${s.title}`;b.setAttribute('aria-current',String(s.number===n));b.onclick=()=>show(s.number,true);$('toc').append(b);}}
 function link(href,label){let a=document.createElement('a');a.href=href;a.className='button';a.textContent=label;return a;}
 function show(value,announce=false){
  n=Math.max(1,Math.min(slides.length,Number(value)||1));const s=slides[n-1];
  $('slide-image').src=s.image;$('slide-image').alt=`Diapositiva ${n}: ${s.title}. Transcripción disponible debajo del visor.`;$('slide-title').textContent=s.title;$('number').value=n;$('number').max=slides.length;$('total').textContent=`/ ${slides.length}`;$('progress').value=n;$('progress').max=slides.length;$('progress').textContent=`${n} de ${slides.length}`;
  $('notes').textContent=s.notes;$('transcript').textContent=s.transcript;$('sources').replaceChildren();for(const f of s.sources){const li=document.createElement('li');if(f.url){let a=document.createElement('a');a.href=f.url;a.textContent=f.label;a.target='_blank';a.rel='noopener noreferrer';li.append(a);}else li.textContent=f.label;$('sources').append(li);}
  $('related').replaceChildren();for(const p of s.labs)$('related').append(link(p+`?slide=${n}&route=${$('route').value}`,'Simulación relacionada'));for(const id of s.videos){let v=D.videos.find(v=>v.id===id);$('related').append(link(`videos.html#${id}`,v.channel+' · '+(id==='calc'?'Cálculo':id==='bp'?'Backpropagation':id==='gd'?'Gradiente':id==='nn'?'Redes neuronales':id.toUpperCase())));}
  const rr=route();$('previous').disabled=!rr.some(x=>x<n);$('next').disabled=!rr.some(x=>x>n);toc();let u=new URL(location.href);u.searchParams.set('slide',n);u.searchParams.set('route',$('route').value);history.replaceState(null,'',u);try{localStorage.setItem('uca-slide-'+D.slug,String(n));}catch{}document.title=s.title+' · UCA';if(announce)$('announcement').textContent=`Diapositiva ${n} de ${slides.length}: ${s.title}`;
 }
 function move(dir){let rr=route();show(dir<0?rr.filter(x=>x<n).at(-1)||rr[0]:rr.find(x=>x>n)||rr.at(-1),true);}
 $('previous').onclick=()=>move(-1);$('next').onclick=()=>move(1);$('number').onchange=()=>show($('number').value,true);$('route').onchange=()=>{let rr=route();show(rr.includes(n)?n:rr.find(x=>x>=n)||rr.at(-1),true);};$('search').oninput=toc;
 $('fullscreen').onclick=()=>toggleFullscreen($('stage'));document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Salir de pantalla completa':'Pantalla completa';});
 document.addEventListener('keydown',e=>{if(['INPUT','TEXTAREA','SELECT','BUTTON'].includes(e.target.tagName)||e.altKey||e.ctrlKey||e.metaKey)return;const rr=route();if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();if(e.key==='Home')show(rr[0],true);else if(e.key==='End')show(rr.at(-1),true);else move(e.key==='ArrowLeft'?-1:1);}});
 $('slide-image').onerror=()=>{$('error').textContent='No se pudo cargar la imagen. La transcripción y las notas siguen disponibles.';};show(n);
})();
