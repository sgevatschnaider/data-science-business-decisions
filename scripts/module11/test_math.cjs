const assert=require('node:assert/strict'),M=require('./math.cjs');
const near=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<tol,`${a} ≠ ${b}`);
for(const z of [-1000,-100,0,100,1000])assert.ok(Number.isFinite(M.sigmoid(z)));
near(M.sigmoid(.5),.6224593312018546);
near(M.bce(.5,1),.4740769841801067);
near(M.activation('sigmoid',0)[1],.25);near(M.activation('tanh',0)[1],1);
assert.equal(M.activation('relu',0)[1],null);
assert.equal(M.activation('leaky',0)[1],null);
near(M.activation('leaky',-2)[0],-.2);near(M.activation('leaky',-2)[1],.1);
for(const w of [-.7,0,1.3])for(const b of [-.2,.8]){
 const e=1e-5,a=M.logistic(w,b),fd=(M.logistic(w+e,b).loss-M.logistic(w-e,b).loss)/(2*e);
 near(a.gw,fd);near(a.gb,(M.logistic(w,b+e).loss-M.logistic(w,b-e).loss)/(2*e));
}
let loss=M.logistic(-.5,.2),w=-.5-.1*loss.gw,b=.2-.1*loss.gb;
assert.ok(M.logistic(w,b).loss<loss.loss);
for(const kind of ['or','and']){let q=[-.5,.2,-.1];for(let j=0;j<40;j++)q=M.perceptron(kind,q,.15);assert.equal(M.points(kind).filter(p=>M.predict(p,q)!==p.label).length,0);}
// Exhaustive grid cannot prove the XOR theorem, but rejects accidental label mutation.
for(const q of [[1,1,-.5],[-1,-1,.5],[1,-1,0]])assert.ok(M.points('xor').some(p=>M.predict(p,q)!==p.label));
for(const p of M.points('xor'))near(Math.max(0,p.x+p.y)-2*Math.max(0,p.x+p.y-1),p.label);
assert.deepEqual(M.cohort(991),M.cohort(991));assert.notDeepEqual(M.cohort(991),M.cohort(992));
let c=M.cohort(991);for(const th of [0,.2,.5,1]){let r=M.confusion(c,th);assert.equal(r.TP+r.FP+r.FN+r.TN,100);near(r.utility,r.TP*.4*100-r.contacts*5);}
assert.equal(M.confusion(c,1).contacts,0);assert.equal(M.confusion(c,1).precision,null);assert.equal(M.confusion(c,0).contacts,100);
const ex=[{p:.8,y:1},{p:.7,y:0},{p:.2,y:1}];near(M.confusion(ex,.5,100,5,.4).utility,30);
let state=M.lstm(.9,.2,.75,-.5,.8);near(state.c,.62);near(state.h,.4133460214036102);
near(M.lstm(1,0,.75,1,.8).c,.8);near(M.lstm(0,0,1,0,.8).c,0);
let cell=.5;for(let j=0;j<10;j++)cell=M.lstm(.9,0,1,0,cell).c;near(cell,.5*.9**10);
assert.ok(Math.abs((-2)*(1-2.2)**10)>2);assert.ok(Math.abs((-2)*(1-.6)**10)<.001);
console.log('PASS: Pruebas matemáticas, gradientes, semilla, extremos y recorrencias');
for(const x of [-2,0,2])for(const y of [0,1])for(const w of [-.7,.3,2]){
 const q=M.singleNeuron(x,y,w,-.1,.1),e=1e-5;
 near(q.gw,(M.bce(x*(w+e)-.1,y)-M.bce(x*(w-e)-.1,y))/(2*e));
 near(q.gb,(M.bce(x*w-.1+e,y)-M.bce(x*w-.1-e,y))/(2*e));
 if(q.loss>1e-10)assert.ok(q.newLoss<=q.loss+1e-12);
}
near(M.singleNeuron(2,1,.3,-.1,.1).newLoss,.40692573262852194,1e-6);
for(const p of M.points('xor'))near(M.xorRepresentation(p.x,p.y).output,p.label);
for(const scenario of ['small','more','noisy'])for(const degree of [1,3,9])for(const lambda of [0,.1,1]){
 const f=M.fitExperiment(degree,lambda,scenario);assert.ok(f.weights.every(Number.isFinite));assert.ok(f.trainMSE>=0&&f.validMSE>=0);
 assert.equal(f.train.length,scenario==='more'?32:12);assert.equal(f.valid.length,60);
}
assert.ok(M.fitExperiment(9).trainMSE<M.fitExperiment(3).trainMSE);
assert.ok(M.fitExperiment(9).validMSE>M.fitExperiment(3).validMSE);
console.log('PASS: backprop por diferencias finitas y experimento de capacidad');
