#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   version: 0.0.10
   Metodos vns usando diferentes heuristicas
"""


import random

from libs.mis_decoradores import tiempo_ejecucion_

from tsp import distance as dist
from tsp import get_obj_function_value as fobj
from tsp import create_memory, update_matrix, update_memory


from extras import *

#esta es una sub funcion por eso no la decoro
def min_(k, vertex_list, dist_matrix=[]):
    """
        Calcula el vertice perteneciente a vertex_list mas cercano a k.

        Retorna
            ady_vertex : vertice mas cercano a k
            cost: costo de agregar el nuevo vertice
    """
    ady_vertex = None #vertice adyacente que se agregara
    cost = 9999999999 #defino un costo inicial muy elevado
    for vert in vertex_list: #bobo un algoritmo de busqueda
        if vert != k:
            ncost = dist(k, vert, dist_matrix)
            if ncost < cost:
                ady_vertex = vert
                cost = ncost
    return ady_vertex, cost


@tiempo_ejecucion_
def greedy(vertex_list=[], dist_matrix=[], vertex_ini=0):
    """
        Algoritmo Boraz, buscara armar el recorrido conectando siempre el nodo
        mas cercano que no este en el recorrido. en esta version se puede
        definir el nodo raiz o inicial.
    """
    vertex = range(len(vertex_list))
    solution = [vertex_ini] #la solucion comenzara con el vertice 0
    vertex.pop(vertex.index(vertex_ini))
    while vertex != []:
        #conecta el  nodo mas cercano a la solucion pre armada
        i, ci = min_(solution[0], vertex, dist_matrix)
        j, cj = min_(solution[-1], vertex, dist_matrix)
        if ci < cj:
            solution.append(i)
            vertex.pop(vertex.index(i))
        else:
            solution = [j] + solution
            vertex.pop(vertex.index(j))
    return solution


#@tiempo_ejecucion_
def opt2(solution=[], dist_matrix=[]): #no puedo llamarle 2_opt
    """
        Implementacion del algoritmo 2-Optimo
        nota: nelson descubrio donde fallaba el algoritmo :P
    """
    n_vertex = len(solution)
    soluc = solution[:]
    for i in xrange(n_vertex-3):
        for j in xrange(i+2, n_vertex-1):
            vi = soluc[i]
            vj = soluc[i+1]
            vk = soluc[j]
            vl = soluc[j+1]

            d1 = dist(vi,vj,dist_matrix) + dist(vk,vl,dist_matrix)
            d2 = dist(vi,vk,dist_matrix) + dist(vj,vl,dist_matrix)

            if d2 < d1:
                ini = soluc[:i+1]
                med = soluc[i+1:j+1]
                med.reverse()
                fin = soluc[j+1:]
                soluc = ini + med + fin

    return soluc


@tiempo_ejecucion_
def opt2_(solution=[], dist_matrix=[]):
    """
        Implementacion del algoritmo 2-Optimo o como se supone que deveria
        funcionar el algoritmo de arriba
    """
    n_vertex = len(solution)
    soluc = solution[:]
    for i in xrange(n_vertex - 2):
        for j in xrange(i+2, n_vertex - 1):
            sol = soluc[:]
            ini = soluc[:i+1]
            med = soluc[i+1:j+1]
            med.reverse()
            fin = soluc[j+1:]
            sol = ini + med + fin
            if fobj(sol, dist_matrix) < fobj(soluc, dist_matrix):
                soluc = sol[:]
    return soluc


@tiempo_ejecucion_
def opt3(solution=[], d_m=[]):
    """
        Implementacion del Algoritmo 3-Optimo
    """
    n_vertex = len(solution)
    soluc = solution[:]
    for i in xrange(n_vertex-5):
        for j in xrange(i+2, n_vertex-3):
            for k in xrange(j+2, n_vertex-3):
                va, vb = soluc[i], soluc[i+1]
                vc, vd = soluc[j], soluc[j+1]
                ve, vf = soluc[k], soluc[k+1]

                #calculo las distancias de todas las posibles conbinaciones

                distances = [
                    dist(va,vb,d_m) + dist(vc,vd,d_m) + dist(ve,vf,d_m),
                    dist(va,vc,d_m) + dist(vb,vd,d_m) + dist(ve,vf,d_m),
                    dist(va,vb,d_m) + dist(vc,ve,d_m) + dist(vd,vf,d_m),
                    dist(va,vc,d_m) + dist(vb,ve,d_m) + dist(vd,vf,d_m),
                    dist(va,vd,d_m) + dist(ve,vb,d_m) + dist(vc,vf,d_m),
                    dist(va,ve,d_m) + dist(vd,vb,d_m) + dist(vc,vf,d_m),
                    dist(va,vd,d_m) + dist(ve,vc,d_m) + dist(vb,vf,d_m),
                    dist(va,ve,d_m) + dist(vd,vc,d_m) + dist(vb,vf,d_m),
                ]

                ini = soluc[:i+1] #tramo hasta a includo
                t_bc = soluc[i+1:j+1] #tramo bc
                t_de = soluc[j+1:k+1] #tramo de
                fin = soluc[k+1:] #tramo desde f includo

                d = distances[:]
                d.sort()
                min = distances.index(d[0])

                #el primer caso es el original, no implica ningun cambio
                #por eso no hago nada, ahh aca no hay case pero lo mismo eso
                #se soluciona a como sigue :P
                if min == 1:
                    t_bc.reverse()

                elif min == 2:
                    t_de.reverse()

                elif min == 3:
                    t_bc.reverse()
                    t_de.reverse()

                #cuando min = 4 solo invierte las posiciones de tramos bc y ef
                #osea intercambo ambos tramos bc -> ef y ef -> bc

                elif min == 5:
                    t_de.reverse()

                elif min == 6:
                    t_bc.reverse()

                elif min == 7:
                    t_bc.reverse()
                    t_de.reverse()

                if min < 4:
                    soluc = ini + t_bc + t_de + fin
                else:
                    soluc = ini + t_de + t_bc + fin
    return soluc


@tiempo_ejecucion_
def opt3_(solution=[], d_m=[]):
    """
        Implementacion del Algoritmo 3-Optimo,

        optimizado en velocidad calculo
    """
    n_vertex = len(solution)
    soluc = solution[:]
    for i in xrange(n_vertex-5):
        for j in xrange(i+2, n_vertex-3):
            for k in xrange(j+2, n_vertex-3):
                va, vb = soluc[i], soluc[i+1]
                vc, vd = soluc[j], soluc[j+1]
                ve, vf = soluc[k], soluc[k+1]

                #calculo las distancias de todas las posibles conbinaciones
                #muchos calculos entre las conv se repiten y para no hacerlos
                #de nuevo los calculo una sola ves lo que reduce a la mitad la
                #cantida usos de la func dist
                d_ab = dist(va,vb,d_m)
                d_ac = dist(va,vc,d_m)
                d_ad = dist(va,vd,d_m)
                d_ae = dist(va,ve,d_m)

                d_ef = dist(ve,vf,d_m)
                d_df = dist(vd,vf,d_m)
                d_cf = dist(vc,vf,d_m)
                d_vf = dist(vb,vf,d_m)

                d_bd = dist(vb,vd,d_m) # d_bd = d_db
                d_cd = dist(vc,vd,d_m) # d_cd = d_dc
                d_be = dist(vb,ve,d_m) # d_be = d_eb
                d_ce = dist(vc,ve,d_m) # d_ce = d_ec

                distances = [
                    d_ab + d_cd + d_ef,
                    d_ac + d_bd + d_ef,
                    d_ab + d_ce + d_df,
                    d_ac + d_be + d_df,
                    d_ad + d_be + d_cf,
                    d_ae + d_bd + d_cf,
                    d_ad + d_ce + d_vf,
                    d_ae + d_cd + d_vf,
                ]

                ini = soluc[:i+1] #tramo hasta a includo
                t_bc = soluc[i+1:j+1] #tramo bc
                t_de = soluc[j+1:k+1] #tramo de
                fin = soluc[k+1:] #tramo desde f includo

                #d = distances[:]
                #d.sort()
                mini = distances.index(min(distances))

                #el primer caso es el original, no implica ningun cambio
                #por eso no hago nada, ahh aca no hay case pero lo mismo eso
                #se soluciona a como sigue :P
                if mini == 1:
                    t_bc.reverse()

                elif mini == 2:
                    t_de.reverse()

                elif mini == 3:
                    t_bc.reverse()
                    t_de.reverse()

                #cuando min = 4 solo invierte las posiciones de tramos bc y ef
                #osea intercambo ambos tramos bc -> ef y ef -> bc
                elif mini == 5:
                    t_de.reverse()

                elif mini == 6:
                    t_bc.reverse()

                elif mini == 7:
                    t_bc.reverse()
                    t_de.reverse()

                if mini < 4:
                    soluc = ini + t_bc + t_de + fin
                else:
                    soluc = ini + t_de + t_bc + fin
    return soluc


#@tiempo_ejecucion_
def vns_opt2(solution=[], dist_matrix=[]): #no puedo llamarle 2_opt
    """
        Implementacion del algoritmo 2-Optimo  que funciona como VNS
        el algoritmo es algo trucho pero es entre 10 y 20 veses mas rapido
        que 3opt y los resultados varian muy poco
    """
    n_vertex = len(solution)
    soluc = solution[:]

    loop=True
    while loop:
        i=0
        while i < n_vertex-3:
            j = i + 2
            while j < n_vertex-1:
                vi = soluc[i]
                vj = soluc[i+1]
                vk = soluc[j]
                vl = soluc[j+1]

                d1 = dist(vi,vj,dist_matrix) + dist(vk,vl,dist_matrix)
                d2 = dist(vi,vk,dist_matrix) + dist(vj,vl,dist_matrix)

                if d2 < d1:
                    ini = soluc[:i+1]
                    med = soluc[i+1:j+1]
                    med.reverse()
                    fin = soluc[j+1:]
                    soluc = ini + med + fin
                    i = 0
                    j = 1 #con esto remplazo el break de abajo
                    #break #los break no son muy elegantes por eso lo quito
                j += 1
            i += 1
            if i == n_vertex - 3:
                loop = False
    return soluc

def nearest_vertex(distances, size):
    random.seed()
    tsp_sol = []
    number_of_vertex = size
    vertex_list = range(number_of_vertex)
    incoming_vertex = random.randint(0,number_of_vertex-1)
    min_distance = 0
    tsp_sol.append(incoming_vertex)
    vertex_list.remove(incoming_vertex)
    counter = 0
    echo("building solution.....")
    while counter < number_of_vertex-1:
        flag = 0
        vertex = tsp_sol[-1] #el ultimo elemento de tsp_sol
        for vertex_2 in vertex_list:
            if not flag:
                flag = 1
                min_distance=dist(vertex,vertex_2,distances)
                incoming_vertex = vertex_2
            else:
                temp_distance = dist(vertex,vertex_2,distances)
                if min_distance > temp_distance:
                    min_distance = temp_distance
                    incoming_vertex = vertex_2
        tsp_sol.append(incoming_vertex)
        vertex_list.remove(incoming_vertex)
        counter+=1
    echo("Done")
    return tsp_sol

def solution_validator(solution,size):
    vertex_list = [0]*size
    if len(solution)<size:
        print "BAD SOLUTION!!!!!!! --- Incomplete solution"
        return 0
    for vertex in solution:
        if not vertex_list[vertex]:
            vertex_list[vertex] = 1
        else:
            print "BAD SOLUTION!!!!!!! --- repeated vertex in solution"
            return 0
    print "solution ok----"
    return 1

def perturb(solution_o, amount, max):
    """
    deprecated
    """
    random.seed()
    solution = solution_o[:]
    for index in range(amount):
        i = random.randint(0,max-1)
        j = random.randint(0,max-1)
        aux = solution[i]
        solution[i] = solution[j]
        solution[j] = aux
    return solution

def create_neighbor(solution_o, k, memory, maximum, probability, distances, invert_mode = False):
    """
    Crea un vecino de solution perteneciente al vecindario k, pero tomando
    en cuenta la memoria de largo plazo
    """
    if not invert_mode:
        a = 0
        b = -1
    else:
        a = 1
        b = 1
    random.seed()
    solution = solution_o[:]
    selected = []
    alredy_selected = [0]*len(solution_o)
    if k == len(solution):
        selected = solution
    else:
        for i in range(k):
            found = 0
            while not found:
                alredy_used = 0
                while not alredy_used:
                    vertex = random.choice(solution)
                    index = solution.index(vertex)
                    if alredy_selected[index] == 0:
                        alredy_used = 1
                vertex_a = solution[index-1]
                if index == (len(solution)-1):
                    index = -1
                vertex_p = solution[index+1]
                counter_a = dist(vertex_a, vertex, memory)
                counter_p = dist(vertex_p, vertex, memory)
                if counter_a > counter_p:
                    counter = counter_a
                else:
                    counter = counter_p
                prob = counter*probability/maximum
                prob = (a-prob)*b
                luck = random.random()
                #print prob, luck, maximum
                if luck >= prob:
                    selected.append(vertex)
                    alredy_selected[index] = 1
                    found = 1
    neighbor = solution_o[:]
    vertex = random.choice(selected)
    selected.remove(vertex)
    index = neighbor.index(vertex)
    while selected != []:
        vertex_b = random.choice(selected)
        selected.remove(vertex_b)
        index_b = neighbor.index(vertex_b)
        neighbor[index] = vertex_b
        neighbor[index_b] = vertex
        index = index_b
    return neighbor


def find_local_optima_2opt(solution_o = [],value_of_solution = 0, distances = []):
    """
        Aplica una heurística hasta que encuentra un optimo local
    """
    solution = solution_o[:]
    value_temp = 0
    local_optima = 0
    while not local_optima:
        temp_solution = opt2(solution,distances)
        value_temp = fobj(temp_solution, distances)
        if value_of_solution == value_temp:
            local_optima = 1
        if value_temp < value_of_solution:
            solution = temp_solution
            value_of_solution = value_temp
    return solution, value_of_solution


@tiempo_ejecucion_
def find_local_optima_2optmod(solution = [],value_of_solution = 0, distances = []):
    """
        Aplica una heurística hasta que encuentra un optimo local
    """
    value_temp = 0
    local_optima = 0
    counter = 0
    while not local_optima:
        temp_solution = vns_opt2(solution,distances)
        value_temp = fobj(temp_solution, distances)
        if value_of_solution == value_temp:
            local_optima = 1
        if value_temp < value_of_solution:
            solution = temp_solution
            value_of_solution = value_temp
        counter +=1
        print counter
    return solution, value_of_solution


@tiempo_ejecucion_
def vns_opt(initial_solution, value_of_initial, limit_k, iterations, dist_matrix):

    problem_size = len(initial_solution)
    value_best_solution = value_of_initial
    best_solution = initial_solution[:]
    echo("Primera Solucion", value_best_solution)
    stop_condition = 0
    #intento de VNS
    #se hace hasta que se alcance el criterio de parada
    while stop_condition < iterations:
        neigborhood = 1
        #repito hasta que alcance al limite de vecindarios
        while neigborhood < limit_k:
            #creo una solucion de el vecindario correspondiente a neigborhood
            k = problem_size/(neigborhood)
            neighbor = perturb(best_solution, k, problem_size)
            value_neighbor = fobj(neighbor, dist_matrix)
            local_optima, value_local_optima = find_local_optima_2opt(neighbor, value_neighbor, dist_matrix)
            #print "partial solution",value_local_optima,"best solution",best_solution,"neig",k

            if value_local_optima < value_best_solution:
                #me muevo a la nueva solucion
                echo("new best solution", value_local_optima)
                value_best_solution = value_local_optima
                best_solution = local_optima[:]
                neigborhood = 1
            else:
                neigborhood+=1

        stop_condition+=1
    solution_validator(best_solution, problem_size)
    return value_best_solution,best_solution


@tiempo_ejecucion_
def vns_opt_improved(initial_solution, value_of_initial, limit_k, iterations, probability, dist_matrix):
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
    


