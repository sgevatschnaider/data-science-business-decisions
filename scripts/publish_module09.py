"""Publica el aula completa del Módulo 09 desde su fuente canónica."""
from pathlib import Path
import shutil

SOURCE = Path('modules/09-arboles-ensembles/site')
TARGET = Path('docs/modulos/09-arboles-ensembles')
REQUIRED = ('index.html', 'styles.css', 'presentaciones.js',
            'presentacion-01.html', 'presentacion-02.html', 'presentacion-03.html',
            'simulacion.html', 'guia.html', 'glosario.html', 'cuestionario.html',
            'estudio.js', 'estudio.css', 'glosario.js', 'cuestionario.js',
            'videos.html', 'videos.css', 'videos.js', 'videos-badge.svg')


def main():
    missing = [name for name in REQUIRED if not (SOURCE / name).is_file()]
    if missing:
        raise SystemExit('Módulo 09: faltan recursos: ' + ', '.join(missing))
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED:
        shutil.copyfile(SOURCE / name, TARGET / name)
    shutil.copytree(SOURCE / 'presentaciones', TARGET / 'presentaciones', dirs_exist_ok=True)
    guide = SOURCE / 'guia/guia-simulaciones.pdf'
    if not guide.is_file():
        raise SystemExit('Módulo 09: falta la guía integral de simulaciones')
    shutil.copytree(SOURCE / 'guia', TARGET / 'guia', dirs_exist_ok=True)
    simulations = sorted((SOURCE / 'simuladores').glob('simulador_[0-9][0-9]_*.html'))
    if len(simulations) != 16:
        raise SystemExit(f'Módulo 09: se esperaban 16 simulaciones y hay {len(simulations)}')
    shutil.copytree(SOURCE / 'simuladores', TARGET / 'simuladores', dirs_exist_ok=True)
    # Accesos reproducibles también en la portada del repositorio.
    readme = Path('README.md')
    text = readme.read_text(encoding='utf-8')
    marker = '## Árboles, Random Forest y ensembles · aula de clase'
    if marker not in text:
        prefix = 'https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/'
        section = marker + '\n\nTres presentaciones completas con visores, autoplay, pantalla completa y descargas en PowerPoint y PDF.\n\n'
        section += f'[Portal M09]({prefix}index.html) · [PPT 01: Árboles y CART]({prefix}presentacion-01.html) · [PPT 02: Bagging y Random Forest]({prefix}presentacion-02.html) · [PPT 03: Boosting, interpretación y decisión]({prefix}presentacion-03.html)\n\n'
        text = text.replace('## Acceso directo', section + '## Acceso directo')
        readme.write_text(text, encoding='utf-8')
    module_readme = Path('modules/09-arboles-ensembles/README.md')
    text = module_readme.read_text(encoding='utf-8')
    if '## Presentaciones completas' not in text:
        prefix = 'https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/'
        text += '\n## Presentaciones completas\n\n'
        text += f'- [PPT 01: Árboles y CART, 41 diapositivas]({prefix}presentacion-01.html)\n'
        text += f'- [PPT 02: Bagging y Random Forest, 36 diapositivas]({prefix}presentacion-02.html)\n'
        text += f'- [PPT 03: Boosting, interpretación y decisión, 35 diapositivas]({prefix}presentacion-03.html)\n\n'
        text += 'Los visores permiten autoplay, pantalla completa y descargas. La fuente se conserva en `modules/09-arboles-ensembles/site/` y este paso la publica después del generador general.\n'
        module_readme.write_text(text, encoding='utf-8')
    # El build general regenera el README del módulo: reconstruir estos accesos.
    prefix = 'https://sgevatschnaider.github.io/data-science-business-decisions/modulos/09-arboles-ensembles/'
    marker = '## Laboratorio de 16 simulaciones'
    text = module_readme.read_text(encoding='utf-8')
    if marker not in text:
        section = '\n' + marker + '\n\n'
        section += f'[Abrir el catálogo completo]({prefix}simulacion.html)\n\n'
        section += '| Simulación | Acceso |\n|---|---|\n'
        import re
        for simulation in simulations:
            content = simulation.read_text(encoding='utf-8')
            title = re.search(r'<title>(.*?)</title>', content).group(1)
            section += f'| {title} | [Abrir]({prefix}simuladores/{simulation.name}) |\n'
        module_readme.write_text(text + section, encoding='utf-8')
    text = readme.read_text(encoding='utf-8')
    if '[16 simulaciones M09]' not in text:
        section = f'\n[16 simulaciones M09]({prefix}simulacion.html): árboles y CART (01–06), bagging y Random Forest (07–11), interpretación, boosting y decisión (12–16).\n\n'
        readme.write_text(text.replace('## Acceso directo', section + '## Acceso directo'), encoding='utf-8')
    marker = '## Guía, glosario y cuestionario completos'
    text = module_readme.read_text(encoding='utf-8')
    if marker not in text:
        section = '\n' + marker + '\n\n'
        section += f'- [Guía integral de las 16 simulaciones, 38 páginas]({prefix}guia.html): visor, descarga del PDF e índice que conecta cada capítulo con su laboratorio.\n'
        section += f'- [Glosario razonado, 109 conceptos]({prefix}glosario.html): búsqueda, filtros, tarjetas y seguimiento de conceptos aprendidos.\n'
        section += f'- [Cuestionario razonado, 60 preguntas]({prefix}cuestionario.html): respuestas-guía, dificultad, modo examen y seguimiento de repaso.\n\n'
        section += 'Ruta sugerida: presentación → guía y simulación → glosario → cuestionario. El progreso de estudio se conserva en el navegador utilizado.\n'
        module_readme.write_text(text + section, encoding='utf-8')
    text = readme.read_text(encoding='utf-8')
    if '[Guía M09: 38 páginas]' not in text:
        section = f'[Guía M09: 38 páginas]({prefix}guia.html) · [Glosario M09: 109 conceptos]({prefix}glosario.html) · [Cuestionario M09: 60 preguntas]({prefix}cuestionario.html)\n\n'
        readme.write_text(text.replace('## Acceso directo', section + '## Acceso directo'), encoding='utf-8')
    # Reconstruir el botón de videos cuando el generador regenera los README.
    legacy_badge = f'[![Videos M09](https://img.shields.io/badge/Videos-9%20complementarios-b91c1c?style=flat-square&logo=youtube&logoColor=white)]({prefix}videos.html)'
    badge = f'[![Videos M09](modules/09-arboles-ensembles/site/videos-badge.svg)]({prefix}videos.html)'
    module_badge = f'[![Videos M09](site/videos-badge.svg)]({prefix}videos.html)'
    text = readme.read_text(encoding='utf-8')
    text = text.replace(legacy_badge, badge)
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('| 09 |') and f'{prefix}videos.html' not in line:
            lines[i] = line.rstrip().removesuffix('|').rstrip() + ' ' + badge + ' |\n'
    readme.write_text(''.join(lines), encoding='utf-8')
    text = module_readme.read_text(encoding='utf-8')
    text = text.replace(legacy_badge, module_badge)
    marker = '## Videos complementarios'
    if marker not in text:
        section = '\n' + marker + '\n\n' + module_badge + '\n\n'
        section += 'Nueve videos con análisis de pertinencia, fragmentos sugeridos y enlaces a los simuladores. Cuatro centrales (árboles, poda, Random Forest y Gradient Boosting); tres puentes (sesgo–varianza, AdaBoost y regresión); XGBoost como ampliación e introducción opcional en español.\n\n'
        section += 'Los horarios son sugerencias docentes, no capítulos oficiales verificados. Los enlaces directos comienzan en el tiempo indicado; pausa al final del tramo. El visor solicita inicio y fin y mantiene un acceso alternativo a YouTube.\n'
        module_readme.write_text(text + section, encoding='utf-8')
    else:
        module_readme.write_text(text, encoding='utf-8')
    print('Módulo 09: aula completa publicada; 3 presentaciones, 16 simulaciones, guía de 38 páginas, 109 conceptos, 60 preguntas y 9 videos complementarios.')


if __name__ == '__main__':
    main()
