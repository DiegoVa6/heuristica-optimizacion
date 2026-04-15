import math
from abierta import Abierta
from cerrada import Cerrada

class AlgoritmoBusqueda:
    def __init__(self, grafo):
        self.grafo = grafo

    def heuristica(self, u, objetivo):
        lat1, lon1 = self.grafo.coordenadas(u)
        lat2, lon2 = self.grafo.coordenadas(objetivo)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + \
            math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

        c = 2 * math.asin(math.sqrt(a))
        return 6371000 * c  # metros

    def reconstruir_camino(self, padres, objetivo):
        camino = []
        actual = objetivo
        while actual in padres:
            padre, coste = padres[actual]
            camino.append((padre, actual, coste))
            actual = padre
        camino.reverse()
        return camino

    def a_estrella(self, inicio, objetivo, usar_heuristica=True):
        abierta = Abierta()
        cerrada = Cerrada()
        padres = {}

        h0 = 0 if not usar_heuristica else self.heuristica(inicio, objetivo)
        abierta.insertar(h0, 0, inicio)
        cerrada.actualizar(inicio, 0)

        expansiones = 0

        while not abierta.vacia():
            f, _, g, u = abierta.extraer()

            if g > cerrada.mejor_g.get(u, float("inf")):
                continue

            expansiones += 1

            if u == objetivo:
                return self.reconstruir_camino(padres, objetivo), g, expansiones

            for v, coste in self.grafo.vecinos(u):
                nuevo_g = g + coste

                if cerrada.contiene_mejor(v, nuevo_g):
                    continue

                cerrada.actualizar(v, nuevo_g)
                h = 0 if not usar_heuristica else self.heuristica(v, objetivo)
                abierta.insertar(nuevo_g + h, nuevo_g, v)
                padres[v] = (u, coste)

        return None, float("inf"), expansiones

