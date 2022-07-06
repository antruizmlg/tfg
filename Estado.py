class Estado:
    def __init__(self, id):
        self.id = id

    def esTerminal(self):
        pass

    def sucesores(self):
        pass

    def antecesores(self):
        pass

    def __hash__(self):
        return hash(self.id)