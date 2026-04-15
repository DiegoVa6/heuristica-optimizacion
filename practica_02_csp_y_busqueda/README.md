# Práctica 02 — CSP y búsqueda

Proyecto académico de la asignatura **Heurística y Optimización** (Universidad Carlos III de Madrid), centrado en dos enfoques clásicos de inteligencia artificial y optimización:

1. **Satisfacción de restricciones (CSP)** para resolver el puzzle Binario / Takuzu  
2. **Búsqueda en grafos** para resolver problemas de camino mínimo usando **A\*** y **Dijkstra**

## Descripción

Esta práctica se divide en dos partes claramente diferenciadas.

### Parte 1 — Satisfacción de restricciones

Se modela y resuelve el puzzle **Binario (Takuzu)** como un problema de satisfacción de restricciones.

Cada casilla del tablero se representa como una variable con dominio binario, y el objetivo es completar la cuadrícula respetando las reglas del juego:

- cada fila y columna debe contener exactamente la mitad de `X` y la mitad de `O`
- no pueden aparecer tres símbolos iguales consecutivos
- las celdas prefijadas deben respetarse

La resolución se implementa mediante **backtracking manual con poda incremental**, sin dependencias externas.

### Parte 2 — Búsqueda en grafos

Se formula el problema del **camino más corto** sobre mapas reales de carreteras como un problema de búsqueda sobre un grafo dirigido y ponderado.

Se implementan dos variantes:

- **A\***, usando una heurística geográfica basada en la distancia de Haversine
- **Dijkstra**, como caso particular de A\* con heurística nula

La práctica permite comparar ambos algoritmos en términos de:

- coste óptimo
- número de expansiones
- tiempo de ejecución

## Estructura

```text
practica_02_csp_y_busqueda/
├── README.md
├── report/
│   └── practica_02_memoria.pdf
├── csp/
│   ├── parte-1.py
│   ├── examples/
│   │   └── ejemplo.in
│   └── outputs/
│       └── ejemplo.out
└── busqueda/
    ├── abierta.py
    ├── cerrada.py
    ├── algoritmo.py
    ├── grafo.py
    ├── parte-2.py
    └── outputs/
        ├── solucion.txt
        └── solucion_dijkstra.txt
````

## Parte 1 — CSP: resolución del Binairo

### Idea del modelo

El tablero se representa internamente como una matriz con valores:

* `-1` para casillas vacías
* `0` para `O`
* `1` para `X`

La resolución usa backtracking con comprobaciones incrementales de restricciones para podar ramas del árbol de búsqueda tan pronto como una asignación parcial deja de ser válida.

### Restricciones principales

* balance exacto por fila y columna
* prohibición de triples consecutivos
* respeto de las celdas prefijadas

### Archivo principal

* `parte-1.py`

### Ejecución

```bash
python3 parte-1.py ejemplo.in salida.out
```

### Entrada de ejemplo

```text
.X.O
X...
...X
O.X.
```

### Salida

El programa:

* muestra la instancia formateada por pantalla
* cuenta el número de soluciones
* escribe en el fichero de salida la instancia y una solución válida si existe

## Parte 2 — Búsqueda: A* y Dijkstra

### Idea del problema

El mapa se representa como un **grafo dirigido y ponderado**:

* los vértices representan intersecciones o puntos del mapa
* los arcos representan conexiones con coste positivo
* cada vértice tiene coordenadas geográficas

### Componentes

* `grafo.py`
  Carga coordenadas y arcos desde los ficheros del mapa y construye la lista de adyacencia.

* `abierta.py`
  Implementa la lista ABIERTA con una cola de prioridad.

* `cerrada.py`
  Mantiene el mejor coste conocido para cada vértice.

* `algoritmo.py`
  Implementa A* y Dijkstra compartiendo la misma lógica base.

* `parte-2.py`
  Script principal para ejecutar la búsqueda y escribir la solución.

### Heurística

Para A* se usa la **distancia geodésica** entre el nodo actual y el objetivo calculada con la fórmula de **Haversine**.

Esta heurística se emplea como cota inferior del coste restante y permite guiar la búsqueda hacia el destino.

### Ejecución

```bash
python3 parte-2.py <origen> <destino> <mapa> <salida>
```

Ejemplo:

```bash
python3 parte-2.py 1 10 USA-road-d.NY solucion.txt
```

### A* y Dijkstra

La implementación está diseñada para reutilizar el mismo algoritmo base.

* Con heurística activa → **A***
* Con heurística desactivada → **Dijkstra**

## Qué se trabaja en esta práctica

* modelización de problemas como CSP
* backtracking y poda incremental
* detección de instancias infactibles
* búsqueda informada
* búsqueda de coste uniforme
* heurísticas admisibles
* representación de grafos
* colas de prioridad
* reconstrucción de caminos óptimos

## Resultados

Según la memoria de la práctica:

* en la parte CSP, el programa detecta correctamente instancias válidas e infactibles y encuentra todas las soluciones, guardando la primera
* en la parte de búsqueda, tanto A* como Dijkstra obtienen el mismo camino óptimo, pero A* reduce el número de expansiones gracias a la heurística
* en mapas grandes, ambos algoritmos siguen siendo correctos, aunque el beneficio de la heurística depende del tamaño efectivo del trayecto y de la estructura del mapa

## Requisitos

* Python 3
* ficheros de entrada del puzzle Binario para la parte 1
* ficheros `.co` y `.gr` del mapa para la parte 2

## Documentación

La explicación completa del modelado, la implementación y el análisis de resultados está en:

```text
report/practica_02_memoria.pdf
```

## Notas

Esta práctica reúne dos formas distintas de abordar problemas complejos:

* mediante **restricciones**, en el caso del Binairo
* mediante **búsqueda heurística**, en el caso del camino mínimo

El conjunto sirve como una referencia clara de modelización, algoritmos clásicos y estructuras de apoyo implementadas en Python.
