"""Referencia independiente NumPy para el ajuste del laboratorio JS."""
from pathlib import Path
import subprocess,json,numpy as np
src=Path(__file__).parent
raw=subprocess.check_output(['node','-e',"const M=require('./math.cjs');console.log(JSON.stringify(['small','more','noisy'].flatMap(s=>[1,3,9].flatMap(d=>[0,.1,1].map(l=>M.fitExperiment(d,l,s))))));"],cwd=src)
for f in json.loads(raw):
 x=np.array([p['x'] for p in f['train']]);y=np.array([p['y'] for p in f['train']]);A=np.polynomial.chebyshev.chebvander(x,f['degree'])
 penalty=np.eye(f['degree']+1)*np.sqrt(len(x)*f['lambda']);penalty[0,0]=0
 w=np.linalg.lstsq(np.vstack([A,penalty]),np.r_[y,np.zeros(len(penalty))],rcond=None)[0]
 np.testing.assert_allclose(w,f['weights'],rtol=1e-9,atol=1e-10)
 xv=np.array([p['x'] for p in f['valid']]);yv=np.array([p['y'] for p in f['valid']]);mse=np.mean((np.polynomial.chebyshev.chebval(xv,w)-yv)**2)
 np.testing.assert_allclose(mse,f['validMSE'],rtol=1e-10)
print('PASS: 27 ajustes y errores contrastados con NumPy lstsq')
