class Politica:
    def __init__(self, politica):
        self.politica = politica

    def setPolitica(self, estado, nuevaPolitica):
        self.politica[estado] = nuevaPolitica

    def getPolitica(self, estado):
        return self.politica[estado] 