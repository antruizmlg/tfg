class Politica:
    def __init__(self, estados, politicas, costes):
        self.estados = estados
        self.politicas = politicas

    def indiceEstado(self, estado):
        i = 0 # Iniciamos el índice a 0
        found = False # Variable que indica si ha encontrado el estado
        while not found and i < len(self.estados): # Mientras no se haya encontrado y siga habiendo estados en el array.
            if self.estados[i] == estado: # Si el estado en la posición i coincide con el estado que estamos buscando
                found = True # found se pone a True.
            else:
                i += 1 # incremento del índice
        if not found:
            i = -1 # Si no se encuentra el estado, devolvemos -1
        return i

    def setPolitica(self, estado, nuevaPolitica):
        indice = self.indiceEstado(estado)
        self.politicas[indice] = nuevaPolitica

    def getPolitica(self, estado):
        indice = self.indiceEstado(estado)
        return self.politicas[indice]  