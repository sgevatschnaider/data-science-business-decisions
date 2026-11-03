import {createRequire} from 'node:module';
const M=createRequire(import.meta.url)('./math.cjs');
export const sceneKinds=new Set(['xor-map','calculation-graph','chain-graph','gradient-graph','update-graph','hidden-gradient','parabola','capacity','shrinkage','dropout-mask','checkpoint','confusion-large','roc-pr','utility-flow','window-timeline','rnn-unroll','rnn-numeric','bptt','gradient-scale','cell-flow','forget-gate','write-gate','cell-update','output-gate','all-gates','cell-numeric','output-numeric','memory-curves','memory-gradient','walk-forward','seasonal-baseline','metric-errors']);
export function drawScene(s,n,{text,line,node,C,font}){
 const T=(v,x,y,w=400,h=42,size=24,c=C.fg,b=false)=>text(s,v,x,y,w,h,size,c,b);
 const box=(label,value,x,y,w=235,color=C.a)=>{s.shapes.add({geometry:'roundRect',position:{left:x,top:y,width:w,height:120},fill:'#0d1827',line:{fill:color,width:1.5}});T(label,x+16,y+12,w-32,42,18,C.muted);T(value,x+16,y+57,w-32,60,value.length>20?20:24,color,true);};
 const arrow=(x,y,z,color=C.a)=>{const d=z>x?1:-1;line(s,x,y,z-9*d,y,color,3);line(s,z-18*d,y-7,z-9*d,y,color,3);line(s,z-18*d,y+7,z-9*d,y,color,3);};
 const axisTitle=t=>({text:t,textStyle:{typeface:'DejaVu Sans',fontSize:18,fill:C.muted}});
 const chart=(x,y,w,h,series,xt,yt,opt={})=>{const q=s.charts.add('scatter',{position:{left:x,top:y,width:w,height:h},series:series.map((r,i)=>({name:r.name,smooth:false,xValues:r.x.map(v=>+v.toFixed(6)),values:r.y.map(v=>v===null?null:+v.toFixed(6)),line:{fill:r.color||[C.a,C.c,C.b][i%3],width:r.points?0:2.5},marker:{symbol:r.points?'circle':'none',size:r.points?8:2,fill:r.color||C.b}})),scatterOptions:{style:'lineWithMarkers'},hasLegend:series.length>1,legend:{position:'bottom',textStyle:{typeface:'DejaVu Sans',fontSize:17,fill:C.fg}},xAxis:{title:axisTitle(xt),textStyle:{typeface:'DejaVu Sans',fontSize:17,fill:C.muted},...opt.xAxis},yAxis:{title:axisTitle(yt),textStyle:{typeface:'DejaVu Sans',fontSize:17,fill:C.muted},majorGridlines:{fill:'#28435f',width:1},...opt.yAxis},chartFill:C.bg,plotAreaFill:C.bg,chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}});font(q,{fontFamily:'DejaVu Sans'});return q;};
 const flow=(labels,values,colors=[C.b,C.a,C.c,C.a])=>{const w=230,gap=65,start=64;labels.forEach((v,i)=>{box(v,values[i],start+i*(w+gap),300,w,colors[i%colors.length]);if(i<labels.length-1)arrow(start+i*(w+gap)+w,350,start+(i+1)*(w+gap)-8);});};
 const v=n.visual,steps=Array.from({length:21},(_,i)=>i);
 if(v==='xor-map'){
  T('Entradas originales',86,245,440,40,26,C.b,true);T('Representación con dos ReLU',700,245,490,40,26,C.a,true);
  for(const [off,maxX,kind] of [[110,1,false],[740,2,true]]){let X=x=>off+x*170,Y=y=>490-y*150;line(s,off-20,510,off+365,510);line(s,off-20,510,off-20,290);for(const p of M.points('xor')){let h=M.xorRepresentation(p.x,p.y),a=kind?h.h1:p.x,b=kind?h.h2:p.y;node(s,String(p.label),X(a),Y(b),p.label?C.a:C.b,21);}T(kind?'h₁':'x₁',off+340,515,70,30,20);T(kind?'h₂':'x₂',off-55,285,70,30,20);if(kind)line(s,X(.5),Y(0),X(2),Y(.75),C.c,3);}
  arrow(540,385,655,C.muted);T('h₁ = ReLU(x₁+x₂)\nh₂ = ReLU(x₁+x₂−1)',475,430,240,90,21,C.muted);T('Clase 1: cian · clase 0: violeta · frontera: h₁−2h₂ = 0,5',85,555,1120,40,22,C.c);return;
 }
 if(['calculation-graph','chain-graph','gradient-graph','update-graph'].includes(v)){
  const q=M.singleNeuron(2,1,.3,-.1,.1);
  flow(['Entrada y parámetros','Logit z = wx+b','Probabilidad σ(z)','BCE con y = 1'],['x=2 · w=0,3 · b=−0,1','0,500000','0,622459','0,474077']);
  if(v==='calculation-graph')T('El forward conserva los valores intermedios para calcular derivadas después.',86,455,1100,65,27,C.muted);
  if(v==='chain-graph'){T('∂L/∂p = −1/p',80,440,330,45,27,C.c,true);T('∂p/∂z = p(1−p)',450,440,350,45,27,C.c,true);T('∂z/∂w = x = 2',850,440,345,45,27,C.c,true);T('Producto: ∂L/∂w = (p−y)x = −0,755081',80,500,1120,45,30,C.a,true);}
  if(v==='gradient-graph'){T('La señal vuelve desde la pérdida',80,440,600,45,25,C.muted);T('δ = p−y = −0,377541',80,495,525,45,29,C.c,true);T('∂L/∂w = −0,755081     ∂L/∂b = −0,377541',620,495,570,80,26,C.a,true);}
  if(v==='update-graph'){box('Actualización con η=0,1','w′ = 0,375508',80,445,340,C.a);box('Actualización del sesgo','b′ = −0,062246',465,445,340,C.b);box('Nuevo forward','BCE′ = 0,406926',850,445,340,C.c);}return;
 }
 if(v==='hidden-gradient'){
  flow(['Salida p y etiqueta y','Transporte por W₂ᵀ','Error oculto δ₁','Gradiente de W₁'],['δ₂ = p−y','W₂ᵀδ₂','(W₂ᵀδ₂) ⊙ φ′(z₁)','δ₁xᵀ']);
  T('W₂ reparte la señal hacia la capa oculta. φ′ modula cuánto atraviesa cada unidad.',85,455,1100,80,28,C.muted);T('Una ReLU inactiva tiene derivada 0 en z<0 y bloquea esa contribución local.',85,535,1100,50,23,C.c);return;
 }
 if(v==='parabola'){
  const ss=[.2,1.4,2.2].map((eta,i)=>({name:'η = '+eta.toLocaleString('es'),x:steps.slice(0,11),y:steps.slice(0,11).map(k=>-2*(1-eta)**k),color:[C.a,C.b,C.c][i]}));
  chart(64,245,760,330,ss,'Iteración k','Error wₖ−2');T('L(w) = ½(w−2)²',870,270,330,55,30,C.a,true);T('0 < η < 2\nconverge\n\nη > 2\noscila y se aleja',870,340,330,220,27,C.muted);return;
 }
 if(v==='capacity'){
  const fit=M.fitExperiment(9,0),xs=fit.curve.map(p=>p.x);
  chart(64,245,740,335,[{name:'Generadora',x:xs,y:fit.curve.map(p=>p.truth),color:C.muted},...[1,3,9].map((d,i)=>{const z=M.fitExperiment(d,0);return{name:'Grado '+d,x:xs,y:z.curve.map(p=>p.y),color:[C.c,C.a,C.b][i]};})],'x','y');
  T('MSE en validación',845,265,360,40,26,C.fg,true);[1,3,9].forEach((d,i)=>T('Grado '+d+'     '+M.fitExperiment(d,0).validMSE.toFixed(4),845,330+i*65,350,40,27,[C.c,C.a,C.b][i],true));T('12 puntos train · 60 valid\nSemilla 42 · λ=0',845,535,360,55,19,C.muted);return;
 }
 if(v==='shrinkage'){
  const x=Array.from({length:41},(_,i)=>i/10);chart(64,245,740,335,[{name:'Óptimo w*',x,y:x.map(l=>2/(1+l))}],'Penalización λ','Peso óptimo');T('J = ½(w−2)² + ½λw²',855,280,350,80,28,C.a,true);T('λ=0     w*=2\nλ=1     w*=1\nλ=3     w*=0,5',855,390,350,140,27,C.muted);return;
 }
 if(v==='dropout-mask'){
  T('Activaciones h',80,265,300,40,26,C.muted);T('Máscara Bernoulli',465,265,330,40,26,C.muted);T('Salida durante train',850,265,350,40,26,C.muted);
  flow(['Antes del dropout','Retención 1−p = 0,5','Escalado invertido'],['[0,2 · 0,4 · 0,6]','máscara [1 · 0 · 1]','[0,4 · 0 · 1,2]']);T('Cada activación conservada se divide por 1−p. En inferencia se usa la red completa.',80,465,1110,90,29,C.c);return;
 }
 if(v==='checkpoint'){
  const tr=[1,.8,.65,.51,.42,.34,.28,.23,.19,.16,.13],va=[1,.83,.72,.63,.59,.61,.65,.72,.81,.91,1.02],x=tr.map((_,i)=>i);
  chart(64,245,770,335,[{name:'Train (ilustración)',x,y:tr},{name:'Validación (ilustración)',x,y:va},{name:'Mejor checkpoint',x:[4],y:[.59],points:true,color:C.b}],'Época','Pérdida');T('Se conserva la época 4',865,285,330,80,32,C.a,true);T('El mínimo de validación\nselecciona el checkpoint.\n\nTest se consulta al final.',865,390,330,160,25,C.muted);return;
 }
 if(v==='confusion-large'){
  const tb=s.tables.add({rows:3,columns:3,left:90,top:270,width:730,height:265,values:[['Real / Acción','Contactar','No contactar'],['Abandona','TP = 3','FN = 2'],['No abandona','FP = 7','TN = 88']]});for(let r=0;r<3;r++)for(let c=0;c<3;c++){const q=tb.getCell(r,c);q.text.style={fontSize:24,typeface:'DejaVu Sans',color:r?C.fg:C.a};q.fill=r===0?'#12243a':'#0d1827';}
  T('Recall = 3/5 = 60%',865,295,340,70,28,C.a,true);T('Precisión = 3/10 = 30%',865,385,340,80,28,C.c,true);T('100 clientes sintéticos\nEjemplo manual de conteo',865,490,340,65,22,C.muted);return;
 }
 if(v==='roc-pr'){
  const co=M.cohort(991),q=[Infinity,...[...new Set(co.map(p=>p.p))].sort((a,b)=>b-a),-Infinity].map(t=>M.confusion(co,t));
  chart(64,250,550,320,[{name:'ROC',x:q.map(r=>r.FP/(r.FP+r.TN)),y:q.map(r=>r.recall)},{name:'Azar',x:q.map(r=>r.FP/(r.FP+r.TN)),y:q.map(r=>r.FP/(r.FP+r.TN)),color:C.muted}],'FPR','TPR');const pr=q.filter(r=>r.precision!==null);
  chart(665,250,550,320,[{name:'Precision–Recall',x:pr.map(r=>r.recall),y:pr.map(r=>r.precision),color:C.b},{name:'Prevalencia',x:pr.map(r=>r.recall),y:pr.map(()=>co.filter(p=>p.y).length/co.length),color:C.muted}],'Recall','Precisión');T('Mismos 100 scores sintéticos, semilla 991. Ninguna curva incorpora por sí sola el costo de actuar.',80,575,1120,32,20,C.muted);return;
 }
 if(v==='utility-flow'){
  flow(['Beneficio supuesto','Costo de contactar','Utilidad proxy'],['TP × q × B','(TP+FP) × C','TPqB − (TP+FP)C']);T('Ejemplo: TP=3, FP=7, q=0,4, B=100 UM, C=5 UM',80,455,1110,45,28,C.muted);T('Beneficio 120 UM − costo 50 UM = 70 UM',80,515,1110,50,34,C.a,true);return;
 }
 if(v==='window-timeline'){
  [10,12,11,14,15].forEach((z,i)=>{box(i<4?'Entrada t−'+(3-i):'Objetivo t+1',String(z),80+i*225,305,190,i<4?C.a:C.c);});T('Ventana observada: [10, 12, 11, 14]',80,455,760,60,32,C.a,true);T('El objetivo 15 queda fuera de las entradas.',80,525,1100,45,27,C.muted);return;
 }
 if(['rnn-unroll','rnn-numeric','bptt'].includes(v)){
  const xs=[250,630,1010];xs.forEach((x,i)=>{node(s,'h'+(v==='rnn-numeric'?i:i+1),x,355,C.a,46);if(v!=='rnn-numeric'||i>0){T('x'+(v==='rnn-numeric'?i:i+1),x-30,475,100,40,28,C.b,true);line(s,x,465,x,405,C.b,2);}if(v==='rnn-numeric')T(['0','0,761594','0,363399'][i],x-100,405,250,40,25,C.c,true);if(i<2)arrow(x+50,355,xs[i+1]-55);T('Mismos Wₓ, Wₕ, b',x-120,255,270,40,21,C.muted);});
  if(v==='bptt'){arrow(585,420,300,C.c);arrow(965,420,680,C.c);T('El gradiente acumula contribuciones de todos los pasos sobre los pesos compartidos.',80,550,1120,55,25,C.c);}
  else if(v==='rnn-numeric')T('h₀=0 · Wₓ=1 · Wₕ=0,5 · b=0 · x₁=1 · x₂=0    ⇒    h₂=0,363399',80,550,1120,55,24,C.c);
  else T('hₜ = tanh(Wₓxₜ + Wₕhₜ₋₁ + b)',80,550,1120,55,30,C.c,true);return;
 }
 if(v==='gradient-scale'){
  chart(64,245,770,335,[{name:'0,5ᵏ',x:steps,y:steps.map(k=>.5**k)},{name:'1,1ᵏ',x:steps,y:steps.map(k=>1.1**k)}],'Pasos k','Producto de sensibilidades');T('El producto importa',865,280,330,80,32,C.a,true);T('Factores menores que 1\npueden extinguir la señal.\n\nFactores mayores que 1\npueden amplificarla.',865,380,330,180,25,C.muted);return;
 }
 if(['cell-flow','forget-gate','write-gate','cell-update','output-gate','all-gates','cell-numeric','output-numeric'].includes(v)){
  if(v==='all-gates'){
   [['fₜ = σ(Wf [hₜ₋₁,xₜ]+bf)','iₜ = σ(Wi [hₜ₋₁,xₜ]+bi)'],['gₜ = tanh(Wg [hₜ₋₁,xₜ]+bg)','oₜ = σ(Wo [hₜ₋₁,xₜ]+bo)'],['cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ gₜ','hₜ = oₜ ⊙ tanh(cₜ)']].forEach((row,j)=>row.forEach((q,i)=>T(q,80+i*585,275+j*100,555,65,25,j===2?C.c:i?C.b:C.a,true)));return;
  }
  box('Retener: f × c anterior','0,9 × 0,8 = 0,72',80,270,330,v==='forget-gate'?C.c:C.a);
  box('Escribir: i × g','0,2 × (−0,5) = −0,10',80,430,330,v==='write-gate'?C.c:C.b);
  line(s,410,330,475,330,C.a,3);line(s,475,330,475,390,C.a,3);line(s,410,490,475,490,C.b,3);line(s,475,490,475,450,C.b,3);node(s,'+',475,420,C.c,28);arrow(505,420,530);
  box('Memoria c: retener + escribir','0,72 − 0,10 = 0,62',540,360,325,['cell-update','cell-numeric'].includes(v)?C.c:C.a);arrow(865,420,905);
  box('Exponer: o × tanh(c)','0,75 × 0,5511 = 0,4133',915,360,285,['output-gate','output-numeric'].includes(v)?C.c:C.b);
  const captions={'forget-gate':'f decide qué fracción del estado anterior conserva la celda.','write-gate':'i regula la escritura. g aporta un contenido que también puede ser negativo.','cell-update':'Conservar y escribir se suman en una vía aditiva.','output-gate':'o regula el estado expuesto h. Cerrar o no borra c.','cell-numeric':'Memoria: 0,72 retenido + (−0,10) escrito = 0,62.','output-numeric':'La memoria c=0,62 permanece mientras h expone solo 0,413346.','cell-flow':'La memoria c circula entre pasos. El estado h comunica una parte transformada.'};T(captions[v],80,570,1110,38,21,C.muted);return;
 }
 if(['memory-curves','memory-gradient'].includes(v)){
  chart(64,245,770,335,[{name:'f=0,9',x:steps,y:steps.map(k=>(v==='memory-curves'?.5:1)*.9**k)},{name:'f=0,5',x:steps,y:steps.map(k=>(v==='memory-curves'?.5:1)*.5**k)}],'Pasos desde el impulso',v==='memory-curves'?'Estado c':'Vía directa ∂cₜ/∂c₀');T(v==='memory-curves'?'Sin nueva escritura':'Producto directo de f',865,280,330,90,30,C.a,true);T(v==='memory-curves'?'c₀=0,5, i=0\nLa retención controla\nla escala temporal.':'Gates tratados constantes.\nLa derivada total también\nincluye sus dependencias.',865,400,330,150,25,C.muted);return;
 }
 if(v==='walk-forward'){
  const X=i=>90+i/420*1100;[300,320,340].forEach((o,i)=>{const y=300+i*90;line(s,X(0),y,X(o),y,C.a,18);line(s,X(o+1),y,X(o+14),y,C.c,18);T('Origen '+o,80,y+19,1100,40,21,C.muted);});T('Historia creciente (cian) y horizonte de validación de 14 pasos (ámbar).',80,565,1110,40,23,C.muted);return;
 }
 if(v==='seasonal-baseline'){
  const x=Array.from({length:28},(_,i)=>i),sig=x.map(i=>10+.15*i+2*Math.sin(2*Math.PI*i/7));chart(64,245,770,335,[{name:'Observado sintético',x,y:sig},{name:'Naive estacional s=7',x:x.slice(7),y:sig.slice(0,-7),color:C.c}],'Día t','Demanda (unidades)');T('ŷₜ = yₜ₋₇',865,285,330,70,36,C.a,true);T('Usa el mismo día\nde la semana previa.\n\nUna tendencia genera\nerrores sistemáticos.',865,385,330,170,25,C.muted);return;
 }
 if(v==='metric-errors'){
  flow(['Errores absolutos','MAE','RMSE'],['2, 5, 5','(2+5+5)/3 = 4','√((4+25+25)/3) = 4,243']);T('MAE y RMSE mantienen la unidad del objetivo. RMSE amplifica errores grandes.',80,465,1110,90,29,C.muted);T('MAPE queda indefinido cuando un valor real es cero.',80,555,1110,40,24,C.c);return;
 }
}
