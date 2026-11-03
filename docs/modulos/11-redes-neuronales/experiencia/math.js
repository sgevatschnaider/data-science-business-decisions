'use strict';
// Núcleo compartido por el navegador y las pruebas Node. Sin dependencias.
const sigmoid=x=>x>=0?1/(1+Math.exp(-x)):Math.exp(x)/(1+Math.exp(x));
const softplus=x=>Math.max(x,0)+Math.log1p(Math.exp(-Math.abs(x)));
const bce=(z,y)=>softplus(z)-y*z;
const points=kind=>[[0,0],[0,1],[1,0],[1,1]].map(([x,y])=>({x,y,label:kind==='xor'?+(x!==y):kind==='and'?+(x&&y):+(x||y)}));
const predict=(p,w)=>+(p.x*w[0]+p.y*w[1]+w[2]>=0);
function perceptron(kind,w,eta=.15){let q=[...w];for(const p of points(kind)){const e=p.label-predict(p,q);q[0]+=eta*e*p.x;q[1]+=eta*e*p.y;q[2]+=eta*e;}return q;}
function activation(kind,z){if(kind==='sigmoid'){let a=sigmoid(z);return[a,a*(1-a)];}if(kind==='tanh'){let a=Math.tanh(z);return[a,1-a*a];}if(kind==='relu')return[Math.max(0,z),z===0?null:+(z>0)];return[z<0?.1*z:z,z===0?null:z<0?.1:1];}
const DATA=[[-2,0],[-1,0],[1,1],[2,1]];
function logistic(w,b){let loss=0,gw=0,gb=0;for(let[x,y]of DATA){let z=w*x+b,e=sigmoid(z)-y;loss+=bce(z,y);gw+=e*x;gb+=e;}return{loss:loss/4,gw:gw/4,gb:gb/4};}
function rng(seed=991){let s=seed>>>0;return()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296;};}
function cohort(seed=991,n=100){let r=rng(seed),p=[];for(let j=0;j<n;j++){let score=.02+.6*r()**3;p.push({p:score,y:+(r()<score)});}return p;}
function confusion(data,threshold,B=100,C=5,q=.4){let TP=0,FP=0,FN=0,TN=0;for(const p of data){if(p.p>=threshold){if(p.y)TP++;else FP++;}else{if(p.y)FN++;else TN++;}}const contacts=TP+FP;return{TP,FP,FN,TN,contacts,precision:contacts?TP/contacts:null,recall:TP+FN?TP/(TP+FN):null,utility:TP*q*B-contacts*C};}
function lstm(f,i,o,g,c){const cell=f*c+i*g;return{c:cell,h:o*Math.tanh(cell)};}
function candidate(s,t){return s==='impulse'?(t===1?1:0):s==='alternating'?(t%2?1:-1):t===1?1:t===12?-1:0;}
function xorRepresentation(x1,x2){const h1=Math.max(0,x1+x2),h2=Math.max(0,x1+x2-1);return {h1,h2,output:h1-2*h2};}
function singleNeuron(x,y,w,b,eta=.1){const z=x*w+b,p=sigmoid(z),loss=bce(z,y),gw=(p-y)*x,gb=p-y,wn=w-eta*gw,bn=b-eta*gb;return{x,y,w,b,z,p,loss,gw,gb,wn,bn,newLoss:bce(x*wn+bn,y)};}
function chebyshev(x,d){const a=[1];if(d>0)a.push(x);for(let j=2;j<=d;j++)a.push(2*x*a[j-1]-a[j-2]);return a;}
function solve(A,b){const a=A.map((r,i)=>[...r,b[i]]),n=b.length;for(let k=0;k<n;k++){let pivot=k;for(let j=k+1;j<n;j++)if(Math.abs(a[j][k])>Math.abs(a[pivot][k]))pivot=j;[a[k],a[pivot]]=[a[pivot],a[k]];if(Math.abs(a[k][k])<1e-12)throw Error('Sistema singular');const v=a[k][k];for(let j=k;j<=n;j++)a[k][j]/=v;for(let i=0;i<n;i++)if(i!==k){const f=a[i][k];for(let j=k;j<=n;j++)a[i][j]-=f*a[k][j];}}return a.map(r=>r[n]);}
function fitExperiment(degree=3,lambda=0,scenario='small'){
 const rand=rng(42),n=scenario==='more'?32:12,noise=scenario==='noisy'?.55:.22;
 const truth=x=>Math.sin(3*x)+.25*x;
 const train=Array.from({length:n},(_,j)=>{const x=-1+2*j/(n-1);return{x,y:truth(x)+noise*(2*rand()-1)};});
 const valid=Array.from({length:60},(_,j)=>{const x=-.98+1.96*j/59;return{x,y:truth(x)+noise*(2*rand()-1)};});
 const A=Array.from({length:degree+1},()=>Array(degree+1).fill(0)),b=Array(degree+1).fill(0);
 for(const p of train){const v=chebyshev(p.x,degree);for(let i=0;i<v.length;i++){b[i]+=v[i]*p.y;for(let j=0;j<v.length;j++)A[i][j]+=v[i]*v[j];}}
 // Objetivo: promedio de errores cuadrados + lambda por norma; intercepto sin penalización.
 for(let j=1;j<A.length;j++)A[j][j]+=n*lambda;
 const weights=solve(A,b),predict=x=>chebyshev(x,degree).reduce((s,v,j)=>s+v*weights[j],0),mse=data=>data.reduce((s,p)=>s+(predict(p.x)-p.y)**2,0)/data.length;
 return{degree,lambda,scenario,train,valid,weights,trainMSE:mse(train),validMSE:mse(valid),curve:Array.from({length:161},(_,j)=>{const x=-1+2*j/160;return{x,y:predict(x),truth:truth(x)};})};
}
const NNMath={sigmoid,softplus,bce,points,predict,perceptron,activation,logistic,rng,cohort,confusion,lstm,candidate,xorRepresentation,singleNeuron,chebyshev,solve,fitExperiment};
if(typeof module!=='undefined')module.exports=NNMath;
if(typeof window!=='undefined')window.NNMath=NNMath;
