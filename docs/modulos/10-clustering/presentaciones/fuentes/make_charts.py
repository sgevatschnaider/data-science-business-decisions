import os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from sklearn.datasets import make_blobs, make_moons
from numpy.linalg import eigh
from matplotlib.colors import ListedColormap

DIR=os.path.join(os.path.dirname(__file__),'assets'); os.makedirs(DIR,exist_ok=True)
BG='#101F37'; WHITE='#E7F2FD'; SUB='#9FB4CC'; GRID='#30435D'; TEAL='#48DFC5'; BLUE='#72A7FA'; AMBER='#FFCB70'; PINK='#F487C8'; GREEN='#8CE3A7'; COLORS=[TEAL,BLUE,AMBER,PINK,GREEN]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':WHITE,'axes.labelcolor':SUB,'xtick.color':SUB,'ytick.color':SUB,'axes.edgecolor':GRID,'axes.facecolor':BG,'figure.facecolor':BG,'grid.color':GRID,'savefig.facecolor':BG,'axes.titlecolor':WHITE,'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False})
rng=np.random.default_rng(33)
def fig(title='',axis=True):
 f,a=plt.subplots(figsize=(8.6,5.2),dpi=160);f.patch.set_facecolor(BG);a.set_facecolor(BG)
 if title:a.set_title(title,loc='left',fontweight='bold',pad=14)
 if axis:a.grid(alpha=.26);a.set_axisbelow(True)
 return f,a
def save(f,name):
 f.savefig(os.path.join(DIR,name+'.png'),dpi=160,bbox_inches='tight',pad_inches=.22);plt.close(f)
def scat(a,x,colors=None,s=36,alpha=.82,**kw):
 if colors is None: colors=TEAL
 a.scatter(x[:,0],x[:,1],s=s,c=colors,alpha=alpha,edgecolors=BG,linewidths=.6,**kw)
# dataset PCA
x=rng.normal(size=(180,2));R=np.array([[2.9,1.0],[1.6,0.8]]);X=x@R.T+np.array([5,4]); Z=StandardScaler().fit_transform(X);model=PCA().fit(Z)
f,a=fig('La mayor variación se concentra en una dirección')
scat(a,X,c=TEAL) if False else scat(a,X)
means=X.mean(axis=0); w,v=np.linalg.eigh(np.cov(X.T));order=np.argsort(w)[::-1]
for j,c in enumerate([AMBER,PINK]):
 vv=v[:,order[j]];a.arrow(means[0],means[1], vv[0]*2.6,vv[1]*2.6,head_width=.25,color=c,lw=3, length_includes_head=True);a.text(*(means+vv*3.0),['PC1','PC2'][j],color=c,weight='bold')
a.set(xlabel='Frecuencia de compra (escala ilustrativa)',ylabel='Valor monetario (escala ilustrativa)');save(f,'pca_geometry')
f,a=fig('Centrar = trasladar el origen sin deformar distancias')
scat(a,X,colors=BLUE,s=19,alpha=.38);scat(a,X-means,colors=TEAL,s=19,alpha=.53)
a.axhline(0,color=SUB,lw=1);a.axvline(0,color=SUB,lw=1);a.scatter([means[0],0],[means[1],0],color=[BLUE,TEAL],marker='X',s=150)
a.text(0.01,.98,'AZUL: sin centrar     ·     VERDE: centrado',transform=a.transAxes,color=SUB,va='top');a.set(xlabel='Variable 1',ylabel='Variable 2');save(f,'pca_center')
f,axs=plt.subplots(1,2,figsize=(9,5.1),dpi=160)
for a in axs:a.set_facecolor(BG);a.grid(alpha=.22);a.set_axisbelow(True)
scale=np.array([100,1]);Y=np.column_stack((rng.normal(45,15,130),rng.normal(2,0.8,130)))
axs[0].scatter(Y[:,0],Y[:,1],s=22,c=BLUE,alpha=.7);axs[0].set_title('Unidades originales',color=WHITE);axs[0].set_xlabel('Facturación ($) / 100',color=SUB);axs[0].set_ylabel('Frecuencia',color=SUB)
Ys=StandardScaler().fit_transform(Y);axs[1].scatter(Ys[:,0],Ys[:,1],s=22,c=TEAL,alpha=.7);axs[1].set_title('Escala Z (media 0, desvío 1)',color=WHITE);axs[1].set_xlabel('Facturación estandarizada',color=SUB);axs[1].set_ylabel('Frecuencia estandarizada',color=SUB)
for a in axs:a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'pca_scale')
f,a=fig('Covarianza: magnitud + dirección de la relación')
S=np.cov(X.T);im=a.imshow(S,cmap='YlGnBu',vmin=0,vmax=S.max()*1.05)
for i in range(2):
 for j in range(2):a.text(j,i,f'{S[i,j]:.2f}',ha='center',va='center',fontsize=22,color='#061529',weight='bold')
a.set_xticks([0,1],['Frecuencia','Valor']);a.set_yticks([0,1],['Frecuencia','Valor']);save(f,'pca_covariance')
# scree realistic: 5 var synthetic
Lat=rng.normal(size=(300,2));A=np.array([[1,0.2],[.8,.1],[.5,.9],[.2,.8],[.3,-.4]])
XX=Lat@A.T + rng.normal(0,.40,size=(300,5));Xp=StandardScaler().fit_transform(XX);p5=PCA().fit(Xp)
ev=p5.explained_variance_ratio_;cs=np.cumsum(ev)
f,a=fig('Varianza individual y acumulada: dos criterios diferentes')
idx=np.arange(1,6);a.bar(idx,ev*100,color=[TEAL,BLUE,BLUE,BLUE,BLUE],alpha=.9,width=.65)
a2=a.twinx();a2.plot(idx,cs*100,color=AMBER,lw=3,marker='o');a2.set_ylim(0,110);a2.tick_params(colors=AMBER);a.set_ylim(0,85);a.set_xticks(idx);a.set_xlabel('Número de componente');a.set_ylabel('Varianza individual (%)');a2.set_ylabel('Varianza acumulada (%)',color=AMBER)
for i,v in enumerate(ev):a.text(i+1,v*100+2,f'{v:.0%}',ha='center',color=WHITE,fontsize=10)
save(f,'pca_scree')
f,a=fig('Reconstrucción: qué información se pierde con 1 componente')
scat(a,Z,colors=BLUE,s=27,alpha=.32);p=PCA(n_components=1).fit(Z);zr=p.inverse_transform(p.transform(Z));scat(a,zr,colors=AMBER,s=23,alpha=.72)
for i in range(0,len(Z),10):a.plot([Z[i,0],zr[i,0]],[Z[i,1],zr[i,1]],lw=.75,color=SUB,alpha=.4)
a.set(xlabel='Z₁',ylabel='Z₂');a.text(.02,.97,'AZUL: original   ·   DORADO: reconstruido',transform=a.transAxes,ha='left',va='top',color=SUB);save(f,'pca_reconstruct')
f,a=fig('Biplot: clientes y variables en el mismo plano')
pcs=p5.transform(Xp);scat(a,pcs[:,0:2],colors=BLUE,s=13,alpha=.25)
for j,lab in enumerate(['Recencia','Frecuencia','Gasto','Uso app','Descuento']):
 xy=p5.components_[:2,j]*3.5;a.annotate('',xy=xy,xytext=(0,0),arrowprops=dict(arrowstyle='-|>',color=[TEAL,AMBER,PINK,GREEN,BLUE][j],lw=2.4));a.text(xy[0]*1.08,xy[1]*1.08,lab,color=[TEAL,AMBER,PINK,GREEN,BLUE][j],fontsize=10)
a.axhline(0,color=SUB,lw=.8);a.axvline(0,color=SUB,lw=.8);a.set(xlabel='PC1 · combinación de variables',ylabel='PC2 · estructura residual');save(f,'pca_biplot')
Xp2=np.vstack([X,[[19,-4]]]);f,axs=plt.subplots(1,2,figsize=(9,5.2),dpi=160)
for a,y,t in zip(axs,[X,Xp2],['Sin extremo','Con extremo']):
 a.set_facecolor(BG);a.scatter(y[:,0],y[:,1],s=15,c=BLUE,alpha=.5)
 if len(y)>180:a.scatter(y[-1,0],y[-1,1],s=140,marker='X',c=PINK)
 w,v=eigh(np.cov(y.T));d=v[:,np.argmax(w)];m=y.mean(0);a.plot([m[0]-d[0]*9,m[0]+d[0]*9],[m[1]-d[1]*9,m[1]+d[1]*9],c=AMBER,lw=3);a.set_title(t,color=WHITE);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'pca_outlier')
# business data 3 groups
centers=np.array([[-3,-1],[0,2.8],[3,-.7]]);stds=[.65,.7,.67];Xb=np.vstack([rng.normal(loc=c,scale=std,size=(70,2)) for c,std in zip(centers,stds)]);truth=np.repeat(np.arange(3),70)
f,a=fig('Una misma muestra: 210 clientes, tres patrones sintéticos')
scat(a,Xb,colors=BLUE,s=25,alpha=.75);a.set(xlabel='Frecuencia estandarizada',ylabel='Margen estandarizado');save(f,'business_cloud')
# kmeans sequence random manual
init=np.array([[-4,2],[-2,3],[4,2]])
assign0=np.argmin(((Xb[:,None,:]-init[None,:,:])**2).sum(axis=2),axis=1)
c1=np.vstack([Xb[assign0==j].mean(axis=0) for j in range(3)])
assign1=np.argmin(((Xb[:,None,:]-c1[None,:,:])**2).sum(axis=2),axis=1)
c2=np.vstack([Xb[assign1==j].mean(axis=0) for j in range(3)])
model3=KMeans(n_clusters=3,n_init=20,random_state=13).fit(Xb)
for name,ct,lab,tit in [('k_init',init,assign0,'Paso 0 · centroides iniciales'),('k_iter1',c1,assign1,'Paso 1 · asignar y recalcular'),('k_final',model3.cluster_centers_,model3.labels_,'Convergencia · clusters estables')]:
 f,a=fig(tit)
 for j in range(3):scat(a,Xb[lab==j],colors=COLORS[j],s=25,alpha=.73)
 a.scatter(ct[:,0],ct[:,1],s=230,c=[COLORS[j] for j in range(3)],marker='X',edgecolors='#ffffff',linewidth=2,zorder=4)
 a.set_xlim(-5.2,5.3);a.set_ylim(-3.7,4.5);a.set(xlabel='Frecuencia (Z)',ylabel='Margen (Z)');save(f,name)
# Voronoi
f,a=fig('La frontera de decisión une centroides y geometría')
xx,yy=np.meshgrid(np.linspace(-5,5,280),np.linspace(-3.5,4.8,250));pred=model3.predict(np.c_[xx.ravel(),yy.ravel()]).reshape(xx.shape)
a.contourf(xx,yy,pred,alpha=.20,levels=np.arange(-.5,3.5,1),colors=[TEAL,BLUE,AMBER]);
for j in range(3):scat(a,Xb[model3.labels_==j],colors=COLORS[j],s=14)
a.scatter(model3.cluster_centers_[:,0],model3.cluster_centers_[:,1],marker='X',c=WHITE,s=150,edgecolor=BG);a.set(xlabel='Frecuencia (Z)',ylabel='Margen (Z)');save(f,'k_regions')
# elbow
ks=np.arange(1,10);loss=[];sil=[]
from sklearn.metrics import silhouette_score
for k in ks:
 mdl=KMeans(n_clusters=int(k),random_state=42,n_init=15).fit(Xb);loss.append(mdl.inertia_);sil.append(silhouette_score(Xb,mdl.labels_) if k>1 else np.nan)
f,axs=plt.subplots(1,2,figsize=(9.1,5.0),dpi=160)
for a in axs:a.set_facecolor(BG);a.grid(alpha=.2);a.set_axisbelow(True);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
axs[0].plot(ks,loss,'o-',color=TEAL,lw=3);axs[0].axvline(3,color=AMBER,ls='--');axs[0].set_title('Inercia: siempre desciende',color=WHITE);axs[0].set_xlabel('K',color=SUB)
axs[1].plot(ks[1:],np.array(sil)[1:],'o-',color=BLUE,lw=3);axs[1].axvline(3,color=AMBER,ls='--');axs[1].set_title('Silhouette: separar vs compactar',color=WHITE);axs[1].set_xlabel('K',color=SUB)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'k_metrics')
# silhouette
svals=silhouette_samples(Xb,model3.labels_);f,a=fig('Silhouette por cluster: inspeccionar el perfil, no solo promedio')
y_lower=12
for j in range(3):
 v=np.sort(svals[model3.labels_==j]);count=len(v);a.fill_betweenx(np.arange(y_lower,y_lower+count),0,v,color=COLORS[j],alpha=.83);a.text(-.11,y_lower+count/2,f'C{j+1}',color=WHITE);y_lower+=count+12
a.axvline(np.mean(svals),color=AMBER,lw=2,ls='--');a.set(xlim=(-.3,1),xlabel='Silhouette de cada observación',ylabel='Clientes ordenados por cluster');save(f,'k_silhouette')
f,axs=plt.subplots(1,2,figsize=(9,5.1),dpi=160)
for a,dat,t in zip(axs,[Xb,np.vstack([Xb,[[12,12]]])],['Sin extremo','Con cliente excepcional']):
 km=KMeans(n_clusters=3,random_state=20,n_init=20).fit(dat);a.set_facecolor(BG)
 for j in range(3):scat(a,dat[km.labels_==j],colors=COLORS[j],s=12)
 a.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],marker='X',s=160,c=WHITE,edgecolor=BG);a.set_title(t,color=WHITE);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'k_outlier')
Xm,ym=make_moons(n_samples=350,noise=.07,random_state=9);km=KMeans(n_clusters=2,n_init=15,random_state=9).fit(Xm)
f,axs=plt.subplots(1,2,figsize=(9,4.7),dpi=160)
for a,labels,t in zip(axs,[ym,km.labels_],['Estructura de medias lunas','K-Means impone regiones convexas']):
 a.set_facecolor(BG)
 for j in range(2):scat(a,Xm[labels==j],colors=COLORS[j],s=15)
 a.set_title(t,color=WHITE);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'k_moons')
# anisotropy
Xan,y = make_blobs(n_samples=290,centers=3,random_state=50);Xan=Xan@np.array([[.5,-.7],[-.6,.85]]);km=KMeans(n_clusters=3,n_init=15,random_state=10).fit(Xan)
f,a=fig('Clusters alargados: la inercia favorece esferas')
for j in range(3):scat(a,Xan[km.labels_==j],colors=COLORS[j],s=25,alpha=.75)
a.set(xlabel='Dimensión 1',ylabel='Dimensión 2');save(f,'k_anisotropy')
# random init stability
Xclose=np.vstack([rng.normal([-2,-1],[1.25,.7],(70,2)),rng.normal([0,1],[1.5,.6],(75,2)),rng.normal([2,0],[1.4,1],(65,2))]);f,axs=plt.subplots(1,2,figsize=(9,5.2),dpi=160)
for a,seed,t in zip(axs,[1,13],['Semilla 1','Semilla 13']):
 km=KMeans(n_clusters=3,n_init=1,init='random',random_state=seed).fit(Xclose);a.set_facecolor(BG)
 for j in range(3):scat(a,Xclose[km.labels_==j],colors=COLORS[j],s=14)
 a.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],c=WHITE,marker='X',s=120);a.set_title(t,color=WHITE);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'k_stability')
# business profile
cols=['Recencia','Frecuencia','Margen','Uso digital'];profiles=np.array([[1.4,-.6,-.7,-.8],[-.7,1.3,1.15,.9],[.1,-.2,.2,1.35]])
f,a=fig('Perfil relativo de tres segmentos (valores Z sintéticos)')
loc=np.arange(len(cols));w=.24
for j in range(3):a.bar(loc+(j-1)*w,profiles[j],width=w,color=COLORS[j],label=f'Segmento {j+1}')
a.set_xticks(loc,cols);a.set_ylim(-1.55,1.85);a.axhline(0,color=SUB,lw=1);a.legend(frameon=False,labelcolor=WHITE,ncol=3,loc='upper right');save(f,'business_profiles')
# hier data use same Xb subset more legible dendrogram ~12 points
Xsmall=np.array([[-3,-.8],[-2.7,-1.35],[-3.25,-1.35],[-.8,2.3],[0,2.65],[.6,3.1],[2.5,-1],[3.2,-.6],[3.6,-1.1],[1.15,.4],[1.55,.3],[1.9,.35]])
labels=[f'P{i:02}' for i in range(1,len(Xsmall)+1)]
f,a=fig('Distancias entre puntos: punto de partida de la jerarquía')
scat(a,Xsmall,colors=TEAL,s=85)
for i,q in enumerate(Xsmall):a.annotate(labels[i],q+np.array([.08,.12]),fontsize=9,color=WHITE)
a.set(xlabel='Frecuencia estandarizada',ylabel='Margen estandarizado');save(f,'h_points')
f,a=fig('Matriz de distancias euclídeas entre 12 clientes')
DM=squareform(pdist(Xsmall));im=a.imshow(DM,cmap='magma_r');a.set_xticks(range(12),labels,rotation=45);a.set_yticks(range(12),labels);f.colorbar(im,ax=a,shrink=.8).ax.tick_params(colors=SUB);save(f,'h_matrix')
# 4 dendrograms
for meth in ['single','complete','average','ward']:
 f,a=fig({'single':'Single linkage · vecinos más próximos','complete':'Complete linkage · peor distancia','average':'Average linkage · distancia promedio','ward':'Ward · menor aumento de SSE'}[meth])
 L=linkage(Xsmall,method=meth,metric='euclidean');dendrogram(L,labels=labels,ax=a,leaf_rotation=0,leaf_font_size=9,color_threshold=0,above_threshold_color=TEAL)
 for line in a.get_lines():line.set_linewidth(2.2)
 a.set(xlabel='Observaciones',ylabel='Altura de fusión');save(f,'h_'+meth)
# 4 linkages 2x2
f,axs=plt.subplots(2,2,figsize=(9.0,5.4),dpi=160)
for a,meth in zip(axs.ravel(),['single','complete','average','ward']):
 a.set_facecolor(BG);L=linkage(Xsmall,method=meth);dendrogram(L,no_labels=True,color_threshold=0,above_threshold_color=TEAL,ax=a);a.set_title(meth.upper(),color=WHITE,fontsize=11);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False);a.set_ylabel('Altura',color=SUB)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'h_compare')
# cut
f,a=fig('Cortar horizontalmente el dendrograma produce una partición')
L=linkage(Xsmall,method='ward');dendrogram(L,labels=labels,color_threshold=4.3,above_threshold_color=SUB,ax=a)
a.axhline(4.3,color=AMBER,lw=2,ls='--',label='Umbral h = 4,3');a.legend(frameon=False,labelcolor=WHITE);a.set(xlabel='Observaciones',ylabel='Distancia de fusión');save(f,'h_cut')
# chaining
chain=np.column_stack([np.arange(10),np.zeros(10)]) + rng.normal(0,.08,(10,2));f,axs=plt.subplots(1,2,figsize=(9,5.0),dpi=160)
for a,m in zip(axs,['single','complete']):
 l=linkage(chain,method=m);a.set_facecolor(BG);dendrogram(l,ax=a,no_labels=True,above_threshold_color=TEAL,color_threshold=0);a.set_title(m.upper(),color=WHITE);a.set_ylabel('Altura de fusión',color=SUB);a.tick_params(colors=SUB);a.spines[['top','right']].set_visible(False)
f.patch.set_facecolor(BG);f.tight_layout();save(f,'h_chaining')
# profile heatmap
f,a=fig('Mapa de calor de segmentos · datos sintéticos estandarizados')
im=a.imshow(profiles,cmap='coolwarm',vmin=-1.6,vmax=1.6,aspect='auto');a.set_xticks(np.arange(4),cols);a.set_yticks(np.arange(3),['S1 · proteger','S2 · fidelizar','S3 · activar']);
for i in range(3):
 for j in range(4):a.text(j,i,f'{profiles[i,j]:+.1f}',color=WHITE if abs(profiles[i,j])>.8 else '#17243b',ha='center',va='center',weight='bold')
f.colorbar(im,ax=a,shrink=.7).ax.tick_params(colors=SUB);save(f,'h_profiles')
# scatter for 3 clusters agglomerative
from sklearn.cluster import AgglomerativeClustering
for meth in ['single','complete','average','ward']:
 alg=AgglomerativeClustering(n_clusters=3,linkage=meth).fit(Xb)
 f,a=fig('K=3 usando '+meth+' linkage')
 for j in range(3):scat(a,Xb[alg.labels_==j],colors=COLORS[j],s=16)
 a.set(xlabel='Frecuencia (Z)',ylabel='Margen (Z)');save(f,'h_scatter_'+meth)
print('CHARTS',len(os.listdir(DIR)))