const pptxgen=require('pptxgenjs');
const fs=require('fs'),path=require('path');
const OUT=path.join(__dirname,'..'),AS=path.join(__dirname,'assets');
const C={bg:'081627',panel:'10233B',panel2:'142C47',panel3:'1A3450',line:'29435A',white:'F2F7FD',body:'C8D9EB',muted:'93ADC5',teal:'48DFC5',blue:'72A7FA',amber:'FFCB70',pink:'F487C8',green:'8CE3A7',dark:'061628'};
const SW=13.333,SH=7.5;
const hex=(k)=>C[k]||k;
const deck=(id,title,accent,coverChart,slides,tagline)=>({id,title,accent,coverChart,slides,tagline});
const s=(title,kicker,bullets,opt={})=>({title,kicker,bullets,...opt});
const section=(title,kicker,sub,chart)=>({kind:'section',title,kicker,sub,chart});
const titles=(a)=>a.map(x=>x.title);
function txt(sl,text,x,y,w,h,opt={}){sl.addText(text,{x,y,w,h,fontFace:'Inter',fontSize:opt.size||16,bold:opt.bold||false,breakLine:false,margin:0,vertAlign:'mid',fit:'shrink',...opt,color:hex(opt.color||'body')})}
function box(sl,x,y,w,h,fill='panel',radius=.16,line=null){sl.addShape('roundRect',{x,y,w,h,rectRadius:radius,radius,fill:{color:hex(fill)},line:{color:hex(line||fill),transparency:line?0:100,width:.9},radius})}
function rule(sl,x,y,w,color='line',width=1){sl.addShape('line',{x,y,w,h:0,line:{color:hex(color),width}})}
function circle(sl,x,y,r,fill){sl.addShape('ellipse',{x,y,w:2*r,h:2*r,fill:{color:hex(fill)},line:{color:hex(fill),transparency:100}})}
function hLine(sl,y,color){sl.addShape('line',{x:.68,y,w:12.0,h:0,line:{color:hex(color),width:.8,transparency:55}})}
function addFoot(sl,idx,total,d){
 hLine(sl,7.145,'line');txt(sl,'CIENCIA DE DATOS · DECISIONES DE NEGOCIO',.72,7.21,5.8,.16,{size:8.0,color:'muted',charSpacing:.8});
 txt(sl,'MÓDULO 10  /  '+d.id.replace(/^\d+_/, '').toUpperCase(),7.5,7.205,3.4,.17,{size:8.0,color:'muted',align:'right'});
 txt(sl,String(idx).padStart(2,'0')+' / '+String(total).padStart(2,'0'),11.55,7.19,1.12,.22,{size:9.2,color:'white',bold:true,align:'right'});
}
function img(sl,name,x,y,w,h){
 let p=path.join(AS,name+'.png');if(!fs.existsSync(p))return;
 sl.addImage({path:p,x,y,w,h,sizingContain:true});
}
function safeNotes(sl,slide,d){
 let notes=[];notes.push('Módulo 10 — '+d.title+'. '+slide.title+'.');
 if(slide.kicker)notes.push(slide.kicker+'.');
 if(slide.bullets)notes.push(slide.bullets.map((b,i)=>'Punto '+(i+1)+': '+b.replace(/[;.]?$/g,'.')).join(' '));
 if(slide.take)notes.push('Idea para enfatizar: '+slide.take+'.');
 if(slide.detail)notes.push('Ampliación docente: '+slide.detail);
 if(slide.sim)notes.push('Articulación con el laboratorio interactivo: '+slide.sim+'.');
 notes.push('Invitar a los estudiantes a justificar el vínculo entre evidencia, supuestos y decisión empresarial. Los gráficos de ejemplo están realizados con datos sintéticos salvo que se indique otra fuente.');
 sl.addNotes(notes.join('\n\n'));
}
function plotVisual(sl,obj,x=6.46,y=1.70,w=6.12,h=4.75){
 box(sl,x,y,w,h,'panel',.17);
 if(obj.chart){img(sl,obj.chart,x+.15,y+.22,w-.3,h-.65);txt(sl,obj.caption||'ESQUEMA / DATOS SINTÉTICOS',x+.25,y+h-.33,w-.5,.18,{size:8.5,color:'muted',charSpacing:.6});return;}
 if(obj.visual?.type==='formula'){
  txt(sl,'MODELO MATEMÁTICO',x+.3,y+.30,w-.6,.3,{size:11.0,color:'teal',bold:true,charSpacing:1.5});
  box(sl,x+.28,y+1.0,w-.56,1.25,'panel2');txt(sl,obj.visual.main||'',x+.5,y+1.12,w-1,1.0,{size:23.5,color:'white',align:'center',bold:true});
  (obj.visual.lines||[]).forEach((p,i)=>{circle(sl,x+.35,y+2.64+i*.57,.065,i%2?'amber':'teal');txt(sl,p,x+.59,y+2.50+i*.57,w-1, .47,{size:12.2,color:'body'});});return;
 }
 if(obj.visual?.type==='compare'){
  let rows=obj.visual.rows||[];
  txt(sl,obj.visual.heading||'COMPARACIÓN',x+.3,y+.3,w-.6,.25,{size:11,color:'teal',bold:true,charSpacing:1.2});
  let top=y+.80; let rh=Math.min(.8,3.7/rows.length);
  rows.forEach((r,i)=>{box(sl,x+.3,top+i*(rh+.10),w-.6,rh,'panel2');txt(sl,r[0],x+.50,top+i*(rh+.1)+.10,1.8,rh-.2,{size:12.4,color:i%2?'amber':'teal',bold:true});txt(sl,r[1],x+2.2,top+i*(rh+.1)+.08,w-2.7,rh-.16,{size:12.2,color:'white'});});return;
 }
 if(obj.visual?.type==='metrics'){
  const values=obj.visual.values||[];txt(sl,obj.visual.heading||'REGLAS DE DECISIÓN',x+.32,y+.33,w-.64,.4,{size:13,color:'teal',bold:true});
  values.forEach((v,i)=>{let cx=x+.35+(i%2)*2.92,cy=y+1+(Math.floor(i/2))*1.66;box(sl,cx,cy,2.75,1.42,'panel2');txt(sl,v[0],cx+.2,cy+.17,2.32,.38,{size:21,color:i%2?'amber':'teal',bold:true});txt(sl,v[1],cx+.2,cy+.63,2.34,.65,{size:12,color:'body'});});return;
 }
 if(obj.visual?.type==='questions'){
  txt(sl,'PREGUNTAS DE DECISIÓN',x+.37,y+.35,w-.74,.30,{size:12.5,color:'teal',bold:true,charSpacing:1.4});
  (obj.visual.items||[]).forEach((z,i)=>{box(sl,x+.32,y+.87+i*.89,w-.64,.71,'panel2');circle(sl,x+.55,y+1.1+i*.89,.13,i%2?'amber':'teal');txt(sl,String(i+1),x+.55,y+1.1+i*.89,.26,.26,{size:10.5,color:'dark',bold:true,align:'center'});txt(sl,z,x+1.0,y+.93+i*.89,w-1.38,.54,{size:13,color:'white'});});return;
 }
 // visual flow default
 const arr=obj.visual?.items||['Datos','Representación','Modelo','Validación','Acción'];
 txt(sl,obj.visual?.heading||'SECUENCIA DE ANÁLISIS',x+.35,y+.30,w-.7,.32,{size:12.1,color:'teal',bold:true,charSpacing:1.0});
 let itemH=Math.min(.62,3.7/arr.length);let gap=.13;let y0=y+.84;
 arr.forEach((v,i)=>{let yy=y0+i*(itemH+gap);box(sl,x+.52,yy,w-1.04,itemH,'panel2');circle(sl,x+.76,yy+.16,.105, i%3===0?'teal':i%3===1?'blue':'amber');txt(sl,v,x+1.22,yy+.08,w-1.77,itemH-.16,{size:14.4,color:'white',bold:i===arr.length-1});if(i<arr.length-1){sl.addShape('line',{x:x+w/2,y:yy+itemH,w:0,h:gap,line:{color:C.muted,width:1.2,beginArrowType:'none',endArrowType:'triangle'}})}});
}
function normal(slide,ppt,idx,total,d){let sl=ppt.addSlide();sl.background={color:C.bg};
 sl.addShape('rect',{x:0,y:0,w:SW,h:.07,fill:{color:hex(d.accent)},line:{transparency:100}});
 txt(sl,'10  /  '+d.id+'     ·     '+(slide.kicker||'FUNDAMENTOS'),.71,.30,11.8,.31,{size:11,color:d.accent,bold:true,charSpacing:1});
 txt(sl,slide.title,.72,.82,12.05,.63,{size:26.4,color:'white',bold:true,fit:'shrink',breakLine:false});
 rule(sl,.72,1.55,11.94,'line',1);
 box(sl,.71,1.70,5.54,4.75,'panel',.15);
 txt(sl,slide.prompt||'IDEAS CLAVE',.99,1.94,4.95,.28,{size:11,color:d.accent,bold:true,charSpacing:1.2});
 const bullets=slide.bullets||[];const sp=bullets.length>=5?.78:bullets.length===4?.94:1.16;
 bullets.forEach((b,i)=>{let y=2.38+i*sp; circle(sl,1.0,y+.11,.065,i===0?d.accent:(i%2?'blue':'amber')); txt(sl,b,1.28,y,4.60,sp-.12,{size:bullets.length>=5?14.0:15.2,color:'body',valign:'mid',fit:'shrink'});});
 plotVisual(sl,slide);
 box(sl,.73,6.59,11.93,.39,'panel2',.1);txt(sl,'IDEA QUE DEBE QUEDAR',.91,6.70,2.1,.15,{size:8.8,color:d.accent,bold:true,charSpacing:.6});txt(sl,slide.take||'Comprender el procedimiento exige evaluar su utilidad y sus límites.',3.04,6.66,9.33,.23,{size:12,color:'white',bold:true,fit:'shrink'});
 addFoot(sl,idx,total,d);safeNotes(sl,slide,d);
}
function sectionSlide(slide,ppt,idx,total,d){let sl=ppt.addSlide();sl.background={color:C.bg};sl.addShape('rect',{x:0,y:0,w:SW,h:.07,fill:{color:hex(d.accent)},line:{transparency:100}});
 txt(sl,'MÓDULO 10  ·  '+d.id+'    /    SECCIÓN',.75,.49,8,.35,{size:12,color:d.accent,bold:true,charSpacing:2});
 txt(sl,slide.title,.76,1.40,7.1,1.7,{size:42,color:'white',bold:true,breakLine:false});
 txt(sl,slide.sub||'',.8,3.57,6.5,1.5,{size:20,color:'body'});
 if(slide.chart){box(sl,7.7,1.27,4.92,4.89,'panel');img(sl,slide.chart,7.85,1.65,4.6,4.06);}else{let x=8.2,y=2.4;for(let i=0;i<7;i++){circle(sl,x+(i%3)*1.25,y+Math.floor(i/3)*1.02,.22,i%3===0?d.accent:i%3===1?'blue':'amber')}}
 addFoot(sl,idx,total,d);safeNotes(sl,slide,d);
}
function cover(ppt,d,total){let sl=ppt.addSlide();sl.background={color:C.bg};sl.addShape('rect',{x:0,y:0,w:SW,h:.11,fill:{color:hex(d.accent)},line:{transparency:100}});
 box(sl,.65,.66,7.35,6.02,'panel');txt(sl,'CIENCIA DE DATOS PARA DECISIONES DE NEGOCIO',1.0,.98,6.5,.35,{size:12.0,color:d.accent,bold:true,charSpacing:1.75});
 txt(sl,'MÓDULO 10',1.02,1.64,5.7,.49,{size:21,color:'muted',bold:true});
 txt(sl,d.title,1.02,2.20,6.60,1.48,{size:38,color:'white',bold:true,breakLine:false});
 sl.addShape('line',{x:1.03,y:4.19,w:2.0,h:0,line:{color:hex(d.accent),width:4}});
 txt(sl,d.tagline,1.04,4.52,6.25,.79,{size:17.5,color:'body'});
 txt(sl,'Clases conceptuales · Matemáticas · Evidencia visual · Decisión de negocio',1.03,5.61,6.38,.55,{size:11.5,color:'muted'});
 box(sl,8.19,.66,4.47,6.02,'panel');img(sl,d.coverChart,8.33,1.45,4.21,3.88);txt(sl,'Sergio Gevatschnaider  ·  Material de cátedra',8.57,5.76,3.85,.54,{size:11.3,color:'body',align:'center'});
 addFoot(sl,1,total,d);safeNotes(sl,{title:'Presentación introductoria',kicker:d.tagline},d)
}
function make(d){const ppt=new pptxgen();ppt.layout='LAYOUT_WIDE';ppt.author='Sergio Gevatschnaider';ppt.subject='Módulo 10 · PCA, K-Means y clustering jerárquico';ppt.title='M10 — '+d.title;ppt.company='Ciencia de Datos para Decisiones de Negocio';ppt.lang='es-AR';ppt.theme={headFontFace:'Inter Display',bodyFontFace:'Inter',lang:'es-AR'};
 const total=d.slides.length+1;cover(ppt,d,total);d.slides.forEach((o,i)=>o.kind==='section'?sectionSlide(o,ppt,i+2,total,d):normal(o,ppt,i+2,total,d));const out=path.join(OUT,'M10_'+d.id+'_Clase_Completa.pptx');return ppt.writeFile({fileName:out}).then(()=>({file:out,slides:total,title:d.title}));}
// ------------------ PCA -------------------------
const PCA=deck('01_PCA','PCA · Análisis de Componentes Principales','teal','pca_geometry',[
 s('Antes de reducir dimensiones: ¿qué queremos preservar?','PROPÓSITO Y CRITERIOS',[
 'Conservar variación útil sin confundir variación con relevancia empresarial.',
 'Sintetizar correlaciones y visualizar datos de muchas variables.',
 'Preparar una representación para explorar o modelar, sin etiquetas.',
 'Evaluar qué información e interpretabilidad se pierden al comprimir.'
 ],{visual:{type:'questions',items:['¿Qué decisión necesita el mapa de datos?','¿Qué variables pueden dominar por su escala?','¿Qué estructura conservaría la proyección?','¿Cómo evaluaríamos pérdida y utilidad?']},take:'PCA maximiza varianza retenida; no maximiza valor de negocio.'}),
 s('Caso conductor: clientes con métricas heterogéneas','APLICACIÓN A NEGOCIOS',[
 'Una fila representa un cliente observado durante 90 días.',
 'Variables: recencia, frecuencia, gasto, margen, uso digital.',
 'Las escalas mezclan días, cantidades y unidades monetarias.',
 'Buscamos estructura para explorar clientes, no crear etiquetas de “buenos” o “malos”.'
 ],{chart:'business_cloud',take:'Primero definir unidad de análisis, ventana temporal y variable de acción.'}),
 section('01 · Intuición geométrica','PCA · GEOMETRÍA','Una rotación de ejes encuentra las direcciones que contienen más variabilidad.','pca_geometry'),
 s('PCA no borra variables: construye nuevos ejes','INTUICIÓN',[
 'PC1 es la dirección que captura la mayor varianza de la nube centrada.',
 'PC2 es ortogonal a PC1 y explica la mayor varianza residual.',
 'Las componentes son combinaciones lineales de las variables.',
 'Con todas las componentes, el cambio de base no pierde información.'
 ],{chart:'pca_geometry',take:'Reducir dimensión significa descartar componentes, no solo rotar ejes.'}),
 s('Centrar los datos: transformar X en X − μ','PREPROCESAMIENTO',[
 'Restar la media de cada variable sitúa el centroide de la muestra en cero.',
 'Las distancias relativas entre observaciones no cambian.',
 'Sin centrado, los ejes pueden reflejar la localización respecto del origen.',
 'Una transformación aprendida en train debe aplicarse igual a test.'
 ],{chart:'pca_center',visual:{type:'formula',main:'Xc = X − 1 μᵀ'},take:'Centrar no equivale a escalar; son decisiones distintas.'}),
 s('Escalar o no escalar: el peso de las unidades','PREPROCESAMIENTO',[
 'PCA sobre covarianzas conserva el peso de la dispersión original.',
 'PCA sobre variables Z equivale a operar sobre correlaciones.',
 'Si las unidades difieren mucho, una variable puede dominar por escala.',
 'La estandarización también puede amplificar variables muy ruidosas.'
 ],{chart:'pca_scale',take:'Elegir la escala a partir del significado de las variables, no por automatismo.'}),
 s('La matriz que describe dispersión y dependencia','COVARIANZA',[
 'La diagonal de Σ contiene las varianzas de cada variable.',
 'Fuera de la diagonal aparecen covarianzas entre pares.',
 'Σ es simétrica y semidefinida positiva.',
 'Una covarianza grande puede reflejar unidades, no necesariamente relación fuerte.'
 ],{chart:'pca_covariance',take:'Σ = XcᵀXc / (n − 1) para la covarianza muestral.'}),
 section('02 · Fundamento matemático','PCA · ÁLGEBRA LINEAL','Autovalores, autovectores y descomposición en valores singulares traducen la geometría a cálculo.','pca_covariance'),
 s('De la covarianza a las componentes principales','AUTOVECTORES',[
 'Cada autovector es una dirección de variación de la muestra.',
 'Cada autovalor mide cuánta varianza existe en esa dirección.',
 'Ordenar autovalores de mayor a menor determina PC1, PC2, etc.',
 'Las direcciones son ortogonales cuando la matriz es simétrica.'
 ],{visual:{type:'formula',main:'Σvⱼ = λⱼvⱼ',lines:['Σ: covarianza de las variables centradas.','vⱼ: eje principal de norma 1.','λⱼ ≥ 0: varianza de la componente j.','λ₁ ≥ λ₂ ≥ … ≥ λₚ.']},take:'Los autovectores dan direcciones; los autovalores dan varianzas.'}),
 s('PCA resuelve un problema de optimización','CRITERIO DE MÁXIMA VARIANZA',[
 'Buscamos una dirección unitaria v para proyectar cada fila de Xc.',
 'La varianza proyectada es vᵀΣv.',
 'La solución de máxima varianza es el autovector principal de Σ.',
 'Para más componentes, imponemos ortogonalidad entre ejes.'
 ],{visual:{type:'formula',main:'maxᵥ  vᵀΣv   sujeto a   vᵀv = 1',lines:['La solución es v₁, autovector de λ₁.','PC1 captura λ₁ de varianza muestral.','PC2 maximiza con v₂ ⟂ v₁.']},take:'Una componente es una dirección óptima según un objetivo muy específico.'}),
 s('SVD: la forma numéricamente robusta de PCA','IMPLEMENTACIÓN',[
 'Descomponemos Xc = U S Vᵀ, sin necesidad de construir Σ explícitamente.',
 'Las filas de Vᵀ aportan direcciones principales.',
 'Los scores aparecen como U S; las varianzas como sⱼ²/(n − 1).',
 'En práctica, librerías usan variantes de SVD por eficiencia y precisión.'
 ],{visual:{type:'formula',main:'Xc = U S Vᵀ',lines:['Scores: T = XcV = U S.','Loadings: columnas de V.','Varianzas: λⱼ = sⱼ² / (n − 1).','Para n ≪ p pueden convenir métodos truncados.']},take:'SVD conecta la explicación geométrica con la implementación reproducible.'}),
 s('Scores y loadings no son lo mismo','INTERPRETACIÓN',[
 'Score: coordenada de cada observación en el nuevo sistema de ejes.',
 'Loading: peso de la variable original en una componente.',
 'Un valor alto en PC1 no implica automáticamente un “buen” cliente.',
 'El signo de toda componente puede invertirse sin cambiar la solución.'
 ],{chart:'pca_biplot',take:'Interpretar cargas requiere contexto, escala y convención de signos.'}),
 s('Ejemplo numérico pequeño para resolver en clase','EJEMPLO PASO A PASO',[
 'Cuatro observaciones: (1,2), (2,3), (3,5), (4,6).',
 'Las medias son x̄ = 2,5 e ȳ = 4; se resta cada media.',
 'La covarianza muestral resulta aproximadamente [[1,67; 2,33],[2,33; 3,33]].',
 'El primer autovalor concentra alrededor de 99,6 % de la variabilidad.'
 ],{visual:{type:'formula',main:'Σ ≈ [1,67  2,33 ; 2,33  3,33]',lines:['Calcular media de cada columna.','Construir Xc y XcᵀXc / 3.','Ordenar autovalores y normalizar vectores.','Proyectar cada observación sobre PC1.']},take:'Un ejemplo mínimo vincula datos, matriz, ejes y proyección.'}),
 section('03 · ¿Cuántas componentes conservar?','PCA · COMPRESIÓN','Cada componente adicional retiene variabilidad, pero también aumenta complejidad y puede reintroducir ruido.','pca_scree'),
 s('Varianza explicada: individual y acumulada','SCORE CARD',[
 'Proporción individual: EVRⱼ = λⱼ / Σ λᵢ.',
 'Varianza acumulada: suma de las proporciones hasta k.',
 'Scree plot identifica cambios de pendiente; no prueba un “K correcto”.',
 'Los umbrales 80 % o 95 % son convenciones, no garantías de utilidad.'
 ],{chart:'pca_scree',take:'Retener varianza no garantiza preservar segmentos, anomalías ni predicción.'}),
 s('Reconstruir los datos: el costo medible de comprimir','ERROR DE RECONSTRUCCIÓN',[
 'Con k componentes, X̂c = TₖVₖᵀ aproxima la matriz centrada.',
 'La diferencia Xc − X̂c cuantifica pérdida de información cuadrática.',
 'PCA de rango k minimiza el error de reconstrucción de Frobenius.',
 'La suma de autovalores omitidos mide la varianza descartada.'
 ],{chart:'pca_reconstruct',take:'Compresión útil = pérdida aceptable para una decisión concreta.'}),
 s('Biplot: observaciones y relaciones entre variables','VISUALIZACIÓN',[
 'Puntos cercanos en PC1–PC2 tienen scores similares, no necesariamente distancia original idéntica.',
 'Las flechas muestran la relación de cada variable con el plano proyectado.',
 'El ángulo entre vectores sugiere asociaciones si la representación es adecuada.',
 'Las longitudes deben leerse según la escala elegida para el biplot.'
 ],{chart:'pca_biplot',take:'El biplot es una aproximación de dos dimensiones, no un mapa exhaustivo.'}),
 s('PCA frente a seleccionar variables','ALTERNATIVAS',[
 'Selección: conservar variables originales; maximiza interpretabilidad.',
 'PCA: generar factores lineales; reduce redundancia entre medidas.',
 'Variables con baja varianza pueden ser útiles si predicen un evento raro.',
 'PCA no selecciona atributos por relevancia para una etiqueta futura.'
 ],{visual:{type:'compare',rows:[['SELECCIÓN','Retiene columnas originales.'],['PCA','Combina columnas en ejes nuevos.'],['PREDICCIÓN','Validar ambos caminos con métricas externas.'],['RIESGO','Confundir varianza con información útil.']]},take:'Conservar interpretabilidad puede ser más valioso que una compresión extrema.'}),
 section('04 · Riesgos y decisiones','PCA · USO RESPONSABLE','El procedimiento puede ser matemáticamente correcto y analíticamente poco útil si se ignora el contexto.','pca_outlier'),
 s('Sensibilidad a extremos, ruido y escalas','ROBUSTEZ',[
 'Una sola observación muy extrema puede rotar PC1 al cambiar Σ.',
 'Centrado y escalado clásicos también reaccionan a outliers.',
 'Comparar con y sin extremos; evaluar alternativas robustas.',
 'No excluir clientes excepcionales sin una justificación de negocio.'
 ],{chart:'pca_outlier',take:'El análisis de sensibilidad es obligatorio cuando la estructura depende de pocos casos.'}),
 s('PCA es lineal; algunas formas no caben en un plano lineal','LIMITACIONES',[
 'PCA busca ejes rectos y ortogonales, no variedades curvas.',
 'Los métodos no lineales pueden representar estructuras curvas.',
 't-SNE y UMAP son útiles para exploración, pero las distancias pueden distorsionarse.',
 'Nunca inferir clusters fiables solo por manchas en una visualización.'
 ],{chart:'k_moons',take:'Un gráfico atractivo en 2D no demuestra que existan segmentos reales.'}),
 s('PCA dentro del pipeline: evitar fuga de información','VALIDACIÓN',[
 'Separar train y test antes de ajustar imputación, escalado y PCA.',
 'Ajustar medias, desvíos y componentes únicamente en train.',
 'Aplicar transformaciones aprendidas sobre validación y test.',
 'Si se evalúan clusters, medir estabilidad sin usar datos futuros.'
 ],{visual:{type:'flow',heading:'PIPELINE CORRECTO',items:['Dividir por cliente o período','Imputar / escalar con entrenamiento','Ajustar PCA solamente en train','Proyectar train y test','Validar estabilidad y efecto en decisión']},take:'Todo preprocesamiento aprendido del dataset pertenece dentro del pipeline.'}),
 s('¿PCA antes de K-Means? Beneficios y costos','CONEXIÓN CON LA SIGUIENTE CLASE',[
 'Puede atenuar ruido y reducir el costo del cálculo de distancias.',
 'Puede eliminar direcciones de baja varianza que sí separan grupos.',
 'Se compara clustering en variables originales escaladas versus PCA(k).',
 'La comparación requiere criterios de estabilidad e interpretación externa.'
 ],{visual:{type:'compare',rows:[['ORIGINAL','Métricas transparentes y accionables.'],['PCA(k)','Compresión, posible reducción de ruido.'],['VALIDAR','Silhouette, estabilidad, perfiles, utilidad.'],['DECIDIR','Preferir solución reproducible e interpretable.']]},take:'PCA y clustering son etapas diferentes; no siempre conviene combinarlas.'}),
 s('De la gráfica a una decisión concreta','CASO EMPRESARIAL',[
 'PC1 puede capturar intensidad de relación comercial; PC2, sensibilidad promocional.',
 'Esas etiquetas solo valen si los loadings respaldan la interpretación.',
 'Construir perfiles con métricas originales, no únicamente con componentes.',
 'Proponer una acción medible: retención, activación o costo de contacto.'
 ],{chart:'business_profiles',take:'Toda recomendación debe recuperar las variables originales y su impacto esperado.'}),
 s('Laboratorios vinculados a cada idea','DISEÑO DE SIMULACIONES M10',[
 'S01: rotación de PC1–PC2 y nube con correlación ajustable.',
 'S02: centrar, estandarizar y modificar pesos de variables.',
 'S03: scree plot, varianza acumulada y error de reconstrucción.',
 'S04: outliers, biplot y comparación PCA → K-Means.'
 ],{visual:{type:'flow',items:['S01 · Geometría en tiempo real','S02 · Escala / covarianza / correlación','S03 · Compresión / pérdida','S04 · Sensibilidad / segmentación']},sim:'Los simuladores S01–S04 replicarán las figuras y controles de las diapositivas.',take:'Cada laboratorio cambiará una hipótesis y mostrará evidencia observable.'}),
 s('Ejercicio de transferencia y evaluación','DESAFÍO DE CLASE',[
 'Dos variables están muy correlacionadas, pero una mide montos 1.000 veces mayores.',
 'Se obtiene 92 % de varianza con dos componentes de cinco.',
 'Un outlier cambia PC1 y la silhouette mejora después de comprimir.',
 'Explicar qué decisiones sí se pueden justificar y qué evidencia falta.'
 ],{visual:{type:'questions',items:['¿Qué escalado usarías y por qué?','¿Retendrías dos componentes?','¿Qué experimento mide sensibilidad?','¿Qué indicador externo probaría utilidad?']},take:'La evidencia de varianza es necesaria, pero no suficiente.'}),
 s('Mapa de errores frecuentes','AUTOCONTROL',[
 '“PC1 es la variable más importante” → es una combinación, no una columna.',
 '“95 % de varianza = 95 % de precisión” → son magnitudes diferentes.',
 '“PCA identifica clusters” → PCA proyecta; no asigna grupos.',
 '“La misma proyección sirve para siempre” → debe vigilarse el drift.'
 ],{visual:{type:'compare',rows:[['NO','Varianza = capacidad predictiva.'],['NO','Componente = variable original.'],['NO','Biplot = distancias fieles para todo.'],['SÍ','Validación, sensibilidad y contexto.']]},take:'Las interpretaciones fuertes necesitan pruebas externas.'}),
 s('Bibliografía esencial y cierre de PCA','REFERENCIAS',[
 'Jolliffe, I. T. & Cadima, J. (2016). Principal component analysis: a review.',
 'Hastie, Tibshirani & Friedman (2009). The Elements of Statistical Learning, cap. 14.',
 'James et al. (2023). An Introduction to Statistical Learning with Applications in Python.',
 'scikit-learn: User Guide → Decomposition / PCA; documentación de Pipeline.'
 ],{visual:{type:'flow',items:['Comprender → proyectar','Cuantificar → reconstruir','Validar → interpretar','Decidir → monitorear']},take:'En la próxima presentación convertimos la geometría en una asignación de grupos.'})
],'Desde la geometría de la varianza hasta una representación defendible para el negocio.');
// ------------------ K-MEANS -------------------
const KMEANS=deck('02_KMeans','K-Means · Segmentación por centroides','blue','k_final',[
 s('La pregunta correcta antes de elegir K','OBJETIVOS Y DECISIÓN',[
 'Segmentar para definir acciones diferenciadas, no para decorar un dashboard.',
 'Precisar a quién se segmenta: clientes, sucursales, productos o eventos.',
 'Seleccionar variables, distancias, escala y número de segmentos.',
 'Medir estabilidad, capacidad descriptiva y costos de implementación.'
 ],{visual:{type:'questions',items:['¿Qué decisión cambia entre segmentos?','¿Es comparable cada variable?','¿Se pueden ejecutar acciones diferentes?','¿Los segmentos resisten una nueva muestra?']},take:'Un cluster no tiene valor comercial hasta que cambia una decisión.'}),
 s('Un mismo dataset sin etiquetas de segmento','CASO CONDUCTOR',[
 '210 clientes sintéticos expresados en frecuencia y margen estandarizados.',
 'La nube parece exhibir tres concentraciones principales.',
 'El algoritmo no conoce los grupos originales que generaron los datos.',
 'El reto es detectar y describir una estructura sin sobreinterpretarla.'
 ],{chart:'business_cloud',take:'Los grupos descubiertos dependen de distancia, escala y supuestos.'}),
 section('01 · Qué optimiza K-Means','K-MEANS · MODELO','Una partición “buena” minimiza las distancias cuadráticas de los puntos a sus centroides.','k_regions'),
 s('La función objetivo es la inercia (WCSS)','FORMALIZACIÓN',[
 'Para cada cliente i se asigna una etiqueta zᵢ entre 1 y K.',
 'Cada cluster j tiene un centroide μⱼ, media de sus observaciones.',
 'Se minimiza la suma de distancias euclídeas al cuadrado.',
 'La solución es local y depende de la inicialización.'
 ],{visual:{type:'formula',main:'J = ∑ᵢ ‖xᵢ − μzᵢ‖²',lines:['xᵢ: vector de características del cliente.','zᵢ: etiqueta asignada de 1 a K.','μⱼ: promedio del cluster j.','K-Means favorece grupos compactos.']},take:'La inercia es interna; no mide directamente la utilidad de un segmento.'}),
 s('Asignación: cada punto elige su centroide más cercano','ALGORITMO · PASO A',[
 'Fijados los centros, calcular la distancia euclídea de cada xᵢ.',
 'La etiqueta se actualiza según el centro de distancia mínima.',
 'El plano queda separado en regiones de Voronoi.',
 'Un cambio en los centros altera qué cliente cae en cada zona.'
 ],{chart:'k_regions',take:'En cada iteración se reasignan clientes por proximidad.'}),
 s('Actualización: la media minimiza la SSE intracluster','ALGORITMO · PASO B',[
 'Para cada grupo se calcula la media de los puntos asignados.',
 'La media es el minimizador de la suma de distancias al cuadrado.',
 'Repetimos asignación y actualización hasta converger.',
 'Un cluster vacío requiere una estrategia explícita de reinicio.'
 ],{visual:{type:'formula',main:'μⱼ ← (1 / nⱼ) ∑ᵢ:zᵢ=j xᵢ',lines:['Asignar puntos al centro más cercano.','Calcular la media de cada nuevo grupo.','Repetir y detener ante estabilidad / tolerancia.','Controlar iteraciones, vacíos y semilla.']},take:'El algoritmo de Lloyd alterna dos optimizaciones condicionadas.'}),
 s('Demostración manual con seis puntos','EJEMPLO NUMÉRICO',[
 'A=(1,1), B=(2,1), C=(2,2); D=(7,7), E=(8,7), F=(8,8).',
 'Con K=2 y una asignación natural: ABC frente a DEF.',
 'Centroides: μ₁=(1,67;1,33), μ₂=(7,67;7,33).',
 'Cada punto debe quedar asignado al centroide más próximo.'
 ],{visual:{type:'formula',main:'μ₁ = (5/3, 4/3)   ·   μ₂ = (23/3, 22/3)',lines:['Pedir a la clase justificar la primera asignación.','Calcular ambas medias coordenada a coordenada.','Verificar distancias y si cambiaron etiquetas.','Comparar con K=1 y K=3.']},take:'La media es vectorial: cada coordenada se promedia dentro de su grupo.'}),
 section('02 · La dinámica visible','K-MEANS · ITERACIONES','Acompañar cada desplazamiento del centroide explica mucho más que mostrar el cluster final.','k_init'),
 s('Inicialización: una elección con consecuencias','ITERACIÓN 0',[
 'Elegimos K=3 y tres centroides iniciales, potencialmente alejados.',
 'Se colorean los clientes según el centro más cercano.',
 'Una elección desfavorable puede inducir un mínimo local de peor calidad.',
 'El objetivo todavía puede disminuir de forma importante.'
 ],{chart:'k_init',take:'S05 del futuro simulador permitirá mover centroides a mano.'}),
 s('Primer ciclo: nuevas medias, nuevas asignaciones','ITERACIÓN 1',[
 'Con las etiquetas actuales, recalculamos tres promedios.',
 'Los centroides migran hacia las regiones con más puntos asignados.',
 'Luego cambia la frontera de decisión.',
 'La inercia no aumenta cuando se ejecutan correctamente ambos pasos.'
 ],{chart:'k_iter1',take:'Cada iteración reduce o mantiene el objetivo; no garantiza óptimo global.'}),
 s('Convergencia: se estabilizan los grupos','RESULTADO',[
 'El algoritmo termina cuando no hay mejora significativa o se alcanza un límite.',
 'Los tres segmentos sintéticos pasan a ser territorialmente compactos.',
 'La posición final de cada centro resume promedios, no clientes reales.',
 'El orden numérico de las etiquetas 0, 1, 2 es arbitrario.'
 ],{chart:'k_final',take:'La convergencia técnica no certifica que el modelo sea estable o útil.'}),
 s('Por qué conviene K-Means++ y varios reinicios','INICIALIZACIÓN',[
 'K-Means++ tiende a separar centroides iniciales mediante distancias.',
 'Disminuye el riesgo de soluciones iniciales claramente pobres.',
 'Usar varios reinicios y escoger la menor inercia obtenida.',
 'Guardar random_state, n_init, tolerancia y versión de librería.'
 ],{visual:{type:'flow',heading:'DISEÑO REPRODUCIBLE',items:['Elegir K y variables','Sembrar centros con K-Means++','Ejecutar varios reinicios','Comparar inercia y estabilidad','Guardar parámetros / perfil resultante']},take:'Más reinicios reducen dependencia del azar; no eliminan los supuestos del método.'}),
 section('03 · Elegir K sin autoengaño','K-MEANS · EVALUACIÓN','Una curva bonita no sustituye un criterio de decisión ni la validación de estabilidad.','k_metrics'),
 s('Elbow: buscar rendimientos marginales decrecientes','MÉTODO DEL CODO',[
 'El mínimo teórico de inercia no crece con K; un ajuste local puede diferir.',
 'Se observa si la mejora comienza a ser marginal al añadir clusters.',
 'Algunas muestras no muestran un codo claro.',
 'Nunca maximizar K exclusivamente para minimizar la inercia.'
 ],{chart:'k_metrics',take:'El “codo” es una heurística visual, no una prueba estadística universal.'}),
 s('Silhouette: equilibrio de cohesión y separación','VALIDACIÓN INTERNA',[
 'a(i): distancia media del punto a su propio cluster (excluyéndose a sí mismo).',
 'b(i): menor distancia media a otro cluster.',
 's(i) = [b(i) − a(i)] / max{a(i), b(i)}.',
 'Cercano a 1 indica mayor separación; negativo sugiere asignación discutible.'
 ],{chart:'k_silhouette',take:'Usar tanto la media como el perfil por cluster; requiere grupos de tamaño adecuado.'}),
 s('Triangular K con evidencias diferentes','VALIDACIÓN EXTERNA E INTERNA',[
 'Calcular inertia, silhouette, tamaño de grupos y estabilidad entre muestras.',
 'Revisar si los perfiles originales son distintos e interpretables.',
 'Medir utilidad: retención, conversión, uplift o ahorro operativo.',
 'Preferir K interpretable cuando diferencias de métricas son marginales.'
 ],{visual:{type:'metrics',values:[['K','No siempre hay óptimo único'],['SSE','Compacidad interna'],['S(i)','Cohesión / separación'],['€','Acción / valor esperado']]},take:'La selección de K es multicriterio y debe declararse antes de actuar.'}),
 section('04 · Límites estructurales','K-MEANS · ADVERTENCIAS','La forma de los datos, los outliers y las decisiones de escala determinan qué segmentos son posibles.','k_moons'),
 s('La escala cambia la noción de parecido','MÉTRICAS Y DISTANCIAS',[
 'Euclidean² suma diferencias al cuadrado por variable.',
 'Si una característica tiene varianza enorme puede dirigir la partición.',
 'StandardScaler, transformaciones log y ponderaciones cambian los grupos.',
 'Evaluar cambios de perfiles y estabilidad frente a transformaciones.'
 ],{chart:'pca_scale',take:'Una distancia solo tiene sentido luego de justificar la escala y las variables.'}),
 s('K-Means no es “clustering con cualquier distancia”','SUPUESTOS MATEMÁTICOS',[
 'La actualización con medias deriva de distancias euclídeas al cuadrado.',
 'Con distancias arbitrarias el centroide puede dejar de ser el minimizador.',
 'K-Medoids usa observaciones representativas, útil con métricas más generales.',
 'Para datos mixtos o categóricos convienen modelos de agrupamiento adecuados.'
 ],{visual:{type:'compare',rows:[['K-MEANS','Centroide medio / Euclidean².'],['K-MEDOIDS','Medoide real / distancias elegidas.'],['K-MODES','Moda para variables categóricas.'],['GOWER','Una posible distancia para datos mixtos.']]},take:'No cambiar la función de distancia sin reconsiderar el algoritmo completo.'}),
 s('Outliers: un punto puede arrastrar centroides','ROBUSTEZ',[
 'La pérdida cuadrática penaliza fuertemente las desviaciones extremas.',
 'Un punto aislado puede desplazar uno o más centroides.',
 'Comparar ajustes con y sin casos extremos documentados.',
 'K-Medoids, clustering robusto o reglas específicas pueden ser alternativas.'
 ],{chart:'k_outlier',take:'No decidir automáticamente que los clientes excepcionales son “errores”.'}),
 s('Clases no convexas: K-Means puede cortar la estructura','GEOMETRÍA DE LAS FORMAS',[
 'Con medias lunas, el agrupamiento real sigue una trayectoria curva.',
 'K-Means crea celdas convexas y no sigue automáticamente la curva.',
 'El criterio de inercia puede verse razonable pese a una partición equivocada.',
 'Examinar alternativas como métodos de densidad o espectrales.'
 ],{chart:'k_moons',take:'Una silhouette elevada no corrige supuestos geométricos inadecuados.'}),
 s('Clusters alargados, tamaños distintos y densidades desiguales','ESTRUCTURA DE GRUPOS',[
 'Los centros esféricos sufren cuando las covarianzas son anisotrópicas.',
 'Clusters grandes pueden absorber pequeños pero importantes.',
 'La diferencia de densidad deteriora la frontera por cercanía.',
 'Gaussian Mixture o modelos de densidad pueden resultar más adecuados.'
 ],{chart:'k_anisotropy',take:'El negocio puede preferir un segmento pequeño que K-Means diluye.'}),
 s('Estabilidad frente a semillas y remuestreo','REPRODUCIBILIDAD',[
 'Correr diferentes semillas y revisar inercia, silhouette y tamaños.',
 'Repetir el análisis sobre bootstrap o cortes temporales comparables.',
 'Evaluar acuerdo entre particiones mediante ARI u otras métricas.',
 'No comparar etiquetas numéricas sin alinear las particiones.'
 ],{chart:'k_stability',take:'Un segmento que desaparece con cambios menores necesita cautela antes de activarlo.'}),
 section('05 · De grupos a acciones','K-MEANS · NEGOCIO','La segmentación se vuelve valiosa cuando cada perfil permite diseñar y evaluar una intervención.','business_profiles'),
 s('Perfilado: volver de los números Z al cliente real','INTERPRETACIÓN',[
 'Calcular distribución de frecuencia, margen, recencia y canal por segmento.',
 'Comparar tamaño, ingreso, dispersión y riesgo de cada grupo.',
 'Traducir patrones a hipótesis, evitando estereotipos como “fiel” sin evidencia.',
 'Asignar nombres operativos solo después de validar el perfil.'
 ],{chart:'business_profiles',take:'El perfil debe explicarse con unidades originales y dispersión interna.'}),
 s('Diseñar acciones y testearlas','GOBIERNO DE SEGMENTOS',[
 'Ejemplo S1: reconexión con clientes de recencia alta y margen bajo.',
 'Ejemplo S2: fidelización y beneficios para frecuencia/margen altos.',
 'Ejemplo S3: activación digital sin otorgar descuentos indiscriminados.',
 'Probar campañas con grupos de control; segmentar no implica causalidad.'
 ],{visual:{type:'compare',rows:[['S1 · PROTEGER','Recuperación controlada / costo por contacto.'],['S2 · FIDELIZAR','Beneficios basados en margen incremental.'],['S3 · ACTIVAR','Onboarding digital y adopción de canal.'],['MEDIR','Lift incremental y ROI neto por segmento.']]},take:'Una campaña segmentada debe demostrar valor incremental contra una alternativa.'}),
 s('Asignación de nuevos clientes y monitoreo','PRODUCCIÓN',[
 'Guardar escalador, variables, centros, semillas y fecha de entrenamiento.',
 'Calcular distancias a centros sin recalcular todo el modelo en cada predicción.',
 'Vigilar drift de variables, tamaño y distribución de grupos.',
 'Definir una política de refresco y de intervención ante anomalías.'
 ],{visual:{type:'flow',items:['Datos nuevos con contrato de calidad','Transformación fija / mismo orden','Asignación al centro más cercano','Regla de acción elegible','Experimento / monitoreo / reentrenamiento']},take:'El cluster se mantiene como instrumento operativo, no como etiqueta permanente.'}),
 s('Simulaciones K-Means y pruebas de hipótesis','LABORATORIOS CORRESPONDIENTES',[
 'S05: arrastrar centros y observar la asignación en vivo.',
 'S06: ejecutar Lloyd paso a paso y ver curva de inercia.',
 'S07: comparar k-means++, reinicios y semillas.',
 'S08: comparar K mediante codo, silhouette y estabilidad.',
 'S09: editar escala, forma, outliers y ver fallas geométricas.'
 ],{visual:{type:'flow',items:['S05 · Asignar / actualizar','S06 · Iteración / convergencia','S07 · Inicio / mínimos locales','S08 · K / calidad / estabilidad','S09 · Fallas / perturbaciones']},take:'En cada simulación el alumno debe describir qué cambió y por qué.'}),
 s('Prueba de transferencia: segmentar y defender','ACTIVIDAD DE EVALUACIÓN',[
 'El codo sugiere K=4, pero silhouette prefiere K=3.',
 'Un segmento estratégico con 2 % de clientes aparece solo con K=5.',
 'Al cambiar una semilla, 25 % de clientes cambia de grupo.',
 'Argumentar un plan de selección y validación antes de activar campañas.'
 ],{visual:{type:'questions',items:['¿Qué métricas compararías para K?','¿Cómo proteger el segmento minoritario?','¿Qué harías con la inestabilidad?','¿Qué experimento prueba valor económico?']},take:'El mejor K equilibra estructura, estabilidad, interpretación y decisión.'}),
 s('Errores frecuentes y bibliografía','SÍNTESIS / REFERENCIAS',[
 'Confundir K-NN (supervisado) con K-Means (no supervisado).',
 'Leer etiquetas de cluster como ranking o como diagnóstico causal.',
 'MacQueen (1967); Arthur & Vassilvitskii (2007), k-means++.',
 'Hastie, Tibshirani & Friedman (2009); scikit-learn User Guide: Clustering.'
 ],{visual:{type:'compare',rows:[['SUPUESTO','La distancia euclídea al cuadrado importa.'],['CONTROL','Semilla / escala / forma / outliers.'],['EVIDENCIA','SSE + silhouette + estabilidad.'],['NEGOCIO','Grupos con intervención evaluable.']]},take:'La segmentación no es una explicación causal del comportamiento del cliente.'})
],'Cómo se mueven los centroides, cómo elegir K y cuándo desconfiar de los grupos.');
// ------------------ HIERARCHY -------------------
const HIER=deck('03_Jerarquico','Clustering jerárquico · Dendrogramas y linkages','amber','h_ward',[
 s('Por qué construir jerarquías, no solo grupos','PROPÓSITO',[
 'Investigar estructura anidada sin fijar K desde el inicio.',
 'Observar el orden y la distancia a los que se fusionan grupos.',
 'Seleccionar resoluciones apropiadas para distintas decisiones.',
 'Distinguir jerarquía matemática de una jerarquía causal o empresarial.'
 ],{visual:{type:'questions',items:['¿Cuántos niveles de segmentación interesan?','¿Qué observaciones se parecen primero?','¿Qué significa fusionar grupos?','¿Qué punto de corte es útil?']},take:'Un dendrograma muestra una historia de fusiones, no “categorías naturales” definitivas.'}),
 s('El mismo caso de 12 clientes facilita seguir fusiones','CASO CONDUCTOR',[
 'Cada observación tiene frecuencia y margen estandarizados.',
 'Primero se calcula una matriz de distancias entre pares.',
 'Al principio cada cliente forma su propio grupo.',
 'La estrategia de linkage decide qué grupos se fusionan.'
 ],{chart:'h_points',take:'Con pocos puntos podemos verificar a mano cada paso del algoritmo.'}),
 section('01 · Cómo nace la jerarquía','AGLOMERATIVO','Se comienza con n grupos unitarios y se repite la fusión más cercana hasta obtener uno.','h_points'),
 s('Una matriz de distancias es el verdadero punto de partida','MÉTRICA',[
 'Distancia euclídea d(i,j) = √Σₘ(xᵢₘ − xⱼₘ)².',
 'La diagonal de la matriz vale cero y la matriz es simétrica.',
 'La escala define cuánto pesa cada variable en la proximidad.',
 'La tabla de distancias por sí sola no decide cómo combinar clusters.'
 ],{chart:'h_matrix',take:'Métrica y linkage son elecciones distintas, que deben explicitarse.'}),
 s('Fusión paso a paso: 12 → 11 → … → 1','ALGORITMO AGLOMERATIVO',[
 'Buscar el par de clusters con mínima disimilitud según el linkage.',
 'Unir ese par y registrar altura de fusión.',
 'Actualizar distancias entre nuevo cluster y restantes.',
 'Repetir hasta que todos los puntos pertenezcan a un único árbol.'
 ],{visual:{type:'flow',items:['12 clusters individuales','Mínimo par de distancias','Fusionar y registrar altura','Recalcular disimilitudes','Hasta una jerarquía completa']},take:'Una vez fusionados dos grupos, la versión aglomerativa no los separa.'}),
 s('Ejemplo manual con cuatro observaciones','ARITMÉTICA SENCILLA',[
 'A=(0,0), B=(0,1), C=(4,0), D=(4,1).',
 'Distancias AB=CD=1; AC=BD=4; AD=BC=√17.',
 'Se fusionan AB y CD (hay empate; el orden puede variar).',
 'Single linkage entre AB y CD usa la menor distancia entre pares: 4.'
 ],{visual:{type:'formula',main:'d_single(AB, CD) = min{4, √17, √17, 4} = 4',lines:['Altura 1: dos pares A–B y C–D.','Altura 4: fusionar ambos clusters.','Con complete: altura √17 ≈ 4,12.','La elección de linkage cambia el árbol.']},take:'Un dendrograma no es único si hay empates o cambia el criterio de fusión.'}),
 section('02 · Aprender a leer dendrogramas','JERÁRQUICO · VISUALIZACIÓN','La información crucial está en la altura de fusión y en la estructura, no en el espacio horizontal.','h_ward'),
 s('Qué representa cada parte del dendrograma','LECTURA',[
 'Las hojas corresponden a observaciones originales.',
 'Las ramas indican combinaciones sucesivas de grupos.',
 'La altura codifica el valor del criterio de disimilitud al fusionar.',
 'Reordenar hojas puede cambiar el aspecto sin cambiar la jerarquía.'
 ],{chart:'h_ward',take:'La posición horizontal no representa automáticamente una distancia medible.'}),
 s('Cortar un árbol: del continuo jerárquico al K elegido','CORTE HORIZONTAL',[
 'Un umbral h divide el árbol en componentes desconectadas.',
 'Alternativamente, solicitar directamente un número de clusters.',
 'Comparar niveles según estabilidad, tamaños y acción operativa.',
 'El mismo árbol admite segmentaciones gruesas y finas.'
 ],{chart:'h_cut',take:'El corte es una decisión analítica separada de la construcción del árbol.'}),
 section('03 · Cuatro criterios de linkage','JERÁRQUICO · MODELOS','Single, complete, average y Ward producen estructuras diferentes aun con los mismos puntos.','h_compare'),
 s('Single linkage: distancia mínima entre clusters','DISTANCIA ENTRE CONJUNTOS',[
 'D(A,B) = min d(a,b) para a∈A y b∈B.',
 'Puede capturar formas alargadas y conectividad local.',
 'Sufre el efecto chaining: un puente de puntos conecta grupos.',
 'Es sensible a contactos accidentales entre regiones.'
 ],{chart:'h_single',take:'Single prioriza conectividad; no necesariamente compacidad.'}),
 s('Complete linkage: la distancia máxima','DISTANCIA ENTRE CONJUNTOS',[
 'D(A,B) = max d(a,b) para a∈A y b∈B.',
 'Favorece grupos de diámetro contenido y relativamente compactos.',
 'Puede dividir estructuras largas que single sí conectaría.',
 'La elección depende de la topología esperada y el uso.'
 ],{chart:'h_complete',take:'Complete minimiza la peor separación entre puntos de grupos unidos.'}),
 s('Average linkage: promedio de distancias por pares','DISTANCIA ENTRE CONJUNTOS',[
 'D(A,B) = promedio de d(a,b) sobre a∈A, b∈B.',
 'Se ubica entre el énfasis conectivo de single y el compacto de complete.',
 'No equivale a distancia entre centroides en general.',
 'Es sensible a la métrica y al peso de grupos grandes.'
 ],{chart:'h_average',take:'Average balancea múltiples relaciones en vez de mirar solo extremos.'}),
 s('Ward: fusionar donde menos aumenta la inercia','CRITERIO DE VARIANZA',[
 'Selecciona la fusión que menos eleva la SSE total dentro de clusters.',
 'Para grupos A y B: ΔSSE = (nA nB)/(nA+nB) ‖μA−μB‖².',
 'Tiende a generar conjuntos compactos y de tamaño relativamente equilibrado.',
 'Requiere trabajar coherentemente con distancia euclídea en su formulación.'
 ],{chart:'h_ward',take:'La altura graficada por software Ward depende de su convención; no siempre es ΔSSE literal.'}),
 s('Comparar los cuatro árboles sobre la misma evidencia','COMPARACIÓN CONTROLADA',[
 'Mantener puntos y escala exactamente iguales.',
 'Cambiar exclusivamente el criterio de enlace.',
 'Observar altas fusiones, grupos aislados y puentes.',
 'Evaluar más de una partición: la comparación visual no basta.'
 ],{chart:'h_compare',take:'El cambio de árbol no surge de nuevos datos sino de la definición de proximidad.'}),
 s('Chaining: cuando un puente “pega” estructuras diferentes','CASO PATOLÓGICO',[
 'Single fusiona observaciones a través de vecinos cercanos sucesivos.',
 'Una cadena de puntos puede conectar extremos muy separados.',
 'Complete penaliza el diámetro y ofrece un comportamiento diferente.',
 'La “mejor” solución depende de la noción de grupo que se quiera detectar.'
 ],{chart:'h_chaining',take:'El chaining no es un bug: es una consecuencia de la definición de single.'}),
 section('04 · Validez y límites','JERÁRQUICO · INFERENCIA','Los algoritmos construyen árboles completos aun cuando los datos no contienen agrupaciones significativas.','h_scatter_ward'),
 s('Las variables y la escala siguen gobernando el resultado','PREPROCESAMIENTO',[
 'Estandarizar si las unidades y dispersiones no son comparables.',
 'Las transformaciones pueden alterar distancias y orden de fusión.',
 'En Ward, la geometría euclídea es parte del criterio cuadrático.',
 'Justificar la inclusión de variables relevantes para la acción.'
 ],{chart:'pca_scale',take:'La jerarquía no corrige datos mal definidos o mal escalados.'}),
 s('Distancia y linkage: combinaciones compatibles','DISEÑO METODOLÓGICO',[
 'Single/complete/average pueden usar diferentes métricas de distancia.',
 'Ward está atado a un objetivo de suma de cuadrados euclídeos.',
 'La distancia de Manhattan puede ser útil, pero cambia interpretación.',
 'Nunca reportar “Ward + cualquier métrica” sin verificar implementación.'
 ],{visual:{type:'compare',rows:[['SINGLE','Mínimo par / diversas métricas.'],['COMPLETE','Máximo par / diversas métricas.'],['AVERAGE','Promedio / diversas métricas.'],['WARD','Incremento SSE / marco euclídeo.']]},take:'La consistencia matemática entre métrica y criterio es una exigencia, no un detalle.'}),
 s('Coeficiente cofenético: cómo deforma las distancias','DIAGNÓSTICO DE AJUSTE',[
 'La distancia cofenética de dos puntos es la altura a la que se unen.',
 'Se correlacionan distancias originales con cofenéticas.',
 'Correlación alta significa fidelidad global del árbol a esas distancias.',
 'No garantiza separación real ni utilidad de clusters para decisiones.'
 ],{visual:{type:'formula',main:'r_coph = corr(dᵢⱼ, cᵢⱼ)',lines:['dᵢⱼ: distancia original entre i y j.','cᵢⱼ: altura de fusión en el árbol.','Comparar linkages manteniendo misma matriz.','No confundir fidelidad geométrica con utilidad.']},take:'Es una medida de representación de distancias, no un “certificado de clusters”.'}),
 s('Costo computacional: por qué no escalar ciegamente','COMPLEJIDAD',[
 'La matriz de distancias completa contiene n(n−1)/2 pares.',
 'Requiere O(n²) memoria para distancias densas.',
 'El tiempo depende de algoritmo, linkage e implementación.',
 'Para cientos de miles de clientes conviene submuestrear o usar alternativas.'
 ],{visual:{type:'metrics',values:[['n²','Número de distancias crece cuadráticamente'],['10k','Casi 50 M de pares'],['RAM','Puede ser el cuello de botella'],['MUESTRA','Evaluar escalabilidad antes de desplegar']]},take:'Un dendrograma completo no siempre es la herramienta operacional escalable.'}),
 s('Ruido, outliers y estabilidad del árbol','ROBUSTEZ',[
 'Una observación atípica puede unirse al final y alterar alturas.',
 'Pequeñas perturbaciones de datos pueden modificar ramas cercanas.',
 'Comparar cortes en bootstrap, ventanas temporales o submuestras.',
 'Medir concordancia de particiones sin comparar IDs arbitrarios.'
 ],{chart:'h_points',take:'Priorizar las divisiones reproducibles por sobre historias atractivas del árbol.'}),
 s('¿PCA antes del clustering jerárquico?','INTEGRACIÓN',[
 'PCA puede atenuar redundancia y facilitar visualización de clusters.',
 'Descartar componentes cambia distancias y, por lo tanto, fusiones.',
 'Si se usan todas las componentes de PCA centrado, las distancias euclídeas se preservan.',
 'Si se estandarizan scores o se truncan, se modifica la geometría.'
 ],{chart:'pca_geometry',take:'La rotación ortogonal completa preserva distancias; la reducción no.'}),
 section('05 · Interpretación y aplicación','JERÁRQUICO · NEGOCIO','Los niveles del árbol pueden corresponder a decisiones de distinta granularidad si se validan.','h_profiles'),
 s('Heatmap de perfiles: ver si los segmentos son accionables','ANÁLISIS DE SEGMENTOS',[
 'Después del corte, calcular medias o medianas en variables originales.',
 'En el ejemplo sintético, los grupos difieren en recencia, margen y canal.',
 'Contrastar cada perfil con dispersión, tamaño y estabilidad.',
 'No tratar la visualización del mapa de calor como evidencia causal.'
 ],{chart:'h_profiles',take:'El mapa de calor transforma una partición en hipótesis comerciales contrastables.'}),
 s('Jerárquico versus K-Means: dos preguntas diferentes','ELECCIÓN DE MÉTODO',[
 'K-Means: partición de K grupos que minimiza inercia localmente.',
 'Jerárquico: secuencia de fusiones sujeta a distancia y linkage.',
 'Ward comparte con K-Means énfasis en SSE, pero no optimizan idénticamente.',
 'La elección depende de escalabilidad, forma, estabilidad y posibilidad de acción.'
 ],{visual:{type:'compare',rows:[['K-MEANS','K inicial, centroides, reasignación.'],['JERÁRQUICO','Árbol y cortes con niveles múltiples.'],['SIMILITUD','Ambos dependen de escala y variables.'],['PRUEBA','Perfiles + estabilidad + utilidad externa.']]},take:'El dendrograma aporta lectura multiescala, no superioridad universal.'}),
 s('Cuatro criterios para adoptar una segmentación','DECISIÓN RESPONSABLE',[
 'Estructura: separación, cohesión y alturas de fusión.',
 'Reproducibilidad: estabilidad frente a remuestreo y perturbaciones.',
 'Interpretabilidad: variables originales distinguen grupos.',
 'Viabilidad: costo de asignación, tamaño mínimo y tratamiento de clientes nuevos.'
 ],{visual:{type:'metrics',values:[['01','Estructura geométrica'],['02','Estabilidad de grupos'],['03','Perfiles interpretables'],['04','Valor y operación']]},take:'Sin valor diferencial verificable, una jerarquía compleja puede sobrar.'}),
 s('Simulaciones para reproducir cada transformación','LABORATORIOS M10',[
 'S10: construir matriz de distancias a partir de puntos movibles.',
 'S11: animar fusiones y actualizar dendrograma paso a paso.',
 'S12: comparar single, complete, average y Ward.',
 'S13: mover el umbral de corte y observar clusters resultantes.',
 'S14: estudiar chaining, sensibilidad y perfiles de negocio.'
 ],{visual:{type:'flow',items:['S10 · Distancias interactivas','S11 · Fusiones una a una','S12 · Linkages lado a lado','S13 · Corte y partición','S14 · Puentes / estabilidad / negocio']},take:'Cada control tiene que conectar cálculo, gráfico e interpretación.'}),
 s('Evaluación integradora: el árbol no decide por nosotros','ACTIVIDAD DE CIERRE',[
 'Single muestra dos grupos unidos por un puente; Ward muestra tres compactos.',
 'Cortar Ward en K=4 crea un grupo de 3 clientes con alto margen.',
 'En una submuestra desaparece ese microgrupo.',
 'Diseñar validaciones antes de asignar presupuesto comercial.'
 ],{visual:{type:'questions',items:['¿Cuál es el supuesto de cada linkage?','¿Qué evidencia favorece cierto corte?','¿Cuánto pesan tres clientes en el negocio?','¿Qué experimento validarías primero?']},take:'El método ofrece alternativas; el analista construye la decisión defendible.'}),
 s('Errores de lectura y fuentes esenciales','REFERENCIAS',[
 'Una hoja próxima en el gráfico no implica una distancia baja.',
 'La altura de Ward no debe leerse siempre como distancia euclídea literal.',
 'Murtagh & Contreras (2012). Algorithms for hierarchical clustering.',
 'Hastie, Tibshirani & Friedman (2009); SciPy hierarchy y scikit-learn Clustering.'
 ],{visual:{type:'flow',items:['Definir métrica + linkage','Construir y leer el árbol','Elegir y justificar el corte','Validar estabilidad + perfiles','Comprobar impacto del negocio']},take:'Las ramas sirven para investigar hipótesis, no para sustituir validación.'})
],'De la distancia entre observaciones a una jerarquía interpretable y operativa.');

Promise.all([make(PCA),make(KMEANS),make(HIER)]).then(v=>{for(const x of v)console.log(JSON.stringify(x))}).catch(e=>{console.error(e);process.exit(1)});