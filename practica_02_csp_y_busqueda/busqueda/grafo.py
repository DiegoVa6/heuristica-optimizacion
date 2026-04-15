import math

class Grafo:
    def __init__(self):
        self.adj = {}          # u -> [(v, coste), ...]
        self.coords = {}       # u -> (lat_rad, lon_rad)
        self.num_vertices = 0
        self.num_arcos = 0

    def cargar_coordenadas(self, fichero_co):
        with open(fichero_co, "r") as f:
            for linea in f:
                if not linea or linea[0] != 'v':
                    continue

                _, vid, lon, lat = linea.split()
                vid = int(vid)

                lat = float(lat) / 1e6
                lon = float(lon) / 1e6

                self.coords[vid] = (
                    math.radians(lat),
                    math.radians(lon)
                )

        self.num_vertices = len(self.coords)

    def cargar_arcos(self, fichero_gr):
        with open(fichero_gr, "r") as f:
            for linea in f:
                if not linea or linea[0] != 'a':
                    continue

                _, u, v, coste = linea.split()
                u = int(u)
                v = int(v)
                coste = int(coste)

                if u not in self.adj:
                    self.adj[u] = []

                self.adj[u].append((v, coste))
                self.num_arcos += 1

    @classmethod
    def cargar_desde_mapa(cls, nombre_base):
        g = cls()
        g.cargar_coordenadas(nombre_base + ".co")
        g.cargar_arcos(nombre_base + ".gr")
        return g

    def vecinos(self, u):
        return self.adj.get(u, [])

    def coordenadas(self, u):
        return self.coords[u]

