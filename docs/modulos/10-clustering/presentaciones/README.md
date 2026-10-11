# Presentaciones M10 · PCA, K-Means y clustering jerárquico

Material docente de Sergio Gevatschnaider para **Ciencia de Datos para Decisiones de Negocio**.

## Contenido verificado

| Material | PowerPoint editable | PDF para consulta | Diapositivas |
|---|---|---|---:|
| PCA | [PPTX](M10_01_PCA_Clase_Completa.pptx) | [PDF](M10_01_PCA_Clase_Completa.pdf) | 29 |
| K-Means | [PPTX](M10_02_KMeans_Clase_Completa.pptx) | [PDF](M10_02_KMeans_Clase_Completa.pdf) | 31 |
| Clustering jerárquico | [PPTX](M10_03_Jerarquico_Clase_Completa.pptx) | [PDF](M10_03_Jerarquico_Clase_Completa.pdf) | 31 |

**91 diapositivas en total.** [Descargar el ZIP de los seis documentos](M10_PCA_KMeans_Clustering_Presentaciones.zip).

## Abrir los visores

- [PCA](../presentacion-01.html) · lectura, miniaturas, autoplay y pantalla completa.
- [K-Means](../presentacion-02.html) · algoritmo, inicializaciones, validación y decisión.
- [Clustering jerárquico](../presentacion-03.html) · linkage, dendrogramas y segmentación multinivel.
- [Índice del módulo 10](../index.html) · contexto didáctico, recorrido y recursos existentes.

## Método de generación y verificaciones

Los fuentes completos están en [`fuentes/`](fuentes/) y permiten reconstruir el paquete en GitHub Actions. `make_charts.py` recrea los gráficos didácticos a partir de datos sintéticos; `build_decks.js` genera los tres PowerPoint con notas del presentador; LibreOffice los convierte a PDF. El workflow `.github/workflows/m10-presentaciones.yml` verifica las cantidades 29, 31 y 31 antes de incorporarlos al repositorio y crea el ZIP de descarga.

**Primera etapa:** presentaciones publicadas. **Etapas posteriores a solicitud:** 14 simulaciones S01–S14 sincronizadas con estas diapositivas; glosario y cuestionario ampliados. No se afirma que esos nuevos recursos estén completados.
