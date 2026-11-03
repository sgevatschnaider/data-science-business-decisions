'use strict';
(()=>{
 const M=NNMath,$=id=>document.getElementById(id),val=id=>+$ (id).value,fmt=(v,n=4)=>Number(v).toFixed(n),css=k=>getComputedStyle(document.documentElement).getPropertyValue(k).trim();
 const kind=document.body.dataset.lab,canvas=$('nn-extra');
 function plot(series,domainX,domainY,xlabel,ylabel,points=[]){
  const W=canvas.clientWidth||700,H=Math.max(310,Math.min(440,W*.58)),d=devicePixelRatio||1;canvas.style.height=H+'px';canvas.style.aspectRatio='auto';canvas.width=Math.round(W*d);canvas.height=Math.round(H*d);const g=canvas.getContext('2d');g.setTransform(d,0,0,d,0,0);g.fillStyle=css('--bg');g.fillRect(0,0,W,H);g.font=(W<500?'12':'15')+'px system-ui';
  const [xmin,xmax]=domainX,[ymin,ymax]=domainY,X=x=>62+(x-xmin)/(xmax-xmin)*(W-90),Y=y=>H-55-(y-ymin)/(ymax-ymin)*(H-95);g.lineWidth=1;g.strokeStyle=css('--grid');
  for(let j=0;j<=4;j++){const x=xmin+(xmax-xmin)*j/4,y=ymin+(ymax-ymin)*j/4;g.beginPath();g.moveTo(X(x),35);g.lineTo(X(x),H-55);g.moveTo(62,Y(y));g.lineTo(W-28,Y(y));g.stroke();g.fillStyle=css('--muted');g.fillText(Math.abs(x)>1000?x.toExponential(1):fmt(x,1),X(x)-8,H-30);g.fillText(Math.abs(y)>1000?y.toExponential(1):fmt(y,2),2,Y(y)+4);}
  for(const[s,idx]of series.map((s,i)=>[s,i])){g.strokeStyle=css(['--a','--b','--c'][idx%3]);g.lineWidth=3;g.beginPath();let open=false;for(const[x,y]of s){if(!Number.isFinite(y)){open=false;continue;}if(!open){g.moveTo(X(x),Y(y));open=true;}else g.lineTo(X(x),Y(y));}g.stroke();}
  for(const p of points){g.fillStyle=css(p.color||'--c');g.beginPath();if(p.square)g.rect(X(p.x)-6,Y(p.y)-6,12,12);else g.arc(X(p.x),Y(p.y),6,0,Math.PI*2);g.fill();if(p.label){g.fillStyle=css('--fg');g.fillText(p.label,Math.min(W-100,X(p.x)+8),Math.max(48,Y(p.y)-8));}}
  g.fillStyle=css('--fg');g.fillText(xlabel,Math.max(65,W-205),H-6);g.fillText(ylabel,62,22);return{g,W,H,X,Y};
 }
 function flow(nodes,gradient=false){
  const svg=$('nn-flow');if(!svg)return;const W=svg.parentElement.clientWidth||700,vertical=W<650,nw=vertical?Math.min(250,W-90):(W-60)/nodes.length-12,nh=76,H=vertical?nodes.length*118+60:gradient?280:200;
  const NS='http://www.w3.org/2000/svg';svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.style.height=H+'px';
  function e(n,a,t){const s=document.createElementNS(NS,n);for(const[k,v]of Object.entries(a))s.setAttribute(k,v);if(t!==undefined)s.textContent=t;svg.append(s);return s;}
  e('title',{},gradient?'Grafo de cálculo y gradientes':'Contribuciones a la memoria y al estado expuesto');
  const pos=nodes.map((n,j)=>vertical?{x:(W-nw)/2,y:20+j*118}:{x:25+j*(W-40)/nodes.length,y:50});
  for(let j=0;j<nodes.length;j++){
   const p=pos[j],n=nodes[j];if(j){const q=pos[j-1];e('path',{d:vertical?`M ${q.x+nw/2} ${q.y+nh} V ${p.y-10}`:`M ${q.x+nw} ${q.y+nh/2} H ${p.x-7}`,class:'path'});}
   e('rect',{x:p.x,y:p.y,width:nw,height:nh,rx:10,class:'node'});e('text',{x:p.x+nw/2,y:p.y+28,'text-anchor':'middle',class:'secondary'},n.label);e('text',{x:p.x+nw/2,y:p.y+56,'text-anchor':'middle'},n.value);
  }
  if(gradient){
   const p=pos[1],q=pos.at(-1),yy=vertical?H-18:205;
   if(!vertical)e('path',{d:`M ${q.x+nw/2} ${q.y+nh+8} V 170 H ${p.x+nw/2} V ${p.y+nh+8}`,class:'path memory'});
   e('text',{x:W/2,y:yy,'text-anchor':'middle'},gradient);
  }
 }
 function draw(d){
  if(!$('nn-extra-scene'))return;
  if(kind==='perceptron'){
   $('nn-extra-scene').hidden=d.scenario!=='xor';if(d.scenario!=='xor')return;
   const pts=M.points('xor').map(p=>({...p,...M.xorRepresentation(p.x,p.y)}));
   plot([[[0,-.25],[2,.75]]],[-.25,2.3],[-.4,1.25],'h₁ (activación)','h₂ (activación)',[{x:0,y:0,color:'--b',label:'00: clase 0'},{x:1,y:0,color:'--a',square:true,label:'01 y 10: clase 1'},{x:2,y:1,color:'--b',label:'11: clase 0'}]);
   $('nn-extra-values').textContent=pts.map(p=>`(${p.x},${p.y}) ⇒ h=(${p.h1},${p.h2}), salida=${p.output}`).join(' · ');
  }
  if(kind==='activaciones'){
   const fn=$('fn').value,z=val('z'),series=Array.from({length:241},(_,j)=>{let x=-6+j/20;return[x,M.activation(fn,x)[1]];}),ys=series.map(p=>p[1]).filter(Number.isFinite),der=M.activation(fn,z)[1];const{g,X,Y,H}=plot([series],[-6,6],[Math.min(-.1,...ys),Math.max(1.1,...ys)],'z (misma entrada)','Derivada φ′(z)');g.strokeStyle=css('--c');g.beginPath();g.moveTo(X(z),35);g.lineTo(X(z),H-55);g.stroke();if(der!==null){g.fillStyle=css('--b');g.beginPath();g.arc(X(z),Y(der),7,0,2*Math.PI);g.fill();}
  }
  if(kind==='gradiente'){
   if(d.scenario==='bce'){
    const extent=Math.max(3,Math.abs(val('w'))+.5,Math.abs(val('b'))+.5),pts=d.history.map(r=>({x:r.w,y:r.b})).filter(r=>Number.isFinite(r.x));pts.push({x:val('w'),y:val('b')});
    const {g,W,H,X,Y}=plot([],[-extent,extent],[-extent,extent],'Peso w','Sesgo b');
    const bg=css('--bg'),a=css('--a');g.save();g.globalAlpha=.55;
    for(let i=0;i<45;i++)for(let j=0;j<32;j++){const x=-extent+2*extent*i/44,y=-extent+2*extent*j/31,L=M.logistic(x,y).loss;g.globalAlpha=.05+.6/(1+L);g.fillStyle=a;g.fillRect(X(x),Y(y),Math.max(2,(W-90)/44+1),Math.max(2,(H-95)/31+1));}g.restore();
    g.strokeStyle=css('--c');g.lineWidth=3;g.beginPath();pts.forEach((p,j)=>j?g.lineTo(X(p.x),Y(p.y)):g.moveTo(X(p.x),Y(p.y)));g.stroke();g.fillStyle=css('--c');g.beginPath();g.arc(X(val('w')),Y(val('b')),7,0,2*Math.PI);g.fill();
    $('nn-extra-values').textContent='Mayor intensidad cian: menor BCE. Punto y trayectoria ámbar: parámetros recorridos. La BCE de datos separables sin penalización no tiene un mínimo finito en w.';
   }else{
    const w=val('w'),e=Math.max(4,Math.abs(w-2)+1),xs=Array.from({length:121},(_,j)=>2-e+2*e*j/120),curve=xs.map(x=>[x,.5*(x-2)**2]);plot([curve],[2-e,2+e],[0,e*e*.55],'Parámetro w','L = ½(w−2)²',[{x:w,y:.5*(w-2)**2,color:'--c',label:'Estado actual'},{x:2,y:0,color:'--b',label:'Mínimo'}]);$('nn-extra-values').textContent='La forma de la pérdida es fija. El learning rate cambia la trayectoria, no la posición del mínimo.';
   }
  }
  if(kind==='umbral'){
   const pts=M.cohort(991).sort((a,b)=>b.p-a.p),th=val('threshold');const{g,X,Y,H}=plot([],[-1,101],[0,1.05],'Clientes ordenados por riesgo','Score y decisión');const bw=Math.max(1,(canvas.clientWidth-90)/100*.75);
   for(let j=0;j<pts.length;j++){const p=pts[j],selected=p.p>=th;g.fillStyle=css(selected?(p.y?'--green':'--c'):'--border');g.fillRect(X(j),Y(p.p),bw,Y(0)-Y(p.p));if(p.y){g.fillStyle=css('--b');g.beginPath();g.arc(X(j)+bw/2,Y(p.p)-5,3,0,Math.PI*2);g.fill();}}
   g.strokeStyle=css('--a');g.lineWidth=2;g.beginPath();g.moveTo(X(0),Y(th));g.lineTo(X(100),Y(th));g.stroke();$('nn-extra-values').textContent='Barras verdes: abandono detectado; ámbar: contacto a quien no abandona; gris: sin contactar. Punto violeta: etiqueta real de abandono. Línea cian: umbral.';
  }
  if(kind==='lstm'){
   let c=0,prev=0,g=0;for(let t=1;t<=d.step;t++){prev=c;g=M.candidate(d.scenario,t);c=val('forget')*c+val('input')*g;}const keep=val('forget')*prev,write=val('input')*g,h=val('output')*Math.tanh(c);
   flow([{label:'Conservar f·c previo',value:fmt(keep)},{label:'Escribir i·g',value:fmt(write)},{label:'Memoria cₜ',value:fmt(c)},{label:'Exponer hₜ',value:fmt(h)}]);
   $('nn-extra-values').textContent=`t=${d.step}: memoria previa ${fmt(prev)}, f=${val('forget')}, i=${val('input')}, g=${fmt(g)}, o=${val('output')}. c y h cambian por mecanismos distintos. Extremos 0/1 e impulsos ±1 son idealizaciones didácticas.`;
  }
  if(kind==='backprop'){
   const r=d.last;flow([{label:'Entrada x',value:fmt(r.x,2)},{label:'Logit z',value:fmt(r.z,4)},{label:'Predicción p',value:fmt(r.p,4)},{label:'Pérdida L',value:fmt(r.loss,4)}],`∂L/∂w=${fmt(r.gw,5)} · ∂L/∂b=${fmt(r.gb,5)}`);
   $('nn-extra-values').textContent=`Pesos actuales: w=${fmt(r.w,6)}, b=${fmt(r.b,6)}. Siguiente actualización propuesta: w=${fmt(r.wn,6)}, b=${fmt(r.bn,6)}.`;
  }
  if(kind==='generalizacion'){
   const values=Array.from({length:9},(_,j)=>M.fitExperiment(j+1,val('lambda'),d.scenario)),ys=values.flatMap(v=>[v.trainMSE,v.validMSE]);plot([values.map(v=>[v.degree,v.trainMSE]),values.map(v=>[v.degree,v.validMSE])],[1,9],[0,Math.max(...ys)*1.1],'Grado del polinomio','MSE medido');$('nn-extra-values').textContent='Cian: entrenamiento. Violeta: validación. Misma semilla y observaciones en todos los grados; cambia únicamente la capacidad del modelo y la penalización elegida.';
  }
 }
 document.addEventListener('nn-render',e=>draw(e.detail));
 function refresh(){if(window.labDebug)draw({kind,step:labDebug.state.step,last:labDebug.state.last,history:labDebug.state.history,scenario:$('scenario').value});}
 window.addEventListener('resize',refresh);refresh();
})();
