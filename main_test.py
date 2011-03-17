#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from src.libs.mis_decoradores import captura_stdout

from src.load import tsp_load, tsp_sol_load
from src.tsp import *
from src.algoritmos import *


def menu():
    loop = True
    while loop:
        os.system('clear')
        print"""
    =====================================================
                    TSP Tester - version 0.0.1
    =====================================================

    1 - Cargar un Problema de TSPlib
    2 - Cargar un Problema de TSP en otro dir
    0 - Salir

    """
        opcion = raw_input('Elija una opcion y precione Enter: ')
        if opcion in ('0','1','2'):
            loop = False
        else:
            raw_input('Opcion No Valida...')
    return opcion


def main():
    #505
    opc = menu()
    if opc != '0':
        #file_name = raw_input('Nombre del fichero: ')
        name, comment, vertex_list = tsp_load('eil51.tsp', False, True)
        print 'Problema:', name
        print 'Comentarios:', comment
        sol = 999999999 #valor muy alto para una solucion inicial base
        dist_matrix = gen_distance_matrix(vertex_list)

        for i in xrange(len(vertex_list)):
            s0 = greedy(vertex_list, dist_matrix, i)
            s1 = opt2(s0, dist_matrix)
            s2 = vns_opt2(s1, dist_matrix)
            nsol = get_obj_function_value(s2, dist_matrix)
            if nsol < sol:
                sol = nsol
                ms = s1[:]
                print 'nueva mejor sol :P'
            print 'greedy',i, 'sol: 2opt+vns', nsol, 'mejor:', sol

        s3 = opt3_(ms, dist_matrix)
        print 'opt3', get_obj_function_value(s3, dist_matrix)
        s4 = vns_opt2(ms, dist_matrix)
        print 'vns_2opt', get_obj_function_value(s4, dist_matrix)


if __name__ == '__main__':
    main()





