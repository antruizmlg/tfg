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

"""Sistema 1"""
probs_1['NN'] = {'NN': 0.8, 'NE': 0.1, 'NO': 0.1}
probs_1['SS'] = {'SS': 0.8, 'SE': 0.1, 'SO': 0.1}
probs_1['EE'] = {'EE': 0.8, 'NE': 0.1, 'SE': 0.1}
probs_1['OO'] = {'OO': 0.8, 'NO': 0.1, 'SO': 0.1}
probs_1['NE'] = {'NE': 0.8, 'EE': 0.1, 'NN': 0.1}
probs_1['NO'] = {'NO': 0.8, 'NN': 0.1, 'OO': 0.1}
probs_1['SE'] = {'SE': 0.8, 'SS': 0.1, 'EE': 0.1}
probs_1['SO'] = {'SO': 0.8, 'OO': 0.1, 'SS': 0.1}
probs_1['--'] = {'--': 1}

"""Sistema 2"""
probs_2['NN'] = {'NN': 0.9, 'NE': 0.1}
probs_2['SS'] = {'SS': 0.9, 'SO': 0.1}
probs_2['EE'] = {'EE': 0.9, 'SE': 0.1}
probs_2['OO'] = {'OO': 0.9, 'NO': 0.1}
probs_2['NE'] = {'NE': 0.9, 'EE': 0.1}
probs_2['NO'] = {'NO': 0.9, 'NN': 0.1}
probs_2['SE'] = {'SE': 0.9, 'SS': 0.1}
probs_2['SO'] = {'SO': 0.9, 'OO': 0.1}
probs_2['--'] = {'--': 1}

"""Sistema 3"""
probs_3['NN'] = {'NN': 0.9, '--': 0.1}
probs_3['SS'] = {'SS': 0.9, '--': 0.1}
probs_3['EE'] = {'EE': 0.9, '--': 0.1}
probs_3['OO'] = {'OO': 0.9, '--': 0.1}
probs_3['NE'] = {'NE': 0.9, '--': 0.1}
probs_3['SE'] = {'SE': 0.9, '--': 0.1}
probs_3['NO'] = {'NO': 0.9, '--': 0.1}
probs_3['SO'] = {'SO': 0.9, '--': 0.1}
probs_3['--'] = {'--': 1}

"""Número de filas, número de columnas y de sumideros""" 
systems = {'1': probs_1, '2': probs_2}
percent_sinks = [30, 50, 80]
states = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

sys.setrecursionlimit(10 ** 9)
def solve_problem(problem, algorithm):
    hg, s0, fs = problem.generate_problem() # Generamos el problema y obtenemos diccionario (estado id -> objeto estado), el hipergrafo
    # que representa el problema, el estado inicial, el heurístico y la política inicial

    p, h = problem.get_initial_policy_and_heuristic(algorithm)
    problem.print_info() # Imprimimos información del problema

    iterations = None
    total_expanded = None
    Z_percent = None

    t_i = time.time() # Iniciamos contador
    # Ejecutamos algoritmo seleccionado por parámetros
    if algorithm == 'LAO*':
        lao_algorithm = LAO(hg, s0, h, p, problem)
        total_expanded, iterations, Z_percent = lao_algorithm.LAO()
    elif algorithm == 'RLAO*':
        rlao_algorithm = RLAO(hg, s0, fs, h, p, problem)
        total_expanded, iterations = rlao_algorithm.RLAO()
    elif algorithm == 'ILAO*':
        ilao_algorithm = ILAO(hg, s0, h, p, problem)
        total_expanded, iterations = ilao_algorithm.ILAO()        
    elif algorithm == 'BLAO*':
        blao_algorithm = BLAO(hg, s0, fs, h, p, problem)
        total_expanded, iterations = blao_algorithm.BLAO()
    elif algorithm == 'VI':
        vi_algorithm = Value_Iteration(hg, p, h, gamma = 0.95)
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

            mt_lao = []
            mt_ilao = []
            mt_blao = []
            mt_rlao = []
            mt_vi = []

            me_lao = []
            me_ilao = []
            me_blao = []
            me_rlao = []

            mi_lao = []
            mi_ilao = []
            mi_blao = []
            mi_rlao = []
            mi_vi = []

            for i in range(0, 10):
                print("Problema "+str(i+1))
                f.write("Problema "+str(i+1)+"\n")
                f.write("-------------------------------------------------------\n")

                p = Problem(st, st, st*st*(ps/100), systems[system])
#                t3, it3, ex3, Z3 = solve_problem(p, 'RLAO*')
                t1, it1, ex1, Z1 = solve_problem(p, 'LAO*')
                t2, it2, ex2, Z2 = solve_problem(p, 'ILAO*')
                t4, it4, ex4, Z4 = solve_problem(p, 'BLAO*')
                t5, it5, ex5, Z5 = solve_problem(p, 'VI')

                f.write('LAO*:\n')
                f.write('Tiempo requerido: '+str(t1)+'\n')
                f.write('Iteraciones requeridas: '+str(it1)+'\n')
                f.write('Nodos expandidos: '+str(ex1)+'\n')
                f.write('Porcentajes del conjunto Z: '+str(Z1)+'\n\n')

                mt_lao.append(t1)
                me_lao.append(ex1)
                mi_lao.append(it1)

                f.write('ILAO*:\n')
                f.write('Tiempo requerido: '+str(t2)+'\n')
                f.write('Iteraciones requeridas: '+str(it2)+'\n')
                f.write('Nodos expandidos: '+str(ex2)+'\n\n')
            
                mt_ilao.append(t2)
                me_ilao.append(ex2)
                mi_ilao.append(it2)

#                f.write('RLAO*:\n')
#                f.write('Tiempo requerido: '+str(t3)+'\n')
#                f.write('Iteraciones requeridas: '+str(it3)+'\n')
#                f.write('Nodos expandidos: '+str(ex3)+'\n\n')

#                mt_rlao.append(t3)
#                me_rlao.append(ex3)
#                mi_rlao.append(it3)

                f.write('BLAO*:\n')
                f.write('Tiempo requerido: '+str(t4)+'\n')
                f.write('Iteraciones requeridas: '+str(it4)+'\n')
                f.write('Nodos expandidos: '+str(ex4)+'\n\n')

                mt_blao.append(t4)
                me_blao.append(ex4)
                mi_blao.append(it4)                

                f.write('VI:\n')
                f.write('Tiempo requerido: '+str(t5)+'\n')
                f.write('Iteraciones requeridas: '+str(it5)+'\n\n')

                mt_vi.append(t5)
                mi_vi.append(it5)

            f.write('Media tiempo LAO: '+str(round(sum(mt_lao)/len(mt_lao), 3))+'\n')
            f.write('Media iteraciones LAO: '+str(round(sum(mi_lao)/len(mi_lao), 3))+'\n')
            f.write('Media expansiones LAO: '+str(round(sum(me_lao)/len(me_lao), 3))+'\n\n')

#            f.write('Media tiempo RLAO: '+str(round(sum(mt_rlao)/len(mt_rlao), 3))+'\n')
#            f.write('Media iteraciones RLAO: '+str(round(sum(mi_rlao)/len(mi_rlao), 3))+'\n')  
#            f.write('Media expansiones RLAO: '+str(round(sum(me_rlao)/len(me_rlao), 3))+'\n\n')

            f.write('Media tiempo ILAO: '+str(round(sum(mt_ilao)/len(mt_ilao), 3))+'\n')
            f.write('Media iteraciones ILAO: '+str(round(sum(mi_ilao)/len(mi_ilao), 3))+'\n')   
            f.write('Media expansiones ILAO: '+str(round(sum(me_ilao)/len(me_ilao), 3))+'\n\n')

            f.write('Media tiempo BLAO: '+str(round(sum(mt_blao)/len(mt_blao), 3))+'\n')
            f.write('Media iteraciones BLAO: '+str(round(sum(mi_blao)/len(mi_blao), 3))+'\n')  
            f.write('Media expansiones BLAO: '+str(round(sum(me_blao)/len(me_blao), 3))+'\n\n')

            f.write('Media tiempo VI: '+str(round(sum(mt_vi)/len(mt_vi), 3))+'\n')
            f.write('Media iteraciones VI: '+str(round(sum(mi_vi)/len(mi_vi), 3))+'\n\n')                               

            f.write("-------------------------------------------------------\n")