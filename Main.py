from Problema import *
from LAO import *
import time

probabilidades_transicion = {}

probabilidades_transicion['N'] = {'N': 0.8, 'NE': 0.1, 'NO': 0.1}
probabilidades_transicion['S'] = {'S': 0.8, 'SE': 0.1, 'SO': 0.1}
probabilidades_transicion['E'] = {'E': 0.8, 'NE': 0.1, 'SE': 0.1}
probabilidades_transicion['O'] = {'O': 0.8, 'NO': 0.1, 'SO': 0.1}
probabilidades_transicion['NE'] = {'NE': 0.8, 'N': 0.1, 'E': 0.1}
probabilidades_transicion['NO'] = {'NO': 0.8, 'N': 0.1, 'O': 0.1}
probabilidades_transicion['SE'] = {'SE': 0.8, 'S': 0.1, 'E': 0.1}
probabilidades_transicion['SO'] = {'SO': 0.8, 'S': 0.1, 'O': 0.1}
 
numFilas = 20
numCol = 20
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

estado_por_id, hg, s0, h, pi = p.generar_problema()

t_i = time.time()

VI_algorithm = VI(pi, h, estado_por_id)
VI_algorithm.run(hg)

t_f = time.time()

print("RESULTADO: ")
p.print_tablero(pi)

print("Tiempo usado: " + str(t_f - t_i))