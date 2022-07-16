from Problema import *
from LAO import *

probabilidades_transicion = [[0.8, 0.1, 0.1, 0], # MOVERSE ARRIBA
                             [0.1, 0.8, 0, 0.1], # MOVERSE A LA DERECHA
                             [0.1, 0, 0.8, 0.1], # MOVERSE A LA IZQUIERDA
                             [0, 0.1, 0.1, 0.8]] # MOVERSE ABAJO

numFilas = 5
numCol = 5
numSumideros = 3

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
estado_por_id, hg, s0, h, pi = p.generar_problema()

p.print_info()

lao_algorithm = LAO(estado_por_id, hg, s0, h, pi, 'VI')
pf, V = lao_algorithm.LAO()

print("RESULTADO: ")
print("--------------------------------------------------------------------------------------- ")
for i in range(len(p.tablero)):
    for j in range(len(p.tablero[0])):
        if p.tablero[i][j].terminal:
            print('TT', end = ' ')
        elif p.tablero[i][j].sumidero:
            print('SS', end = ' ')
        else:
            if pf.get_politica(p.tablero[i][j].id) == 'ARRIBA':
                print('AR', end = ' ')
            if pf.get_politica(p.tablero[i][j].id) == 'DERECHA':
                print('DE', end = ' ')
            if pf.get_politica(p.tablero[i][j].id) == 'IZQUIERDA':
                print('IZ', end = ' ')
            if pf.get_politica(p.tablero[i][j].id) == 'ABAJO':
                print('AB', end = ' ')
    print("")