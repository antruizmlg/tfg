class Estado:
    def __init__(self, id):
        self.id = id
        self.terminal = False
        self.sumidero = False

    def h_zero(self):
        return 0

    def h_MD(self, fil, col, fil_obj, col_obj):
        return abs(fil_obj - fil) + abs(col - col_obj)

    def __hash__(self):
        return hash(self.id)