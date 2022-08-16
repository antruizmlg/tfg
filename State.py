class State:
    def __init__(self, id, row, column):
        self.id = id
        self.row = row
        self.col = column
        self.final = False
        self.sink = False

    """ heurístico distancia Manhattan"""
    def h_MD(self, row, col, final_row, final_column):
        return abs(final_row - row) + abs(col - final_column)

    def __hash__(self):
        return hash(self.id)