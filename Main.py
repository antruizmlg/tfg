from Problema import *
from LAO import *

probabilidades_transicion = [[0.8, 0.1, 0.1, 0], # MOVERSE ARRIBA
                             [0.1, 0.8, 0, 0.1], # MOVERSE A LA DERECHA
                             [0.1, 0, 0.8, 0.1], # MOVERSE A LA IZQUIERDA
                             [0, 0.1, 0.1, 0.8]] # MOVERSE DEBAJO

numFilas = 8
numCol = 8
numSumideros = 0

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
hipergrafo, estado_inicial, heuristico, politica_inicial = p.generar_Problema()

p.informacion()

lao_algorithm = LAO(hipergrafo, estado_inicial, heuristico, politica_inicial, 'VI')
politica, V = lao_algorithm.LAO()

print(politica.politica)