"""Exporta los PPTX finales con LibreOffice y deriva de esos PDF las imágenes web."""
from pathlib import Path
import json,subprocess,tempfile,hashlib,shutil
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'docs/modulos/11-redes-neuronales/experiencia'
decks=json.loads((Path(__file__).parent/'decks.json').read_text())
manifest={}
for deck in decks:
 folder=BASE/deck['slug'];ppt=folder/'downloads'/(deck['slug']+'.pptx')
 with tempfile.TemporaryDirectory(prefix='uca-nn-lo-') as temp:
  subprocess.run(['soffice','-env:UserInstallation='+Path(temp).as_uri(),'--headless','--convert-to','pdf','--outdir',temp,str(ppt)],check=True)
  shutil.copyfile(Path(temp)/(deck['slug']+'.pdf'),ppt.with_suffix('.pdf'))
 pdf=ppt.with_suffix('.pdf');doc=fitz.open(pdf)
 assert len(doc)==len(deck['slides']),(pdf,len(doc))
 for i,page in enumerate(doc):
  pix=page.get_pixmap(matrix=fitz.Matrix(1.25,1.25))
  image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  image.save(folder/'slides/es'/f'{i+1:02}.webp',quality=90)
 for p in [ppt,pdf,*sorted((folder/'slides/es').glob('*.webp'))]:
  manifest[str(p.relative_to(BASE))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
 print(deck['slug'],len(doc),'slides sincronizados')
(BASE/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
