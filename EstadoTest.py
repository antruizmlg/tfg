from Estado import *

class EstadoTest(Estado):
    def __init__(self, id):
        super().__init__(id)

    def esTerminal(self):
        return self.id == 's4'