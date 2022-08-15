class Estado:
    def __init__(self, id, fila, columna):
        self.id = id
        self.fila = fila
        self.col = columna
        self.terminal = False
        self.sumidero = False

    """ heurístico distancia Manhattan"""
    def h_MD(self, fil, col, fil_obj, col_obj):
        return abs(fil_obj - fil) + abs(col - col_obj)

    def __hash__(self):
        return hash(self.id)