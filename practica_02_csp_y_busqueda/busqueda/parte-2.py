import sys
import time
from grafo import Grafo
from algoritmo import AlgoritmoBusqueda

def main():

    # 1. Comprobación de argumentos
    if len(sys.argv) != 5:
        print("Uso: python3 parte-2.py <origen> <destino> <mapa> <salida>")
        sys.exit(1)

    inicio = int(sys.argv[1])
    objetivo = int(sys.argv[2])
    mapa = sys.argv[3]
    salida = sys.argv[4]

    grafo = Grafo.cargar_desde_mapa(mapa)

    # 3. Comprobar que los vértices existen
    if inicio not in grafo.coords or objetivo not in grafo.coords:
        print("Error: vértice inicial o destino no existe en el mapa")
        sys.exit(1)

    buscador = AlgoritmoBusqueda(grafo)

    t0 = time.time()
    camino, coste, expansiones = buscador.a_estrella(inicio, objetivo, True)
    t1 = time.time()

    print("# vertices:", grafo.num_vertices)
    print("# arcos:", grafo.num_arcos)
    print("Solución óptima encontrada con coste", coste)
    print("Tiempo de ejecución:", round(t1 - t0, 3), "segundos")
    print("# expansiones:", expansiones)

    with open(salida, "w") as f:
        f.write(str(inicio))
        for u, v, c in camino:
            f.write(f" - ({c}) - {v}")
        f.write("\n")

if __name__ == "__main__":
    main()

