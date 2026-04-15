class Cerrada:
    def __init__(self):
        self.mejor_g = {}  # nodo -> mejor g conocido

    def contiene_mejor(self, nodo, g):
        return nodo in self.mejor_g and self.mejor_g[nodo] <= g

    def actualizar(self, nodo, g):
        self.mejor_g[nodo] = g

