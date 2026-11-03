const {chromium}=require('playwright');
const fs=require('fs'),assert=require('node:assert/strict');
const path=require('node:path'),os=require('node:os');
const ROOT=path.resolve(__dirname,'../..');process.chdir(ROOT);
const OUT=process.env.MODULE11_TEST_OUTPUT||fs.mkdtempSync(path.join(os.tmpdir(),'module11-browser-'));fs.mkdirSync(OUT,{recursive:true});
const server=require('node:child_process').spawn('python',['-m','http.server','8766','--directory','docs'],{stdio:'ignore'});
process.on('exit',()=>server.kill());
(async()=>{
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
await new Promise(r=>setTimeout(r,500));
const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];
page.on('pageerror',e=>errors.push(String(e)));
const base='http://127.0.0.1:8766/modulos/11-redes-neuronales/experiencia/';
const labs=[['ppt-1-fundamentos','01_perceptron.html'],['ppt-1-fundamentos','02_activaciones.html'],['ppt-1-fundamentos','03_gradiente.html'],['ppt-1-fundamentos','04_umbral.html'],['ppt-2-rnn-lstm','05_memoria_lstm.html'],['ppt-1-fundamentos','06_backpropagation.html'],['ppt-1-fundamentos','07_generalizacion.html']];
let checks=[];
for(const [deck,file]of labs){
 await page.goto(base+deck+'/labs/'+file);await page.waitForFunction(()=>window.labDebug?.state.last);
 const initial=await page.evaluate(()=>labDebug.state);
 assert.equal(initial.step,0);await page.locator('#nextstep').click();assert.equal(await page.evaluate(()=>labDebug.state.step),1);
 await page.locator('#speed').selectOption('2');await page.locator('#auto').click();await page.locator('#auto').click();await page.waitForTimeout(720);
 assert.ok(await page.evaluate(()=>labDebug.state.step>=2));assert.equal(await page.evaluate(()=>labDebug.state.timers),1);
 await page.locator('#pause').click();const stopped=await page.evaluate(()=>labDebug.state.step);await page.waitForTimeout(450);assert.equal(await page.evaluate(()=>labDebug.state.step),stopped);
 await page.locator('#pause').click();await page.waitForTimeout(400);assert.ok(await page.evaluate(()=>labDebug.state.step)>stopped);await page.locator('#pause').click();
 for(const theme of ['light','contrast','dark']){await page.locator('#theme').selectOption(theme);assert.equal(await page.locator('html').getAttribute('data-theme'),theme);}
 const options=await page.locator('#scenario option').evaluateAll(e=>e.map(x=>x.value));assert.ok(options.length>=3);
 for(const option of options){await page.locator('#scenario').selectOption(option);await page.locator('#nextstep').click();assert.equal(await page.evaluate(()=>labDebug.state.step),1);assert.ok((await page.locator('#stats').textContent()).length>15);}
 await page.locator('#reset').click();assert.equal(await page.evaluate(()=>labDebug.state.step),0);assert.equal(await page.evaluate(()=>labDebug.state.timers),0);
 const dl=page.waitForEvent('download');await page.locator('#csv').click();const download=await dl;await download.saveAs(path.join(OUT,file+'.csv'));assert.ok(fs.readFileSync(path.join(OUT,file+'.csv'),'utf8').includes(','));
 await page.locator('#full').click();assert.ok(await page.evaluate(()=>!!document.fullscreenElement));await page.locator('#full').click();assert.equal(await page.evaluate(()=>!!document.fullscreenElement),false);
 await page.locator('#theme').selectOption('light');await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
 await page.setViewportSize({width:390,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:path.join(OUT,'mobile-'+file+'.png'),fullPage:true});await page.setViewportSize({width:1440,height:1000});
 checks.push({lab:file,passed:true,scenarios:options.length,autoplay:true,pauseResume:true,singleTimer:true,reset:true,csv:true,fullscreen:true,themes:true,mobile:true});
}
for(const [deck,total]of [['ppt-1-fundamentos',51],['ppt-2-rnn-lstm',34]]){
 await page.goto(base+deck+'/reader.html?slide=5');await page.waitForFunction(()=>document.getElementById('number').value==='5');
 await page.locator('#next').click();assert.equal(await page.locator('#number').inputValue(),'6');await page.locator('#previous').click();assert.equal(await page.locator('#number').inputValue(),'5');
 await page.locator('h1').click();await page.keyboard.press('End');assert.equal(await page.locator('#number').inputValue(),String(total));await page.keyboard.press('Home');assert.equal(await page.locator('#number').inputValue(),'1');
 await page.locator('#search').fill('sigmoide');if(deck.includes('fundamentos'))assert.ok(await page.locator('#toc button').count()>0);await page.locator('#search').fill('');
 await page.locator('#number').fill('15');await page.locator('#number').dispatchEvent('change');await page.locator('#fullscreen').click();assert.ok(await page.evaluate(()=>!!document.fullscreenElement));await page.locator('#fullscreen').click();
 await page.locator('#route').selectOption('essential');if(deck.includes('fundamentos'))assert.equal(await page.locator('#toc button').count(),28);
 for(let j=1;j<=total;j++){const r=await page.request.get(base+deck+`/slides/es/${String(j).padStart(2,'0')}.webp`);assert.equal(r.status(),200);}
 await page.screenshot({path:path.join(OUT,'reader-'+deck+'.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.setViewportSize({width:1440,height:1000});
 checks.push({reader:deck,slides:total,passed:true,keyboard:true,search:true,fullscreen:true,notes:true,mobile:true});
}
// Mecanismos nuevos y controles a tiempo fijo.
await page.goto(base+'ppt-1-fundamentos/labs/06_backpropagation.html');
const before=await page.evaluate(()=>labDebug.state.last);for(let j=0;j<4;j++)await page.locator('#nextstep').click();const after=await page.evaluate(()=>labDebug.state.last);assert.ok(after.loss<before.loss);assert.ok(Math.abs(after.w-before.wn)<1e-10);assert.equal(await page.locator('#nn-flow rect').count(),4);
await page.goto(base+'ppt-1-fundamentos/labs/07_generalizacion.html');await page.locator('#degree').fill('9');await page.locator('#degree').dispatchEvent('input');const high=await page.evaluate(()=>labDebug.state.last);await page.locator('#degree').fill('3');await page.locator('#degree').dispatchEvent('input');const low=await page.evaluate(()=>labDebug.state.last);assert.ok(high.trainMSE<low.trainMSE&&high.validMSE>low.validMSE);
await page.goto(base+'ppt-2-rnn-lstm/labs/05_memoria_lstm.html');await page.locator('#time').fill('10');await page.locator('#time').dispatchEvent('input');const stored=await page.evaluate(()=>labDebug.state.last.c);await page.locator('#output').fill('0');await page.locator('#output').dispatchEvent('input');assert.equal(await page.evaluate(()=>labDebug.state.step),10);assert.equal(await page.evaluate(()=>labDebug.state.last.c),stored);assert.equal(await page.evaluate(()=>labDebug.state.last.h),0);
await page.goto(base+'ppt-1-fundamentos/reader.html?slide=22');await page.locator('#related a[href*=temas]').click();assert.ok(page.url().endsWith('#aprendizaje'));assert.equal(await page.locator('.topic-article').count(),6);
// Todas las portadas, guías y páginas de video deben abrir sin errores.
for(const deck of ['ppt-1-fundamentos','ppt-2-rnn-lstm'])for(const name of ['index.html','guide.html','lab.html','videos.html','temas.html']){await page.goto(base+deck+'/'+name);assert.equal(await page.locator('h1').count(),1);}
await page.goto(base+'index.html');await page.locator('#theme').selectOption('dark');await page.screenshot({path:path.join(OUT,'portada.png'),fullPage:true});
await page.goto(base+'ppt-1-fundamentos/labs/04_umbral.html');await page.locator('#nextstep').click();await page.screenshot({path:path.join(OUT,'umbral-desktop.png'),fullPage:true});
await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#reset').click();await page.locator('#auto').click();await page.waitForTimeout(300);assert.equal(await page.evaluate(()=>labDebug.state.step),0);await page.locator('#pause').click();
await page.goto(base+'ppt-1-fundamentos/reader.html?slide=43&route=essential');await page.locator('#related a[href*="labs/"]').first().click();assert.ok(page.url().includes('slide=43'));await page.locator('#return-slide').click();assert.ok(page.url().includes('slide=43'));assert.ok(page.url().includes('route=essential'));
assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'browser-results.json'),JSON.stringify({checks,errors},null,2));console.log(JSON.stringify({passed:checks.length,errors}));await browser.close();server.kill();
})().catch(e=>{console.error(e);process.exit(1)});
