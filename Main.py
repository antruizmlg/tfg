from Problema import *
from LAO import *

probabilidades_transicion = [[0.8, 0.1, 0.1, 0], # MOVERSE ARRIBA
                             [0.1, 0.8, 0, 0.1], # MOVERSE A LA DERECHA
                             [0.1, 0, 0.8, 0.1], # MOVERSE A LA IZQUIERDA
                             [0, 0.1, 0.1, 0.8]] # MOVERSE DEBAJO

numFilas = 50
numCol = 50
numSumideros = 4

p = Problema(numFilas, numCol, numSumideros, probabilidades_transicion)
hipergrafo, estado_inicial, heuristico, politica_inicial = p.generar_Problema()

print("Tamaño de tablero: " + numFilas + "x" + numCol + "\n")
for sumidero in p.sumideros:
        print("Sumidero: "+ p)
print("Celda inicial: [" + p.filaInicial + ", " + p.columnaInicial)

lao_algorithm = LAO(hipergrafo, estado_inicial, heuristico, politica_inicial, 'VI')
politica, V = lao_algorithm.LAO()