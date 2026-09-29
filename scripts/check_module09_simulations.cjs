'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const directory=process.argv[2]||path.join(__dirname,'../modules/09-arboles-ensembles/site/simuladores');
const files=fs.readdirSync(directory).filter(f=>/^simulador_\d{2}_.*\.html$/.test(f)).sort();assert.equal(files.length,16,'Se requieren 16 simulaciones');
const report=[];
for(const file of files){
 const started=Date.now(),html=fs.readFileSync(path.join(directory,file),'utf8'),elements=new Map(),ranges=[],selects=[];
 const attr=s=>Object.fromEntries([...s.matchAll(/([\w-]+)\s*=\s*["']([^"']*)["']/g)].map(m=>[m[1],m[2]]));
 for(const tag of html.matchAll(/<([\w-]+)\b([^>]*)>/g)){
  const attrs=attr(tag[2]);if(!attrs.id)continue;assert(!elements.has(attrs.id),'ID duplicado '+attrs.id);
  const e={id:attrs.id,tagName:tag[1].toUpperCase(),value:attrs.value??'',textContent:'',innerHTML:'',events:{},options:[],addEventListener(type,fn){(this.events[type]??=[]).push(fn)},dispatch(type){for(const fn of this.events[type]??[])fn({target:this});if(type==='click'&&this.onclick)this.onclick({target:this})}};
  if(tag[1]==='select'){
   const body=html.slice(tag.index+tag[0].length).split('</select>')[0];e.options=[...body.matchAll(/<option\b([^>]*)>([^<]*)<\/option>/g)].map(m=>({value:attr(m[1]).value??m[2],selected:/\bselected\b/.test(m[1])}));e.value=(e.options.find(o=>o.selected)||e.options[0]).value;selects.push(e);
  }
  if(tag[1]==='input'&&attrs.type==='range'){e.min=Number(attrs.min);e.max=Number(attrs.max);ranges.push(e)}elements.set(attrs.id,e);
 }
 const timers=[],document={documentElement:{dataset:{theme:'dark'}},getElementById(id){assert(elements.has(id),'ID ausente '+id);return elements.get(id)}};
 const context=vm.createContext({document,console,setTimeout(fn){timers.push(fn);return timers.length},clearTimeout(){}});
 const scripts=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);assert(scripts.length,'Falta JavaScript');
 for(const source of scripts)new vm.Script(source,{filename:file}).runInContext(context,{timeout:180000});
 const metrics=[...html.matchAll(/<strong id="([^"]+)"/g)].map(m=>m[1]);
 const snapshot=()=>[...elements.values()].map(e=>String(e.textContent)+'\n'+String(e.innerHTML)).join('\n');
 const healthy=()=>{for(const id of metrics)assert(String(elements.get(id).textContent).trim(),'Métrica vacía '+id);assert(!/NaN|Infinity|undefined/.test(snapshot()),'Resultado numérico inválido '+file)};healthy();
 const initialValues=ranges.concat(selects).map(e=>[e,e.value]);const reset=elements.get('resetBtn');assert(reset,'Falta Restablecer');
 let exercised=0;
 for(const e of ranges){let outputs=[];for(const v of [e.min,e.max]){e.value=String(v);e.dispatch('input');healthy();outputs.push(snapshot());exercised++}assert.notEqual(outputs[0],outputs[1],'Control inactivo '+e.id);reset.dispatch('click');healthy()}
 for(const e of selects){let outputs=[];for(const o of e.options){e.value=o.value;e.dispatch('change');healthy();outputs.push(snapshot());exercised++}if(outputs.length>1)assert(new Set(outputs).size>1,'Selector inactivo '+e.id);reset.dispatch('click');healthy()}
 for(const e of elements.values()){if(e.tagName==='BUTTON'&&!['resetBtn','themeBtn'].includes(e.id)){e.dispatch('click');while(timers.length)timers.shift()();healthy();exercised++}}
 reset.dispatch('click');for(const [e,v] of initialValues)assert.equal(e.tagName==='INPUT'?Number(e.value):String(e.value),e.tagName==='INPUT'?Number(v):String(v),'Restablecer no recupera '+e.id);
 const theme=elements.get('themeBtn');theme.dispatch('click');assert.equal(document.documentElement.dataset.theme,'light');theme.dispatch('click');assert.equal(document.documentElement.dataset.theme,'dark');
 const seconds=(Date.now()-started)/1000;const row={file,controls:ranges.length+selects.length,interactions:exercised+3,seconds:Number(seconds.toFixed(2)),status:'PASS'};report.push(row);console.log(file,row.status,row.interactions,'interacciones',row.seconds+'s');
}
console.log('16 simulaciones: carga, extremos de controles, selectores, botones y restablecimiento correctos.');
if(process.env.M09_QA_REPORT)fs.writeFileSync(process.env.M09_QA_REPORT,JSON.stringify(report,null,2));
