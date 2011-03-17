#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

from src.load import tsp_load_
from src.tsp import *
from src.algoritmos import *
from src.extras import *


#cantidd veces correre el algoritmo por problema
NRO_PRUEVAS = 20
#numero de vecindades que tendra el problema
NRO_VECINDADES = 25
#nro maximo iteraciones por vecindad
MAX_ITERACIONES = 10

PROBABILIDAD = 0.98


def eval_problema(prob_name):
    name, comment, w_type, vertex_list = tsp_load_(prob_name, True)
    dist_matrix = gen_distance_matrix_(vertex_list, w_type)
    n_vertex = len(vertex_list)

    echo('--- Iniciando pruebas ---')
    for i in xrange(NRO_PRUEVAS):
        soluc_a = nearest_vertex(dist_matrix, n_vertex)
        value_a = get_obj_function_value(soluc_a, dist_matrix)
        echo('------------------------------------------------------')
        echo('Problema: ',name)
        echo('Comentarios: ',comment)
        echo('Inicio: ',time.strftime("[%d/%m/%Y-%H:%M:%S]"))
        echo('---------------- Inicio Prueba Nro %d ----------------' %i)
        echo('NRO Vecindades: ', NRO_VECINDADES)
        echo('Iteraciones por vecindad: ', MAX_ITERACIONES)
        echo('Probabilidad: ', PROBABILIDAD)
        echo('------------------------------------------------------','\n')
        value_a, soluc_a = vns_opt_improved(soluc_a, value_a, NRO_VECINDADES,\
                    MAX_ITERACIONES, PROBABILIDAD, dist_matrix)

        echo('\n','------------------------------------------------------')
        echo('Fin: ',time.strftime("[%d/%m/%Y-%H:%M:%S]"))
        echo('Mejor Solucion: ', value_a)

        #guardamos la mejor solucion de la instancia
        sol_name = 'mejor_sol_%s_%d.dat' %(name, i)
        save_solucion(sol_name, soluc_a)

        data_name = 'prueva_%s_%d.txt' %(name, i)
        os.rename('stdout.txt', data_name)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        eval_problema(sys.argv[1])
    else:
        problema = raw_input('Problema: ')
        eval_problema(problema)
