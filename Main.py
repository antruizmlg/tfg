from Problem import *
from LAO import *
from RLAO import *
from BLAO import *
from ILAO import *
import time

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
percent_sinks = 10
rows = 10
columns = 10
sinks = rows*columns*(percent_sinks/100)
algorithm = 'ILAO'
system = 1

if system == 1:
    probs = probs_1
elif system == 2:
    probs = probs_2
elif system == 3:
    probs = probs_3

def solve_problem(problem, algorithm, heuristic = None):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial
    p, h = problem.get_initial_policy_and_heuristic(heuristic)
    t_i = time.time() # Iniciamos contador
    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO':
        lao_algorithm = LAO(hg, s0, h, p, problem.table, 'VI')
        lao_algorithm.LAO()
    elif algorithm == 'RLAO':
        rlao_algorithm = RLAO(hg, fs, h, p, problem.table)
        rlao_algorithm.RLAO()
    elif algorithm == 'ILAO':
        ilao_algorithm = ILAO(hg, s0, h, p, problem.table)
        it, size = ilao_algorithm.ILAO()        
    elif algorithm == 'BLAO':
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem.table)
        blao_algorithm.BLAO()
    elif algorithm == 'VI':
        vi_algorithm = Value_Iteration(hg, p, h)
        it = vi_algorithm.run(hg.states.keys())
    # Finalizamos contador
    t_f = time.time()
    return t_f - t_i, it, size


while rows <= 100:
    print("Generando stats para tablero "+str(rows)+"x"+str(columns)+"...")
    times = []
    list_it = []
    list_size = []
    for i in range(0, 100):
        p_1 = Problem(rows, columns, sinks, probs) # Creamos la instancia del problema, con el número de filas, columnas, sumideros 
                                                                    # y el sistema transitorio
        t, it, size = solve_problem(p_1, algorithm, 'MD') # Ejecutamos el algoritmo sobre elegido sobre el problema instanciado
                                                                # y el sistema transitorio
        times.append(t)
        list_it.append(it)
        list_size.append(size)

    name = algorithm + "_" + str(rows * columns) + "_" + str(percent_sinks) + "_" + str(system) + ".txt"
    f = open(name, "w")
    f.write("Times required: ")
    f.write(str(times))
    f.write("\nIterations required:" )
    f.write(str(list_it))
    f.write("\nMean time: ")
    f.write(str(sum(times)/len(times)))
    f.write("\nMean iterations: ")
    f.write(str(sum(list_it)/len(list_it)))
    f.write("\nMean size graph: ")
    f.write(str(sum(list_size)/len(list_size)))
    f.close()
    rows = rows + 10
    columns = columns + 10