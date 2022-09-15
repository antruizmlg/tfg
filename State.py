class State:
    def __init__(self, id, row = None, column = None):
        self.id = id
        self.row = row
        self.col = column
        self.final = False
        self.sink = False

    """ heurístico distancia Manhattan"""
    def h(self, row, final_row, col, final_col):
        return max(abs(final_row - row), abs(final_col - col))

    def __hash__(self):
        return hash(self.id)