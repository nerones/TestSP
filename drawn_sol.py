#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Autor: Ricardo D. Quiroga -> L2Radamanthys
    licencia: GPL2
    Email: l2radamanthys@gmail.com, ricardoquiroga.dev@gmail.com
    Web: http://www.l2radamanthys.com.ar
"""

import os
import sys
import time
import pygame
from pygame.locals import *

from src.load import tsp_load, tsp_sol_load
from src.load import tsp_load_
from src.tsp import *
from src.algoritmos import *
from src.extras import *

#colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

#dimenciones
ANCHO = 1024
ALTO = 768
RESOLUCION = (ANCHO, ALTO)
scale = 0.2

def draw_solution(screen, vertex_list, soluc_a):
    n_vertex = len(vertex_list)

    x_ini = vertex_list[0][0]
    x_fin = vertex_list[0][0]

    y_ini = vertex_list[0][1]
    y_fin = vertex_list[0][1]

    for vertex in vertex_list:
        if vertex[0] > x_fin:
            x_fin = vertex[0]
        if vertex[0] < x_ini:
            x_ini = vertex[0]

        if vertex[1] > y_fin:
            y_fin = vertex[0]
        if vertex[1] < y_ini:
            y_ini = vertex[0]

    print (x_fin - x_ini), (y_fin - y_ini)

    for vertex in vertex_list:
        x, y = vertex
        x = int((x - x_ini + 10)*scale)
        y = int((y - y_ini + 10)*scale)
        pygame.draw.circle(screen, ROJO, (x, y), 2, 0)

    lists = []
    for index in soluc_a:
        x = int((vertex_list[index][0]-x_ini+10)*scale)
        y = int((vertex_list[index][1]-y_ini+10)*scale)
        lists.append([x,y])
    pygame.draw.circle(screen, ROJO, lists[0], 4, 0)
    pygame.draw.lines(screen,AZUL,True,lists)

    print 'fin'

    #loop = True
    #while loop:


        #pygame.display.flip()

        #for evento in pygame.event.get():
            #if evento.type == pygame.QUIT:
                #loop = False


def mainaaa():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUCION)#, pygame.FULLSCREEN)
    screen.fill(BLANCO)

    #name, comment, vertex_list = tsp_load('eil51.tsp', False, True)
    name, comment, w_type, vertex_list = tsp_load_('eil51.tsp', True)
    dist_matrix = gen_distance_matrix_(vertex_list, w_type)
    n_vertex = len(vertex_list)
    soluc_a = nearest_vertex(dist_matrix, n_vertex)


    x_ini = vertex_list[0][0]
    x_fin = vertex_list[0][0]

    y_ini = vertex_list[0][1]
    y_fin = vertex_list[0][1]

    for vertex in vertex_list:
        if vertex[0] > x_fin:
            x_fin = vertex[0]
        if vertex[0] < x_ini:
            x_ini = vertex[0]

        if vertex[1] > y_fin:
            y_fin = vertex[0]
        if vertex[1] < y_ini:
            y_ini = vertex[0]

    print (x_fin - x_ini), (y_fin - y_ini)

    for vertex in vertex_list:
        x, y = vertex
        x = int(x - x_ini + 10)*4
        y = int(y - y_ini + 10)*4
        pygame.draw.circle(screen, ROJO, (x, y), 2, 0)
    lists = []
    for index in soluc_a:
        x = int((vertex_list[index][0]-x_ini+10)*4)
        y = int((vertex_list[index][1]-y_ini+10)*4)
        lists.append([x,y])
    pygame.draw.circle(screen, ROJO, lists[0], 4, 0)
    pygame.draw.lines(screen,AZUL,True,lists)

    print 'fin'

    loop = True
    while loop:


        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loop = False


#cantidd veces correre el algoritmo por problema
NRO_PRUEVAS = 1
#numero de vecindades que tendra el problema
NRO_VECINDADES = 30
#nro maximo iteraciones por vecindad
MAX_ITERACIONES = 20

PROBABILIDAD = 0.98

def vns_opt_improved_graph(initial_solution, value_of_initial, limit_k, iterations, probability, dist_matrix, vertex_list):
    maximum = 1
    problem_size = len(initial_solution)
    value_best_solution = value_of_initial
    best_solution = initial_solution[:]
    memory = create_memory(problem_size)
    echo("Primera Solucion", value_best_solution)
    stop_condition = 0
    #intento de VNS
    #se hace hasta que se alcance el criterio de parada
    iter_counter = 0
    invert_mode = False
    while stop_condition < iterations:
        neigborhood = 1
        #repito hasta que alcance al limite de vecindarios
        while neigborhood < limit_k:
            iter_counter += 1
            #creo una solucion de el vecindario correspondiente a neigborhood
            k = problem_size/(neigborhood)
            #k = problem_size-((problem_size/limit_k)*neigborhood)
            #neighbor = perturb(best_solution, k, problem_size)
            if iter_counter == 50:
                invert_mode = True
                #memory = create_memory(problem_size)
            neighbor = create_neighbor(best_solution,k,memory,maximum,probability,dist_matrix,invert_mode)
            value_neighbor = fobj(neighbor, dist_matrix)
            local_optima, value_local_optima = find_local_optima_2opt(neighbor, value_neighbor, dist_matrix)
            #print "partial solution",value_local_optima,"best solution",value_best_solution,"neig",k
            if value_local_optima <= (value_best_solution*1.1):
                #memory,maximum = update_memory(memory,local_optima,maximum)
                memory,maximum = update_memory(memory,neighbor,maximum)
                #print "memory updated", value_local_optima, (value_best_solution*1.1)
            #else:
                #print "no update", value_local_optima, (value_best_solution*1.1)
            if value_local_optima < value_best_solution:
                screen.fill(BLANCO)
                draw_solution(screen, vertex_list, local_optima)
                pygame.display.flip()
                #me muevo a la nueva solucion
                echo("new best solution", value_local_optima, "iter", iter_counter)
                value_best_solution = value_local_optima
                best_solution = local_optima[:]
                neigborhood = 1
                iter_counter = 0
                invert_mode = False
            else:
                neigborhood += 1

        stop_condition+=1
    echo(iter_counter)
    solution_validator(best_solution, problem_size)
    return value_best_solution, best_solution

pygame.init()
screen = pygame.display.set_mode(RESOLUCION)#, pygame.FULLSCREEN)
screen.fill(BLANCO)
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
        value_a, soluc_a = vns_opt_improved_graph(soluc_a, value_a, NRO_VECINDADES,\
                    MAX_ITERACIONES, PROBABILIDAD, dist_matrix, vertex_list)
        screen.fill(BLANCO)
        draw_solution(screen, vertex_list, soluc_a)

        echo('\n','------------------------------------------------------')
        echo('Fin: ',time.strftime("[%d/%m/%Y-%H:%M:%S]"))
        echo('Mejor Solucion: ', value_a)

        #guardamos la mejor solucion de la instancia
        sol_name = 'mejor_sol_%s_%d.dat' %(name, i)
        save_solucion(sol_name, soluc_a)

        data_name = 'prueva_%s_%d.txt' %(name, i)
        os.rename('stdout.txt', data_name)
        pygame.display.flip()



if __name__ == '__main__':
    if len(sys.argv) == 2:
        eval_problema(sys.argv[1])
    else:
        problema = raw_input('Problema: ')
        eval_problema(problema)
