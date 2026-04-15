# Práctica 01 — Programación lineal

Proyecto académico de la asignatura **Heurística y Optimización** (Universidad Carlos III de Madrid), centrado en la **modelización y resolución de problemas de asignación y optimización de recursos** mediante **LibreOffice Calc** y **GLPK**.

## Descripción

Esta práctica reúne tres enfoques de optimización sobre un contexto de planificación de autobuses y talleres:

1. **Modelo básico en Calc**  
   Problema clásico de asignación entre autobuses y talleres, minimizando la distancia total recorrida.

2. **Modelo avanzado en GLPK: minimización del impacto de averías**  
   Asignación de autobuses a franjas horarias en un taller, equilibrando:
   - coste de desplazamiento
   - penalización por no atender un autobús

3. **Modelo avanzado en GLPK: minimización de coincidencias entre autobuses**  
   Asignación de autobuses a talleres y franjas horarias minimizando el impacto sobre pasajeros compartidos cuando varios autobuses coinciden en la misma franja.

## Estructura

```text
practica_01_programacion_lineal/
├── README.md
├── report/
│   └── practica_01_memoria.pdf
├── calc/
│   └── parte-1.ods
└── glpk/
    ├── gen-1.py
    ├── gen-2.py
    ├── parte-2-1.mod
    ├── parte-2-2.mod
    └── examples/
        └── caso2.2.in
````

## Contenido

### 1. Modelo básico en Calc

En `calc/parte-1.ods` se plantea un problema de asignación binaria entre **5 autobuses** y **5 talleres**, donde cada autobús debe asignarse a exactamente un taller y cada taller solo puede recibir un autobús.

La función objetivo minimiza la distancia total recorrida:

* variables binarias `x_ij`
* restricción de asignación única por autobús
* restricción de capacidad única por taller

Este modelo se resolvió inicialmente en hoja de cálculo usando un solver lineal.

### 2. Modelo GLPK — Minimización del impacto de averías

En `glpk/parte-2-1.mod` y `glpk/gen-1.py` se implementa un modelo de programación lineal entera binaria para decidir qué autobuses son atendidos en un conjunto de franjas horarias disponibles.

El objetivo combina:

* coste por kilómetro recorrido
* penalización por pasajero cuando un autobús no es atendido

#### Archivos

* `parte-2-1.mod`: formulación general en MathProg / GLPK
* `gen-1.py`: genera el fichero `.dat`, ejecuta `glpsol` y muestra la solución

#### Ejecución

Desde la carpeta `glpk/`:

```bash
python3 gen-1.py entrada.in salida.dat
```

### 3. Modelo GLPK — Minimización de coincidencias entre autobuses

En `glpk/parte-2-2.mod` y `glpk/gen-2.py` se implementa un modelo más avanzado donde:

* hay varios talleres
* cada taller tiene distintas franjas disponibles
* cada autobús debe asignarse exactamente a una franja de algún taller
* se minimiza la coincidencia de autobuses con pasajeros compartidos en la misma franja

Para ello se introducen:

* variables binarias de asignación `x`
* variables auxiliares `z` para linealizar la coincidencia entre pares de autobuses

#### Archivos

* `parte-2-2.mod`: formulación del modelo en GLPK
* `gen-2.py`: genera el `.dat`, lanza `glpsol` y reconstruye la solución
* `examples/caso2.2.in`: ejemplo de entrada

#### Ejecución

Desde la carpeta `glpk/`:

```bash
python3 gen-2.py examples/caso2.2.in caso2.dat
```

## Qué se trabaja en esta práctica

* programación lineal y entera binaria
* modelización de problemas de asignación
* formulación de funciones objetivo y restricciones
* resolución con herramientas de hoja de cálculo
* modelado en GLPK / MathProg
* automatización con Python para generación de datos y ejecución de solver

## Resultados

Según la memoria de la práctica:

* el modelo básico en Calc obtiene una asignación óptima con distancia mínima total
* el modelo de averías prioriza autobuses con mejor equilibrio entre distancia y pasajeros afectados
* el modelo de coincidencias distribuye los autobuses entre talleres y franjas minimizando conflictos entre pasajeros compartidos

En todos los casos se verifica el cumplimiento de las restricciones del modelo y la coherencia de las soluciones generadas.

## Requisitos

Para ejecutar la parte de GLPK necesitas:

* Python 3
* `glpsol` instalado y accesible desde terminal

## Documentación

La explicación completa de la formulación matemática, restricciones, decisiones de modelado y análisis de resultados está en:

```text
report/practica_01_memoria.pdf
```

## Notas

Este repositorio conserva tanto la parte más académica de modelización como la parte práctica de automatización con Python y GLPK, con el objetivo de dejar una referencia clara del trabajo realizado en la asignatura.
