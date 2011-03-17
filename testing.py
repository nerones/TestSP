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
    #opc = menu()
    #if opc != '0':
        #file_name = raw_input('Nombre del fichero: ')
        name, comment, vertex_list = tsp_load('ch130.tsp', False, True)
        print 'Problema:', name
        print 'Comentarios:', comment
        # falta revisar como me muevo entre vecindarios
        # y cuantos vecindarios uso
        problem_lenght = len(vertex_list)
        dist_matrix = gen_distance_matrix(vertex_list)
        #creo una solucion inicial 
        a = nearest_vertex(dist_matrix,problem_lenght)
        solution_validator(a,problem_lenght)
        value_a = get_obj_function_value(a, dist_matrix)
        best_solution =value_a
        solution = a
        a2 = a[:]
        print "Primera Solucion", value_a
        local_optima = 0
                #aplico busqueda local hasta que me encuentro con un 
                #optimo local
        while not local_optima:
            temp_solution = opt2(a,dist_matrix)
            value_temp = get_obj_function_value(temp_solution, dist_matrix)
            if value_a == value_temp:
                local_optima = 1
            if value_temp < value_a:
                a = temp_solution
                value_a = value_temp
        print "partial solution",value_temp,"best solution",best_solution#,"neig",neigborhood
        vns_opt = opt2(a2,dist_matrix)
        vns_opt = vns_opt2(vns_opt,dist_matrix)
        vns_opt = vns_opt2(vns_opt,dist_matrix)
        vns_opt_v = get_obj_function_value(vns_opt,dist_matrix)
        vopt3 = opt3_(a2,dist_matrix)
        vvopt3 = get_obj_function_value(vopt3,dist_matrix)
        print "opt_vns", vns_opt_v, "2-opt-iter", value_a, "3opt", vvopt3
if __name__ == '__main__':
    main()

