"""Valida rutas, sincronía y referencias del módulo 11 sin tocar otros módulos."""
from pathlib import Path
import json,hashlib,re,zipfile,sys,unicodedata
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/modulos/11-redes-neuronales/experiencia'
errors=[];counts={}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:self.links.append(v)
for page in BASE.parent.rglob('*.html'):
 parser=Links();parser.feed(page.read_text())
 for raw in parser.links:
  q=urlparse(raw)
  if q.scheme or not q.path:continue
  target=(page.parent/unquote(q.path)).resolve()
  if q.path.endswith('/'):target=target/'index.html'
  if not target.exists():errors.append(f'Enlace roto: {page.relative_to(ROOT)}: {raw}')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
source=json.loads((ROOT/'scripts/module11/decks.json').read_text())
for d in source:
 folder=BASE/d['slug'];catalog=json.loads((folder/'catalog.json').read_text());assert catalog==d
 n=len(d['slides']);counts[d['slug']]=n
 assert len(list((folder/'slides/es').glob('*.webp')))==n
 with zipfile.ZipFile(folder/'downloads'/(d['slug']+'.pptx')) as z:
  slides=[p for p in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',p)]
  assert len(slides)==n
  assert len([p for p in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',p)])==n
  for s in d['slides']:
   raw=z.read(f'ppt/slides/slide{s["number"]}.xml');root=ET.fromstring(raw)
   text=''.join(root.itertext())
   # Native text survives export. No screenshot replaces a whole slide.
   assert s['title'] in text,(d['slug'],s['number'],'title')
   assert not root.findall('.//p:pic',ns),(d['slug'],s['number'],'raster slide')
 for s in d['slides']:
  for lab in s['labs']:assert(folder/lab).is_file()
  for vid in s['videos']:assert any(v['id']==vid for v in d['videos'])
  for k in ('notes','transcript','sources'):assert s[k]
 manifest=json.loads((BASE/'asset-manifest.json').read_text())
 for p in [folder/'downloads'/(d['slug']+'.pptx'),folder/'downloads'/(d['slug']+'.pdf'),*list((folder/'slides/es').glob('*.webp'))]:
  rec=manifest[str(p.relative_to(BASE))];assert rec['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),p
try:
 import fitz
 for d in source:
  with fitz.open(BASE/d['slug']/'downloads'/(d['slug']+'.pdf')) as doc:
   assert len(doc)==len(d['slides'])
   for page,s in zip(doc,d['slides']):
    norm=lambda x:unicodedata.normalize('NFKC',x).replace(' ','').replace('\n','')
    assert norm(s['title']) in norm(page.get_text()),(d['slug'],s['number'],'PDF title')
except ImportError:print('PyMuPDF no disponible: comprobación de texto PDF omitida')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(json.dumps({'passed':True,'slides':counts,'total_slides':sum(counts.values()),'local_links':'all existing','hashes':'all matched','notes':'all slides','catalogs':'equal to source'},ensure_ascii=False))
