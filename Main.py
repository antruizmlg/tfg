from Problema import *
from LAO import *

probabilidades_transicion = [[0.8, 0.1, 0.1, 0], # MOVERSE ARRIBA
                             [0.1, 0.8, 0, 0.1], # MOVERSE A LA DERECHA
                             [0.1, 0, 0.8, 0.1], # MOVERSE A LA IZQUIERDA
                             [0, 0.1, 0.1, 0.8]] # MOVERSE DEBAJO

numFilas = 3
numCol = 3
numSumideros = 0

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
estado_por_id, hipergrafo, estado_inicial, heuristico, politica_inicial = p.generar_problema()

p.print_info()

lao_algorithm = LAO(estado_por_id, hipergrafo, estado_inicial, heuristico, politica_inicial, 'PI')
politica, V = lao_algorithm.LAO()

print(politica.politica)