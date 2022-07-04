class PI:
    def __init__(self, hipergrafo, politica, V):
        self.hipergrafo = hipergrafo
        self.politica = politica
        self.V = V

    def policy_evaluation(self):
        while True:
            oldV = self.V

            for i in range(len(self.hipergrafo.estados)):
                estado = self.hipergrafo.estados[i]
                politica = self.politica.getPolitica(estado)
                