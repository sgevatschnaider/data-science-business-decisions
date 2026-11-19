
(() => {
  'use strict';
  const docs = [
    {title:'Soluciones básicas',pdf:'presentaciones/clase-01.pdf',ppt:'presentaciones/clase-01.pptx',visor:'presentacion-01.html',pages:21},
    {title:'Método Simplex',pdf:'presentaciones/clase-02.pdf',ppt:'presentaciones/clase-02.pptx',visor:'presentacion-02.html',pages:23}
  ];
  const tabs=[...document.querySelectorAll('[data-m10g-tab]')],frame=document.getElementById('m10g-frame');
  const title=document.getElementById('m10g-reader-title'),pdf=document.getElementById('m10g-reader-pdf'),ppt=document.getElementById('m10g-reader-ppt'),visor=document.getElementById('m10g-reader-visor');
  function select(i,focus=false){
    if(i<0||i>=docs.length)return;
    const d=docs[i];tabs.forEach((b,n)=>{b.setAttribute('aria-selected',String(n===i));b.tabIndex=n===i?0:-1;});
    title.textContent=d.title+' · '+d.pages+' diapositivas';
    frame.setAttribute('title','Lectura PDF: '+d.title);frame.src=d.pdf+'#page=1&view=FitH';
    pdf.href=d.pdf;ppt.href=d.ppt;visor.href=d.visor;
    if(focus)tabs[i].focus();
    if(history.replaceState)history.replaceState(null,'','#clase-'+(i+1));
  }
  tabs.forEach((b,i)=>{
    b.addEventListener('click',()=>select(i));
    b.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();select((i+(e.key==='ArrowRight'?1:1))%2,true);}});
  });
  document.querySelectorAll('[data-m10g-open]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();select(Number(a.dataset.m10gOpen));document.getElementById('lectura').scrollIntoView({behavior:'smooth',block:'start'});}));
  const index=Number(location.hash.match(/^#clase-([12])$/)?.[1]||1)-1;
  select(index);
})();
