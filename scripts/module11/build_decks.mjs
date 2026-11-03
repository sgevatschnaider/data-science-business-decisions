import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const artifactEntry=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?pathToFileURL(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'@oai/artifact-tool/dist/artifact_tool.mjs')).href:'@oai/artifact-tool';
const {Presentation,PresentationFile}=await import(artifactEntry);

const root=path.resolve(import.meta.dirname,'../..');
const workspace=path.resolve(root,'..');
const base=path.join(root,'docs/modulos/11-redes-neuronales/experiencia');
const data=JSON.parse(await fs.readFile(path.join(import.meta.dirname,'decks.json'),'utf8'));
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL('/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs').href);
const C={bg:'#091321',fg:'#F0F5FA',muted:'#B9C7D8',a:'#55E3D1',b:'#B8A3FF',c:'#FFC77B',line:'#4D617B'};
function text(s,value,x,y,w,h,size=28,color=C.fg,bold=false){
 const sh=s.shapes.add({geometry:'textbox',name:value.slice(0,35),position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});
 sh.text=value;sh.text.style={fontSize:size,typeface:'DejaVu Sans',color,bold,verticalAlignment:'top',wrap:'square',autoFit:'none',insets:0};return sh;
}
function line(s,x1,y1,x2,y2,color=C.line,width=2){return s.shapes.add({geometry:'line',position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.max(1,Math.abs(x2-x1)),height:Math.max(1,Math.abs(y2-y1)),verticalFlip:y2<y1},fill:'none',line:{style:'solid',fill:color,width}});}
function node(s,label,x,y,color=C.a,r=28){s.shapes.add({geometry:'ellipse',name:'nodo-'+label,position:{left:x-r,top:y-r,width:2*r,height:2*r},fill:C.bg,line:{style:'solid',fill:color,width:2}});text(s,label,x-r,y-15,2*r,35,22,color,true).text.alignment='center';}
function network(s,n){const two=n?.title.includes("XOR con");const cols=[[795,[285,390]],[975,two?[300,430]:[250,355,460]],[1160,[355]]];for(let k=0;k<2;k++)for(let y of cols[k][1])for(let z of cols[k+1][1])line(s,cols[k][0]+28,y,cols[k+1][0]-28,z);for(let [k,[x,ys]] of cols.entries())for(let [j,y] of ys.entries())node(s,(k===0?'x':k===1?'h':'p')+(k===2?'':j+1),x,y,k===0?C.b:C.a);['Entradas','Oculta','Salida'].forEach((v,i)=>text(s,v,cols[i][0]-60,520,125,40,22,C.muted));}
function plot(s,categories,series,yTitle,xTitle='z'){
 const axisTitle=t=>({text:t,textStyle:{typeface:'DejaVu Sans',fontSize:21,fill:C.muted}});
 const chart=s.charts.add('line',{position:{left:750,top:230,width:470,height:340},categories,series:series.map((q,i)=>({name:q.name,values:q.values.map(v=>Number(v.toFixed(6))),line:{style:'solid',fill:[C.a,C.c,C.b][i],width:3}})),hasLegend:series.length>1,legend:{position:'bottom',textStyle:{typeface:'DejaVu Sans',fontSize:22,fill:C.fg}},xAxis:{title:axisTitle(xTitle),textStyle:{typeface:'DejaVu Sans',fontSize:22,fill:C.muted},line:{style:'solid',fill:C.line,width:1}},yAxis:{title:axisTitle(yTitle),textStyle:{typeface:'DejaVu Sans',fontSize:22,fill:C.muted},majorGridlines:{style:'solid',fill:'#25344A',width:1}},chartFill:C.bg,plotAreaFill:C.bg,chartLine:{style:'solid',fill:'none',width:0},plotAreaLine:{style:'solid',fill:'none',width:0}});applyPresentationChartFont(chart,{fontFamily:'DejaVu Sans'});return chart;
}
function diagram(s,v,n){
 if(v==='network'){network(s,n);return;}
 if(v==='architecture'){const labels=n.title.includes('RNN,')?[['RNN','Estado recurrente'],['LSTM / GRU','Gates y recurrencia'],['Transformer','Atención y posición']]:[['MLP','Atributos'],['CNN','Estructura local'],['RNN / LSTM','Secuencia'],['Transformer','Atención']];labels.forEach(([a,b],i)=>{text(s,a,775,240+i*80,440,40,29,C.a,true);text(s,b,775,277+i*80,440,40,24,C.muted);});return;}
 if(['sigmoid','activations','bce'].includes(v)){
  const z=Array.from({length:13},(_,i)=>i-6);let series=[];
  if(v==='sigmoid')series=[{name:'σ(z)',values:z.map(x=>1/(1+Math.exp(-x)))},{name:'σ′(z)',values:z.map(x=>{let p=1/(1+Math.exp(-x));return p*(1-p)})}];
  if(v==='activations')series=[{name:'ReLU',values:z.map(x=>Math.max(0,x))},{name:'tanh',values:z.map(Math.tanh)}];
  if(v==='bce'){const p=[.05,.2,.4,.6,.8,.95];plot(s,p.map(String),[{name:'BCE con y=1',values:p.map(x=>-Math.log(x))}],'Pérdida (nats)','p');return;}
  plot(s,z.map(String),series,'Valor / derivada');return;
 }
 if(['overfit','memory','gradient','lr','descent'].includes(v)){
  let x=Array.from({length:11},(_,i)=>i),ser,y='Magnitud',xt='Paso';
  if(v==='overfit'){ser=[{name:'Train (esquema)',values:[1,.8,.65,.51,.42,.34,.28,.23,.19,.16,.13]},{name:'Validación (esquema)',values:[1,.83,.72,.63,.59,.61,.65,.72,.81,.91,1.02]}];y='Pérdida';xt='Época';}
  if(v==='memory'){ser=[{name:'f=0,9',values:x.map(i=>.5*.9**i)},{name:'f=0,5',values:x.map(i=>.5*.5**i)}];y='c (sin unidades)';}
  if(v==='gradient'){ser=[{name:'0,5ᵏ',values:x.map(i=>.5**i)},{name:'1,1ᵏ',values:x.map(i=>1.1**i)}];y='Sensibilidad hipotética';}
  if(v==='lr'){ser=[{name:'η=0,2',values:x.map(i=>-2*.8**i)},{name:'η=1,8',values:x.map(i=>-2*(-.8)**i)}];y='w−2';}
  if(v==='descent'){let w=.3,b=-.1,vals=[];for(let i=0;i<11;i++){let z=2*w+b,p=1/(1+Math.exp(-z));vals.push(Math.log1p(Math.exp(-z)));w-=.1*(p-1)*2;b-=.1*(p-1);}ser=[{name:'BCE de la neurona',values:vals}];y='BCE (nats)';}
  plot(s,x.map(String),ser,y,xt);return;
 }
 if(v==='xor'||v==='boundary'){
  line(s,800,515,1180,515);line(s,800,515,800,235);text(s,'x₁',1170,530,45,40,24);text(s,'x₂',760,220,45,40,24);
  const pts=[[840,470,0],[840,285,1],[1125,470,1],[1125,285,v==='xor'?0:1]];
  for(let [x,y,l]of pts){node(s,String(l),x,y,l?C.a:C.b,22);}
  if(v==='boundary')line(s,810,300,1140,505,C.c,3);
  text(s,v==='xor'?'Clase 0: violeta / Clase 1: cian':'Frontera: wᵀx+b=0',790,580,440,40,22,C.muted);return;
 }
 if(v==='confusion'){
  const t=s.tables.add({rows:3,columns:3,left:755,top:260,width:460,height:240,values:[['Real / Acción','Contactar','No contactar'],['Abandona','TP 3','FN 2'],['No abandona','FP 7','TN 88']]});
  for(let r=0;r<3;r++)for(let c=0;c<3;c++){let cell=t.getCell(r,c);cell.text.style={fontSize:21,typeface:'DejaVu Sans',color:C.fg};cell.fill=r===0?'#263750':C.bg;}
  text(s,'100 clientes · ejemplo sintético',760,530,450,45,23,C.c);return;
 }
 if(v==='lstm'){
  text(s,'Memoria anterior',785,218,400,40,24,C.muted);node(s,'c',815,315,C.a);line(s,845,315,950,315,C.a,3);node(s,'×f',980,315,C.b,35);line(s,1015,315,1090,315,C.a,3);node(s,'+',1120,315,C.a,30);line(s,1120,440,1120,345,C.b,3);text(s,'i ⊙ g',1040,452,170,50,30,C.b,true);line(s,1150,315,1210,315,C.a,3);text(s,'cₜ',1170,345,70,40,26,C.a,true);text(s,'hₜ = oₜ ⊙ tanh(cₜ)',775,545,450,60,29,C.c,true);return;
 }
 if(v==='recurrent'||v==='sequence'||v==='windows'){
  for(let j=0;j<3;j++){let x=805+j*170;node(s,'h'+(j+1),x,355,C.a,35);text(s,'x'+(j+1),x-25,480,60,40,26,C.b);line(s,x,470,x,390,C.b,2);if(j<2)line(s,x+35,355,x+135,355,C.a,3);}
  text(s,'Mismos pesos en cada paso',775,230,455,65,27,C.muted);text(s,'Tiempo / posición',800,565,400,40,24,C.c);return;
 }
 if(v==='split'||v==='walkforward'||v==='timeline'){
  const labels=v==='timeline'&&n.number===4?['9:30 · concepto','10:15 · cálculo','11:05 · decisión']:['Pasado · train','Posterior · valid','Futuro · test'];
  for(let j=0;j<3;j++){let y=260+j*105;line(s,790,y,1190,y,[C.a,C.b,C.c][j],9);text(s,labels[j],790,y+18,430,60,28,[C.a,C.b,C.c][j]);}return;
 }
 if(v==='neuron'||v==='chain'||v==='flow'){
  const labels=v==='neuron'?['wᵀx+b','φ(z)','a']:v==='chain'?['∂z/∂w','∂p/∂z','∂L/∂p']:['z','p','L'];
  labels.forEach((q,j)=>{text(s,q,785,245+j*110,410,60,38,[C.b,C.a,C.c][j],true);if(j<2)line(s,1050,285+j*110,1050,335+j*110,C.line,2);});return;
 }
 if(v==='calibration'){plot(s,['0','0,2','0,4','0,6','0,8','1'],[{name:'Calibración ideal',values:[0,.2,.4,.6,.8,1]}],'Frecuencia positiva','Probabilidad');return;}
 if(v==='imbalance'){text(s,'95%',790,245,410,120,100,C.a,true);text(s,'accuracy del clasificador trivial',790,380,420,90,28,C.muted);text(s,'0 / 5 abandonos detectados',790,505,420,85,30,C.c,true);return;}
 if(v==='numeric'){const num=n.title.includes('Inferencia')?'0,622459':n.title.includes('MSE')?'4 unidades²':n.title.includes('Backpropagation')?'−0,755081':n.title.includes('Umbral')?'70 UM':n.title.includes('Parámetros de una RNN')?'22 parámetros':n.title.includes('Forward de una RNN')?'h₂ = 0,363399':n.title.includes('conservar y escribir')?'cₜ = 0,62':n.title.includes('exponer')?'hₜ = 0,413346':n.title.includes('Conteo')?'72 parámetros':'Cálculo verificable';text(s,num,785,285,420,180,42,C.a,true);text(s,'Valores didácticos verificables',785,520,430,70,25,C.muted);return;}
 if(v==='exercise'){const lab=n.title.includes('Laboratorio');text(s,lab?'Antes de simular':'Defensa con evidencia',785,255,430,90,35,C.a,true);text(s,lab?'1  Predecir\n2  Observar\n3  Explicar':'1  Protocolo\n2  Resultado\n3  Límites',785,365,430,190,35,C.fg);return;}
 if(v==='utility'){text(s,'Beneficio supuesto',780,245,440,60,30,C.a,true);text(s,'TP × q × B',780,315,440,65,38,C.a);text(s,'Costo de todos los contactos',780,415,440,70,27,C.c,true);text(s,'(TP + FP) × C',780,505,440,65,38,C.c);return;}
 if(v==='batches'){for(let j=0;j<5;j++){text(s,String(j+1),800+j*75,315,60,60,34,C.a,true);}text(s,'Un lote por actualización',785,430,430,75,30,C.muted);text(s,'Todos los lotes: una época',785,520,430,75,27,C.c);return;}
 if(v==='metrics'){plot(s,['0','.2','.4','.6','.8','1'],[{name:'ROC ilustrativa',values:[0,.6,.78,.88,.96,1]},{name:'Referencia',values:[0,.2,.4,.6,.8,1]}],'TPR','FPR');return;}
 text(s,v==='compare'?'Comparación con evidencia':'Datos → modelo → política',780,260,440,100,35,C.a,true);text(s,'Mismo protocolo\nCosto explícito\nValidación separada',780,405,440,160,30,C.muted);
}

for(const d of data){
 const dir=path.join(base,d.slug),tmp=path.join(workspace,'build',d.slug);await fs.mkdir(path.join(dir,'slides/es'),{recursive:true});await fs.mkdir(path.join(dir,'downloads'),{recursive:true});await fs.mkdir(tmp,{recursive:true});
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 for(const n of d.slides){
  const s=p.slides.add();s.background.fill=C.bg;
  const cover=n.number===1;
  text(s,'UCA · CIENCIAS DE DATOS II',64,25,650,30,17,C.a,true);
  text(s,n.essential?'RUTA ESENCIAL':'AMPLIACIÓN',990,25,230,30,15,C.muted);
  text(s,n.title,64,cover?115:80,cover?685:1150,cover?200:115,cover?64:40,C.fg,true);
  const has=!!n.visual;const width=has?650:1130;
  let y=cover?355:210;
  if(n.equation){const lines=n.equation.split('\n').length;const h=Math.max(65,lines*38);text(s,n.equation,64,y,width,h,has?27:31,C.a,true);y+=h+25;}
  for(const b of n.body){text(s,b,64,y,cover?670:width,cover?54:67,cover?25:25,C.muted);y+=cover?65:78;}
  if(has)diagram(s,n.visual,n);
  if(!cover){line(s,64,620,1216,620,'#31435B',1);text(s,n.question,64,641,1140,45,23,C.c);}
  text(s,'Sergio Gevatschnaider · '+(d.slug.includes('fundamentos')?'Fundamentos':'RNN / LSTM'),64,696,750,20,12,C.muted);
  text(s,String(n.number).padStart(2,'0')+' / '+d.slides.length,1120,690,100,25,16,C.muted);
  s.speakerNotes.text=[n.notes,'\nFUENTES',...n.sources.map(x=>x.label+(x.url?'\n'+x.url:'')),'\nTRANSCRIPCIÓN',n.transcript].join('\n');
 }
 const draft=path.join(tmp,'draft.pptx');await(await PresentationFile.exportPptx(p)).save(draft);
 const stamp=Date.now();const final=path.join(workspace,'output',d.slug+'-'+stamp+'.pptx');await fs.mkdir(path.dirname(final),{recursive:true});const receipt=path.join(tmp,'validation-'+stamp+'.json');
 const result=await finalizePresentation({workspaceDir:workspace,candidatePath:draft,finalPath:final,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],materializeLiteralChartWorkbooks:true,explicitTotalSlideCount:d.slides.length,fontPolicy:{basis:'design',families:['DejaVu Sans']},verifyArtifactToolImport:true,receiptPath:receipt});
 await fs.copyFile(final,path.join(dir,'downloads',d.slug+'.pptx'));await fs.copyFile(receipt,path.join(tmp,'validation.json'));console.log(d.slug,'PPTX finalizado',result);
 // PDF se exporta desde el PPTX final con LibreOffice (fuentes nativas).
 await fs.writeFile(path.join(tmp,'layout.json'),JSON.stringify(await p.inspect({select:'$.slides[*]',include:['index','elements.text','elements.position']})));
 console.log(d.slug,'PPTX y metadatos listos para exportar');
}
