from Problema import *
from LAO import *
import time

probabilidades_transicion = [[0.8, 0.1, 0.1, 0], # MOVERSE ARRIBA
                             [0.1, 0.8, 0, 0.1], # MOVERSE A LA DERECHA
                             [0.1, 0, 0.8, 0.1], # MOVERSE A LA IZQUIERDA
                             [0, 0.1, 0.1, 0.8]] # MOVERSE ABAJO

numFilas = 10
numCol = 10
numSumideros = 0

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
estado_por_id, hg, s0, h, pi = p.generar_problema()

p.print_info()

t_i = time.time()

lao_algorithm = LAO(estado_por_id, hg, s0, h, pi, p, 'VI')
pf, V = lao_algorithm.LAO()

t_f = time.time()

print("RESULTADO: ")
p.print_tablero(pi)

print("Tiempo usado: " + str(t_f - t_i))