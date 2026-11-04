"""Build the self-contained M11 study glossary from reviewed Spanish source.

Run directly, or through build_course.py. No remote assets or build dependencies.
"""
from pathlib import Path
from html import escape as E
import re
import unicodedata

SOURCE = Path(__file__).resolve().parents[1]
CONTENT = SOURCE / 'modules/11-redes-neuronales/glosario'
KEYS = ('title', 'aliases', 'definition', 'mechanism', 'formula', 'example', 'mistake', 'question', 'answer')

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def mathtext(value):
    """Readable subscripts/superscripts, escaped before adding controlled markup."""
    value = E(value)
    value = re.sub(r'_\(([^)]+)\)', r'<sub>\1</sub>', value)
    value = re.sub(r'_([A-Za-z0-9]+)', r'<sub>\1</sub>', value)
    value = re.sub(r'\^\(([^)]+)\)', r'<sup>\1</sup>', value)
    return re.sub(r'\^([0-9kT]+)', r'<sup>\1</sup>', value)

def load():
    groups = []
    for line in (CONTENT / 'contenido.txt').read_text().splitlines():
        if line.startswith('## '):
            key, number, title, subtitle, resource = line[3:].split('|')
            groups.append(dict(id=key, number=number, title=title, subtitle=subtitle, resource=resource, terms=[]))
        elif line.strip():
            fields = line.split('|')
            if len(fields) != len(KEYS):
                raise ValueError(f'Expected {len(KEYS)} fields: {line[:70]}')
            term = dict(zip(KEYS, fields))
            term['id'] = slug(term['title'])
            term['group'] = groups[-1]['id']
            groups[-1]['terms'].append(term)
    ids = [t['id'] for g in groups for t in g['terms']]
    assert len(ids) == len(set(ids)), 'Duplicate glossary anchors'
    return groups

SOURCES = {
 'fundamentos': [('Deep Learning · redes feedforward', 'https://www.deeplearningbook.org/contents/mlp.html')],
 'aprendizaje': [('Deep Learning · optimización', 'https://www.deeplearningbook.org/contents/optimization.html'), ('Deep Learning · regularización', 'https://www.deeplearningbook.org/contents/regularization.html')],
 'validacion': [('scikit-learn · evaluación y métricas', 'https://scikit-learn.org/stable/modules/model_evaluation.html'), ('scikit-learn · calibración', 'https://scikit-learn.org/stable/modules/calibration.html')],
 'secuencias': [('Forecasting: Principles and Practice · evaluación', 'https://otexts.com/fpp3/accuracy.html'), ('Forecasting: Principles and Practice · validación temporal', 'https://otexts.com/fpp3/tscv.html')],
 'rnn': [('Dive into Deep Learning · RNN', 'https://d2l.ai/chapter_recurrent-neural-networks/rnn.html'), ('Dive into Deep Learning · BPTT', 'https://d2l.ai/chapter_recurrent-neural-networks/bptt.html')],
 'lstm': [('Dive into Deep Learning · LSTM', 'https://d2l.ai/chapter_recurrent-modern/lstm.html'), ('PyTorch · LSTM y convenciones', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html'), ('Attention Is All You Need · artículo original', 'https://arxiv.org/abs/1706.03762')]
}

def build(root=SOURCE):
    groups = load()
    terms = [t for g in groups for t in g['terms']]
    html = (CONTENT / 'plantilla.html').read_text()
    filters = '<button type="button" data-filter="all" aria-pressed="true">Todo <span>102</span></button>'
    sidebar = ''
    sections = ''
    for group in groups:
        gid, number = group['id'], group['number']
        filters += f'<button type="button" data-filter="{gid}" aria-pressed="false">{E(group["title"].split(" · ")[0].replace("Fundamentos de redes neuronales", "Fundamentos").replace("Redes neuronales recurrentes", "RNN").replace("LSTM, GRU y conexiones modernas", "LSTM y GRU").replace("Datos secuenciales y pronóstico", "Secuencias").replace("Evaluación y decisiones", "Evaluación").replace("Cómo aprende una red", "Aprendizaje"))} <span>{len(group["terms"])}</span></button>'
        sidebar += f'<details class="index-group" open><summary><span>{number}</span> {E(group["title"].split(" · ")[0])}</summary><div>'
        for term in group['terms']:
            sidebar += f'<a href="#{term["id"]}">{E(term["title"])}</a>'
        sidebar += '</div></details>'
        sections += f'<section class="unit" data-unit="{gid}" aria-labelledby="unit-{gid}"><div class="unit-head"><span class="unit-number">{number}</span><div><p class="eyebrow">Unidad de estudio · {len(group["terms"])} conceptos</p><h2 id="unit-{gid}">{E(group["title"])}</h2><p>{E(group["subtitle"])}</p></div></div>'
        for n, term in enumerate(group['terms']):
            related = group['terms'][max(0,n-1):n] + group['terms'][n+1:n+2]
            links = ''.join(f'<a href="#{t["id"]}">{E(t["title"])}</a>' for t in related)
            search = ' '.join(term[k] for k in KEYS if k != 'formula')
            sections += f'''<article id="{term['id']}" class="term glossary-entry" data-glossary-entry data-group="{gid}" data-search="{E(search,quote=True)}">
<div class="term-top"><div><p class="term-code">{number}.{n+1:02d} · {E(term['aliases'])}</p><h3><a class="permalink" href="#{term['id']}">{E(term['title'])}</a></h3></div><label class="learned"><input type="checkbox" data-learned="{term['id']}"><span>Estudiado</span></label></div>
<p class="definition">{mathtext(term['definition'])}</p><p class="mechanism">{mathtext(term['mechanism'])}</p>
<div class="formula"><span>Notación / relación clave</span><p>{mathtext(term['formula'])}</p></div>
<div class="two-notes"><div class="example"><h4>Ejemplo para entenderlo</h4><p>{mathtext(term['example'])}</p></div><div class="mistake"><h4>Error frecuente</h4><p>{mathtext(term['mistake'])}</p></div></div>
<details class="review"><summary>Comprobá tu comprensión <span>+</span></summary><p class="question">{mathtext(term['question'])}</p><details class="answer"><summary>Ver respuesta orientativa</summary><p>{mathtext(term['answer'])}</p></details></details>
<div class="related"><span>Conectá con</span>{links}</div></article>'''
        sections += '<div class="unit-sources"><strong>Continuar esta unidad</strong><a href="'+E(group['resource'])+'">Presentación o laboratorio del recorrido →</a><span>Referencias para profundizar</span>'
        sections += ''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{E(label)} ↗</a>' for label,url in SOURCES[gid])
        sections += '</div></section>'
    options = ''.join(f'<option value="{t["id"]}">{E(t["title"])}</option>' for t in sorted(terms,key=lambda t:slug(t['title'])))
    for old,new in {'@@FILTERS@@':filters, '@@INDEX@@':sidebar, '@@SECTIONS@@':sections, '@@OPTIONS@@':options, '@@COUNT@@':str(len(terms))}.items():
        html = html.replace(old,new)
    html = html.replace('@@CSS@@', (CONTENT/'estilos.css').read_text()).replace('@@JS@@',(CONTENT/'interacciones.js').read_text())
    assert '@@' not in html
    dest = Path(root)/'docs/modulos/11-redes-neuronales/glosario.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html.rstrip()+'\n')
    return len(terms)

if __name__ == '__main__':
    print(f'Glosario generado: {build()} conceptos desarrollados, 6 unidades, HTML autónomo.')
