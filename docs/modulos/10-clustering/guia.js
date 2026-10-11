
(() => {
  'use strict';
  const docs = [
    {title:'PCA · Análisis de Componentes Principales',pdf:'presentaciones/M10_01_PCA_Clase_Completa.pdf',ppt:'presentaciones/M10_01_PCA_Clase_Completa.pptx',visor:'presentacion-01.html',pages:29},
    {title:'K-Means · Segmentación y validación',pdf:'presentaciones/M10_02_KMeans_Clase_Completa.pdf',ppt:'presentaciones/M10_02_KMeans_Clase_Completa.pptx',visor:'presentacion-02.html',pages:31},
    {title:'Clustering jerárquico · Dendrogramas y linkage',pdf:'presentaciones/M10_03_Jerarquico_Clase_Completa.pdf',ppt:'presentaciones/M10_03_Jerarquico_Clase_Completa.pptx',visor:'presentacion-03.html',pages:31}
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
    b.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();select((i+(e.key==='ArrowRight'?1:2))%3,true);}});
  });
  const index=Number(location.hash.match(/^#clase-([123])$/)?.[1]||1)-1;
  select(index);
})();
