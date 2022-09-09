import math

class State:
    def __init__(self, id, x = None, y = None, w = None, z = None):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.z = z
        self.final = False
        self.sink = False

    """ heurístico distancia Manhattan"""
    def h_MD(self, x, x_, y, y_, w, w_, z, z_):
        return math.sqrt(abs(x - x_)**2 + abs(y - y_)**2 + abs(w - w_)**2 + abs(z - z_)**2)

    def __hash__(self):
        return hash(self.id)