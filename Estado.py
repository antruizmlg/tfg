class Estado:
    def __init__(self, id):
        self.id = id
        self.terminal = False
        self.sumidero = False

    def setTerminal(self):
        self.terminal = True

    def setSumidero(self):
        self.sumidero = True

    def esTerminal(self):
        return self.terminal

    def h(self):
        if self.sumidero:
            return 10
        else: 
            if not self.esTerminal():
                return 1
            else:
                return 0

    def __hash__(self):
        return hash(self.id)