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
const NNMath={sigmoid,softplus,bce,points,predict,perceptron,activation,logistic,rng,cohort,confusion,lstm,candidate};
if(typeof module!=='undefined')module.exports=NNMath;
if(typeof window!=='undefined')window.NNMath=NNMath;
