from Problema import *
from LAO import *

import matplotlib
import matplotlib.pyplot as plt

"""Tres posibles sistemas de transiciones"""
probs_1 = {}
probs_2 = {}
probs_3 = {}

"""Sistema 1"""
probs_1['N'] = {'N': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['S'] = {'S': 0.8, 'E': 0.1, 'O': 0.1}
probs_1['E'] = {'E': 0.8, 'N': 0.1, 'S': 0.1}
probs_1['O'] = {'O': 0.8, 'N': 0.1, 'S': 0.1}

"""Sistema 2"""
probs_2['N'] = {'N': 0.8, 'E': 0.2}
probs_2['S'] = {'S': 0.8, 'O': 0.2}
probs_2['E'] = {'E': 0.8, 'S': 0.2}
probs_2['O'] = {'O': 0.8, 'N': 0.2}

"""Sistema 3"""
probs_3['N'] = {'N': 0.8, '-': 0.2}
probs_3['S'] = {'S': 0.8, '-': 0.2}
probs_3['E'] = {'E': 0.8, '-': 0.2}
probs_3['O'] = {'O': 0.8, '-': 0.2}

"""Número de filas, número de columnas y de sumideros""" 
numFilas = 5
numCol = 5
numSumideros = 0

def mean(list):
    return sum(list)/len(list)

def resize(it, Z_size):
    for i in range(len(it) - len(Z_size)):
        Z_size.append(None)
    return Z_size

def generate_plot(X, Y_1, Y_2, Y_3, x_label, y_label):
    fig, ax = plt.subplots()
    ax.plot(X, Y_1, label = 'Sistema 1')
    ax.plot(X, Y_2, label = 'Sistema 2')
    ax.plot(X, Y_3, label = 'Sistema 3')
    ax.legend(loc = 'upper left')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()

def run_algorithm(p, algorithm):
    dict_state, hg, s0, h, pi = p.generar_problema() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p.print_info() # Imprimimos información del problema

    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO*':
        lao_algorithm = LAO(dict_state, hg, s0, h, pi, 'VI')
        Z_sizes, Z_percent = lao_algorithm.LAO() # Obtenemos lista con los tamaños de los tres grafos en cada iteración
    elif algorithm == 'VI':
        vi_algorithm = VI(pi, h, dict_state)
        vi_algorithm.run(hg)
    elif algorithm == 'PI':
        pi_algorithm = PI(pi, h, dict_state)
        pi_algorithm.run(hg)

    return Z_sizes, Z_percent

p_1 = Problema(numFilas, numCol, numSumideros, probs_1) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                        # y el sistema transitorio
p_2 = Problema(numFilas, numCol, numSumideros, probs_2) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                        # y el sistema transitorio                                                
p_3 = Problema(numFilas, numCol, numSumideros, probs_3) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                        # y el sistema transitorio

Z_sizes_1, Z_percent_1 = run_algorithm(p_1, 'LAO*')
Z_sizes_2, Z_percent_2 = run_algorithm(p_2, 'LAO*')
Z_sizes_3, Z_percent_3 = run_algorithm(p_3, 'LAO*')

it = []
for i in range(numFilas*numCol):
    it.append(i + 1)

Z_percent_1 = resize(it, Z_percent_1)
Z_percent_2 = resize(it, Z_percent_2)
Z_percent_3 = resize(it, Z_percent_3)

generate_plot(it, Z_percent_1, Z_percent_2, Z_percent_3, 'Iteración', 'Porcentaje tamaño Z')