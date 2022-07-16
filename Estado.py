class Estado:
    def __init__(self, id):
        self.id = id
        self.terminal = False
        self.sumidero = False

    def setTerminal(self):
        self.terminal = True

    def setSumidero(self):
        self.sumidero = True

    def h(self):
            return 0

    def __hash__(self):
        return hash(self.id)