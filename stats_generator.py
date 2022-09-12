from Problem import *
from LAO import *
from RLAO import *
from BLAO import *
from ILAO import *
import time
import sys

"""Tres posibles sistemas de transiciones"""
probs_1 = {}
probs_2 = {}
probs_3 = {}
probs_4 = {}

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
systems = {'1': probs_1, '2': probs_2, '3': probs_3}
percent_sinks = [0]
states = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

sys.setrecursionlimit(1000000)
def solve_problem(problem, algorithm):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic()
    problem.print_info() # Imprimimos información del problema

    iterations = None
    total_expanded = None
    Z_percent = None

    t_i = time.time() # Iniciamos contador
    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO*':
        lao_algorithm = LAO(hg, s0, h, p, problem)
        total_expanded, Z_percent = lao_algorithm.LAO()
    elif algorithm == 'RLAO*':
        rlao_algorithm = RLAO(hg, s0, fs, h, p, problem)
        total_expanded = rlao_algorithm.RLAO()
    elif algorithm == 'ILAO*':
        ilao_algorithm = ILAO(hg, s0, h, p, problem)
        total_expanded = ilao_algorithm.ILAO()        
    elif algorithm == 'BLAO*':
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem)
        total_expanded = blao_algorithm.BLAO()
    elif algorithm == 'VI':
        vi_algorithm = Value_Iteration(hg, p, h, gamma = 0.99)
        iterations = vi_algorithm.run(hg.states.keys())

    # Finalizamos contador
    t_f = time.time()
    return round(t_f - t_i, 3), iterations, total_expanded, Z_percent

for system in systems.keys():
    print("Generando para sistema "+str(system)+"...")
    for ps in percent_sinks:
        print("Generando para porcentaje de skins "+str(ps)+"...")  
        for st in states:
            print("Generando para numero de estados "+str(st*st)+"...")

            name = str(system) + "_" + str(ps) + "_" + str(st*st) + ".txt"
            f = open(name, 'a')

            for i in range(0, 10):
                print("Problema "+str(i+1))
                f.write("Problema "+str(i+1)+"\n")
                f.write("-------------------------------------------------------\n")

                p = Problem(st, st, st*st*(ps/100), systems[system])
                t1, it1, ex1, Z1 = solve_problem(p, 'LAO*')
                t2, it2, ex2, Z2 = solve_problem(p, 'ILAO*')
                t3, it3, ex3, Z3 = solve_problem(p, 'RLAO*')
                t4, it4, ex4, Z4 = solve_problem(p, 'BLAO*')
                t5, it5, ex5, Z5 = solve_problem(p, 'VI')

                f.write('LAO*:\n')
                f.write('Tiempo requerido: '+str(t1)+'\n')
                f.write('Nodos expandidos: '+str(ex1)+'\n')
                f.write('Porcentajes del conjunto Z: '+str(Z1)+'\n\n')

                f.write('ILAO*:\n')
                f.write('Tiempo requerido: '+str(t2)+'\n')
                f.write('Nodos expandidos: '+str(ex2)+'\n\n')

                f.write('RLAO*:\n')
                f.write('Tiempo requerido: '+str(t3)+'\n')
                f.write('Nodos expandidos: '+str(ex3)+'\n\n')

                f.write('BLAO*:\n')
                f.write('Tiempo requerido: '+str(t4)+'\n')
                f.write('Nodos expandidos: '+str(ex4)+'\n\n')

                f.write('VI:\n')
                f.write('Tiempo requerido: '+str(t5)+'\n')
                f.write('Numero de iteraciones: '+str(it5)+'\n')
                f.write("-------------------------------------------------------\n")