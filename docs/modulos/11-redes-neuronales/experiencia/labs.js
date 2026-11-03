'use strict';
(()=>{
 const $=id=>document.getElementById(id),M=NNMath,K=document.body.dataset.lab;
 let timer=null,running=false,step=0,history=[],cohort=M.cohort(991),w=[-.5,.2,0],losses=[],last=null;
 const val=id=>+$ (id).value, fmt=(x,n=4)=>x==null?'no definida':Number(x).toFixed(n);
 const put=(id,t)=>$(id).textContent=t;
 const scenario=()=>$('scenario').value;
 function stop(){if(timer!==null)clearTimeout(timer);timer=null;running=false;$('pause').textContent='▶ Reanudar';}
 function labelRanges(){document.querySelectorAll('input[type=range]').forEach(e=>{let o=$(e.id+'-value');if(o)o.textContent=e.value;});}
 function record(obj){last=obj;history.push(obj);}
 function css(k){return getComputedStyle(document.documentElement).getPropertyValue(k).trim();}
 const cv=$('plot'),g=cv.getContext('2d'),W=cv.width,H=cv.height;
 function clear(){g.fillStyle=css('--bg');g.fillRect(0,0,W,H);g.font='17px system-ui';g.lineWidth=1;}
 function ln(x1,y1,x2,y2,col,width=2){g.strokeStyle=col;g.lineWidth=width;g.beginPath();g.moveTo(x1,y1);g.lineTo(x2,y2);g.stroke();}
 function chart(series,xmin,xmax,ymin,ymax,xlabel,ylabel){
  clear();if(ymax===ymin)ymax=ymin+1;let X=x=>65+(x-xmin)/(xmax-xmin)*(W-95),Y=y=>H-55-(y-ymin)/(ymax-ymin)*(H-95);
  g.fillStyle=css('--muted');for(let j=0;j<=4;j++){let x=xmin+j*(xmax-xmin)/4,y=ymin+j*(ymax-ymin)/4;ln(X(x),35,X(x),H-55,css('--grid'),1);ln(65,Y(y),W-30,Y(y),css('--grid'),1);g.fillText(fmt(x,1),X(x)-10,H-30);g.fillText(fmt(y,2),6,Y(y)+5);}
  series.forEach((s,i)=>{g.strokeStyle=css(['--a','--c','--b'][i]);g.lineWidth=3;g.beginPath();s.forEach(([x,y],j)=>j?g.lineTo(X(x),Y(y)):g.moveTo(X(x),Y(y)));g.stroke();if(s.length){const[x,y]=s.at(-1);g.beginPath();g.arc(X(x),Y(y),5,0,2*Math.PI);g.fillStyle=css(['--a','--c','--b'][i]);g.fill();}});
  g.fillStyle=css('--fg');g.fillText(xlabel,W-220,H-5);g.fillText(ylabel,65,22);return{X,Y};
 }
 function table(headers,rows){$('data').replaceChildren();const t=document.createElement('table'),head=t.createTHead().insertRow();headers.forEach(h=>{const e=document.createElement('th');e.scope='col';e.textContent=h;head.append(e);});const b=t.createTBody();rows.forEach(r=>{const row=b.insertRow();r.forEach(v=>row.insertCell().textContent=v);});$('data').append(t);}
 function renderPerceptron(){w=[val('w1'),val('w2'),val('bias')];const data=M.points(scenario()),errors=data.filter(p=>M.predict(p,w)!==p.label).length;clear();let X=x=>100+x*550,Y=y=>H-85-y*260;ln(80,H-60,W-50,H-60,css('--fg'));ln(80,H-60,80,35,css('--fg'));g.fillStyle=css('--muted');g.fillText('x₁ (0 a 1)',W-180,H-15);g.fillText('x₂ (0 a 1)',85,25);
  // La región usa los mismos pesos que la regla y se recorta al área del gráfico.
  g.save();g.beginPath();g.rect(80,35,W-130,H-95);g.clip();g.globalAlpha=.12;for(let x=0;x<=1.08;x+=.04)for(let y=0;y<=1.12;y+=.04){g.fillStyle=css(M.predict({x,y},w)?'--a':'--b');g.fillRect(X(x),Y(y),24,12);}g.globalAlpha=1;
  if(Math.abs(w[1])>1e-8)ln(X(-.04),Y((-w[0]*(-.04)-w[2])/w[1]),X(1.08),Y((-w[0]*1.08-w[2])/w[1]),css('--c'),3);else if(Math.abs(w[0])>1e-8)ln(X(-w[2]/w[0]),35,X(-w[2]/w[0]),H-60,css('--c'),3);g.restore();
  for(const p of data){g.fillStyle=css(p.label?'--a':'--b');g.beginPath();g.arc(X(p.x),Y(p.y),10,0,2*Math.PI);g.fill();g.fillStyle=css('--fg');g.fillText(`${p.x},${p.y}: ${p.label}`,X(p.x)-30,Y(p.y)+28);}
  put('stats',`Época ${step} · errores ${errors}/4 · exactitud ${100*(4-errors)/4}%`);put('interpret',scenario()==='xor'?'XOR no es separable: más épocas no amplían la capacidad de una sola neurona.':'Una época aplica la regla del perceptrón a los cuatro puntos, siempre en el mismo orden.');
  table(['x₁','x₂','Clase real','Predicción','z'],data.map(p=>[p.x,p.y,p.label,M.predict(p,w),fmt(p.x*w[0]+p.y*w[1]+w[2],3)]));last={epoch:step,w1:w[0],w2:w[1],b:w[2],errors};
 }
 function renderActivation(){let z=val('z'),fn=$('fn').value,[a,d]=M.activation(fn,z);let s=[[],[]];for(let j=0;j<=240;j++){let x=-6+j/20,v=M.activation(fn,x);s[0].push([x,v[0]]);if(v[1]!=null)s[1].push([x,v[1]]);}let all=s.flat().map(p=>p[1]),lo=Math.min(-1.2,...all),hi=Math.max(1.2,...all);let{X,Y}=chart(s,-6,6,lo,hi,'z (sin unidades)','Activación / derivada');ln(X(z),35,X(z),H-55,css('--b'),2);put('stats',`Paso ${step} · z=${fmt(z,2)} · φ(z)=${fmt(a)} · φ′(z)=${d==null?'no existe en z=0':fmt(d)}`);put('interpret',d===null?'En cero, ReLU y Leaky ReLU no son derivables. Una implementación adopta una convención.':Math.abs(d)<.01?'La derivada es pequeña: esta unidad transmite poca sensibilidad local.':'El cursor cambia z y recalcula la activación y la derivada de la función elegida.');table(['z','Activación','Derivada'],[[fmt(z),fmt(a),fmt(d)]]);last={step,z,activation:a,derivative:d,function:fn};}
 function currentGradient(){if(scenario()==='bce')return M.logistic(val('w'),val('b'));return{loss:.5*(val('w')-2)**2,gw:val('w')-2,gb:0};}
 function renderGradient(){let a=currentGradient();if(!losses.length)losses=[a.loss];let hi=Math.max(.01,...losses),lo=Math.min(0,...losses);chart([losses.map((y,j)=>[j,y])],0,Math.max(1,losses.length-1),lo,hi*1.05,'Iteración','Pérdida');put('stats',`Paso ${step} · w=${fmt(val('w'))} · b=${fmt(val('b'))} · pérdida=${fmt(a.loss,6)}`);put('interpret',`∂L/∂w=${fmt(a.gw,6)}; ∂L/∂b=${fmt(a.gb,6)}. ${scenario()==='unstable'?'En la parábola, η>2 amplifica el error.':'Un paso usa los gradientes del mismo estado previo.'}`);table(['Paso','w','b','Pérdida','∂L/∂w','∂L/∂b'],[[step,fmt(val('w')),fmt(val('b')),fmt(a.loss,6),fmt(a.gw,6),fmt(a.gb,6)]]);last={step,w:val('w'),b:val('b'),loss:a.loss,gw:a.gw,gb:a.gb,lr:val('lr')};}
 function renderThreshold(){let th=val('threshold'),r=M.confusion(cohort,th,val('benefit'),val('cost'),val('effect')),curve=Array.from({length:41},(_,j)=>[j/40,M.confusion(cohort,j/40,val('benefit'),val('cost'),val('effect')).utility]);let {X}=chart([curve],0,1,Math.min(0,...curve.map(x=>x[1])),Math.max(1,...curve.map(x=>x[1])),'Umbral','Utilidad proxy (UM)');ln(X(th),35,X(th),H-55,css('--c'),3);put('stats',`Umbral ${fmt(th,3)} · contactos ${r.contacts}/100 · recall ${r.recall==null?'no definido':fmt(100*r.recall,1)+'%'} · precision ${r.precision==null?'no definida':fmt(100*r.precision,1)+'%'} · U_proxy ${fmt(r.utility,2)} UM`);put('interpret',`U_proxy = TP·q·B − (TP+FP)·C. Semilla 991, datos sintéticos. q=${val('effect')} es un supuesto sobre efectividad, no una estimación causal. No optimizar con test real.`);table(['Real / acción','Contactar','No contactar'],[['Abandona',`TP ${r.TP}`,`FN ${r.FN}`],['No abandona',`FP ${r.FP}`,`TN ${r.TN}`]]);last={step,threshold:th,...r,B:val('benefit'),C:val('cost'),q:val('effect')};}
 function renderLSTM(){let vals=[{t:0,g:0,c:0,h:0}],c=0;for(let t=1;t<=step;t++){let q=M.lstm(val('forget'),val('input'),val('output'),M.candidate(scenario(),t),c);c=q.c;vals.push({t,g:M.candidate(scenario(),t),...q});}let max=Math.max(1,...vals.flatMap(v=>[Math.abs(v.c),Math.abs(v.h),Math.abs(v.g)]));chart(['c','h','g'].map(k=>vals.map(v=>[v.t,v[k]])),0,40,-max*1.1,max*1.1,'Paso temporal t','Estado (sin unidades)');const v=vals.at(-1);$('time').value=step;put('stats',`t=${step} · gₜ=${fmt(v.g,2)} · cₜ=${fmt(v.c,6)} · hₜ=${fmt(v.h,6)}`);put('interpret',`cₜ=f·cₜ₋₁+i·gₜ y hₜ=o·tanh(cₜ). Gates constantes: f=${val('forget')}, i=${val('input')}, o=${val('output')}. Modelo escalar didáctico con c₀=0; no entrena matrices LSTM.`);table(['t','gₜ','cₜ','hₜ'],vals.slice(-6).map(v=>[v.t,fmt(v.g),fmt(v.c),fmt(v.h)]));last={...v,f:val('forget'),i:val('input'),o:val('output')};}
 const renders={perceptron:renderPerceptron,activaciones:renderActivation,gradiente:renderGradient,umbral:renderThreshold,lstm:renderLSTM};
 function render(){labelRanges();renders[K]();put('status',running?'Ejecutando trayectoria reproducible':step?'En pausa o trayectoria terminada':'Estado inicial. Elegí un escenario e iniciá o avanzá un paso.');}
 function advance(){
  if(step>=40){stop();render();return false;}
  if(K==='perceptron'){w=M.perceptron(scenario(),[val('w1'),val('w2'),val('bias')],val('eta'));['w1','w2','bias'].forEach((k,j)=>$(k).value=w[j]);}
  if(K==='activaciones'){const t=(step+1)/40;let z=scenario()==='saturation'?3+3*t:scenario()==='kink'?-1+2*t:-6+12*t;$('z').value=z;}
  if(K==='gradiente'){let a=currentGradient(),nw=val('w')-val('lr')*a.gw,nb=val('b')-val('lr')*a.gb;if(!Number.isFinite(nw)||Math.abs(nw)>1e12||!Number.isFinite(nb)){stop();put('error','Trayectoria detenida: parámetros fuera del rango numérico de demostración. Reiniciá con una tasa menor.');return false;}$('w').value=nw;$('b').value=nb;losses.push(currentGradient().loss);}
  if(K==='umbral')$('threshold').value=(step+1)/40;
  step++;render();record(last);if(step>=40){stop();render();}return true;
 }
 function schedule(){if(!running)return;const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;timer=setTimeout(()=>{timer=null;advance();if(running)schedule();},(reduced?1500:650)/val('speed'));}
 function start(){stop();if(step>=40)reset(false);running=true;$('pause').textContent='⏸ Pausar';render();schedule();}
 function reset(defaults=true){stop();step=0;history=[];losses=[];put('error','');if(defaults){
  if(K==='perceptron'){['w1','w2','bias'].forEach((k,j)=>$(k).value=[-.5,.2,-.1][j]);$('eta').value=.15;}
  if(K==='activaciones'){$('z').value=scenario()==='saturation'?3:scenario()==='kink'?-1:-6;$('fn').value=scenario()==='kink'?'relu':'sigmoid';}
  if(K==='gradiente'){$('w').value=-.5;$('b').value=.2;$('lr').value=scenario()==='bce'?.3:scenario()==='unstable'?2.2:.6;}
  if(K==='umbral'){$('threshold').value=0;$('benefit').value=100;$('cost').value=scenario()==='costly'?20:5;$('effect').value=scenario()==='weak'?.05:.4;}
  if(K==='lstm'){$('forget').value=.9;$('input').value=.5;$('output').value=.75;}
 }render();record(last);}
 $('auto').onclick=start;$('pause').onclick=()=>{if(running){stop();render();}else start();};$('nextstep').onclick=()=>{stop();advance();};$('reset').onclick=()=>reset(true);$('scenario').onchange=()=>reset(true);$('speed').onchange=()=>{if(running){stop();running=true;$('pause').textContent='⏸ Pausar';schedule();}};
 document.querySelectorAll('.manual').forEach(e=>e.addEventListener('input',()=>{stop();step=0;history=[];losses=[];if(e.id==='time')step=val('time');render();record(last);}));
 document.addEventListener('themechange',render);document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();render();}});window.addEventListener('pagehide',stop);
 $('full').onclick=()=>toggleFullscreen($('lab-main'));
 $('csv').onclick=()=>{let rows=K==='umbral'?Array.from({length:41},(_,j)=>({threshold:j/40,...M.confusion(cohort,j/40,val('benefit'),val('cost'),val('effect')),B:val('benefit'),C:val('cost'),q:val('effect')})):history;const keys=[...new Set(rows.flatMap(Object.keys))],quote=x=>'"'+String(x??'').replaceAll('"','""')+'"',csv=[keys,...rows.map(r=>keys.map(k=>r[k]))].map(r=>r.map(quote).join(',')).join('\r\n'),url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=`uca-${K}-sintetico.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),0);};
 window.labDebug={get state(){return{step,running,timers:timer===null?0:1,history:[...history],last};},advance,reset};reset(true);
})();
