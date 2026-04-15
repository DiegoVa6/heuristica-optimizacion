import heapq

class Abierta:
    def __init__(self):
        self.heap = []
        self.contador = 0  # para desempate

    def insertar(self, f, g, nodo):
        heapq.heappush(self.heap, (f, self.contador, g, nodo))
        self.contador += 1

    def extraer(self):
        return heapq.heappop(self.heap)

    def vacia(self):
        return len(self.heap) == 0

