"""Publica las presentaciones y las 16 simulaciones del Módulo 09.

Conserva las páginas de glosario y cuestionario hasta su próxima entrega.
Los nuevos recursos se incorporan desde la fuente canónica, sin borrar archivos.
"""
from pathlib import Path
import shutil

SOURCE = Path('modules/09-arboles-ensembles/site')
TARGET = Path('docs/modulos/09-arboles-ensembles')
REQUIRED = ('index.html', 'styles.css', 'presentaciones.js',
            'presentacion-01.html', 'presentacion-02.html', 'presentacion-03.html',
            'simulacion.html')


def main():
    missing = [name for name in REQUIRED if not (SOURCE / name).is_file()]
    if missing:
        raise SystemExit('Módulo 09: faltan recursos: ' + ', '.join(missing))
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED:
        shutil.copyfile(SOURCE / name, TARGET / name)
    shutil.copytree(SOURCE / 'presentaciones', TARGET / 'presentaciones', dirs_exist_ok=True)
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
    print('Módulo 09: portal, tres presentaciones y 16 simulaciones publicados.')


if __name__ == '__main__':
    main()
