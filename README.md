# Heurística y Optimización

Repositorio académico con prácticas de la asignatura **Heurística y Optimización** de la **Universidad Carlos III de Madrid**.

El objetivo de este repositorio es reunir, documentar y organizar distintas prácticas centradas en **modelización matemática, optimización, satisfacción de restricciones y búsqueda heurística**, mostrando tanto la formulación de los problemas como sus implementaciones en Python, GLPK y hoja de cálculo.

## Contenido

Actualmente el repositorio incluye dos bloques principales:

### Práctica 01 — Programación lineal

Trabajo centrado en problemas de **asignación y optimización de recursos** en el contexto de autobuses, talleres y franjas horarias.

Incluye:

- un modelo básico de asignación resuelto en **LibreOffice Calc**
- un modelo en **GLPK** para minimizar el impacto de averías
- un modelo en **GLPK** para minimizar coincidencias entre autobuses con pasajeros compartidos

### Práctica 02 — CSP y búsqueda

Trabajo dividido en dos enfoques:

- resolución del puzzle **Binario / Takuzu** mediante **satisfacción de restricciones (CSP)** y backtracking con poda
- resolución de problemas de **camino mínimo** sobre grafos reales mediante **A\*** y **Dijkstra**

## Estructura

```text
heuristica-optimizacion/
├── README.md
├── LICENSE
├── practica_01_programacion_lineal/
│   ├── README.md
│   ├── report/
│   ├── calc/
│   └── glpk/
└── practica_02_csp_y_busqueda/
    ├── README.md
    ├── report/
    ├── csp/
    └── busqueda/
````

## Prácticas

### `practica_01_programacion_lineal`

Esta práctica trabaja con **programación lineal** y **programación lineal entera binaria**.

Se estudian distintos modelos de asignación:

* asignación de autobuses a talleres minimizando distancia
* asignación de autobuses a franjas horarias minimizando coste operativo
* asignación de autobuses a talleres y franjas minimizando conflictos entre pasajeros compartidos

Tecnologías y herramientas utilizadas:

* LibreOffice Calc
* GLPK / MathProg
* Python para automatización de datos y ejecución del solver

### `practica_02_csp_y_busqueda`

Esta práctica combina dos paradigmas clásicos de resolución de problemas:

* **CSP** para modelar y resolver el puzzle Binario
* **búsqueda en grafos** para encontrar caminos óptimos en mapas reales

Temas principales:

* variables, dominios y restricciones
* backtracking con poda incremental
* detección de instancias infactibles
* grafos ponderados
* heurísticas admisibles
* A* y Dijkstra
* colas de prioridad y reconstrucción de caminos

## Objetivo del repositorio

Este repositorio no pretende presentar proyectos independientes y aislados, sino una colección organizada de prácticas que muestran distintas formas de abordar problemas complejos mediante:

* modelización matemática
* optimización
* búsqueda
* heurísticas
* diseño de algoritmos

## Documentación

Cada práctica incluye su propio `README.md` y una memoria en la carpeta `report/`, donde se documentan:

* el planteamiento del problema
* la formulación del modelo
* la implementación
* los casos de prueba
* el análisis de resultados

## Requisitos generales

Dependiendo de la práctica, puede ser necesario utilizar:

* Python 3
* GLPK / `glpsol`
* LibreOffice Calc o software compatible con hojas de cálculo
* ficheros de entrada específicos para los modelos o algoritmos

Consulta el `README.md` de cada práctica para ver los detalles de ejecución.

## Notas

Este repositorio refleja trabajo académico orientado a:

* entender técnicas de optimización
* comparar enfoques de resolución
* implementar modelos y algoritmos de forma estructurada
* documentar resultados de manera clara y reproducible

## License

This repository is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
