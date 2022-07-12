class Politica:
    def __init__(self, politica):
        self.politica = politica

    def set_politica(self, estado, nuevaPolitica):
        self.politica[estado] = nuevaPolitica

    def get_politica(self, estado):
        return self.politica[estado] 