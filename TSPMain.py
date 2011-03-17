import string
from string import *
import math
from math import *
import re
import time
from time import *
import random
from random import *
import copy

def openFile():
    fileName=raw_input("ingrese nombre y ruta del archivo:")
    archivo=open('p654.tsp', 'r')#(fileName,"r")
    linea=archivo.readline()
    problemName=linea.strip().split(":")[1]
    j=0
    cant_datos=0 #cuento los datos...
    data=[]
    while linea:
        if (linea.strip()=="NODE_COORD_SECTION"):
            j=1
        elif ((j==1) and (linea.strip()!="EOF")):
            cant_datos+=1
            linea=linea.strip().split(" ")
            data.append([atof(linea[1]),atof(linea[2])])            
        linea=archivo.readline()        
    archivo.close()
    print "___la cantidad de datos del archivo " + problemName + " es: " + str(cant_datos)              
    return data,problemName


def getProbability():
    vProb=input("ingrese probabilidad:")
    return vProb

def getDrones():
    vDrones=input("ingrese el numero de zanganos:")
    return vDrones

def getFlights():
    vFlights=input("ingrese el numero de vuelos de la reina:")
    return vFlights

def getDistanceMatrix(data):
    distanceMatrix=[]
    max = len(data)
    
    for i in range(max-1):
        distanceMatrix.append([])
        for j in range(i+1,max):
            distance = sqrt(pow((data[i][0]-data[j][0]),2)+pow((data[i][1]-data[j][1]),2))
            distanceMatrix[i].append(distance)                
    return distanceMatrix

def getNaiveSolution(rangeOfData):
    solution=[]
    seed()

    max=rangeOfData    
    for i in range(max):
        vertexAtRandom=randint(0,max-1)
        while vertexAtRandom in solution:
            vertexAtRandom=randint(0,max-1)
        solution.append(vertexAtRandom)
    return solution

# voy a obtener una secuencia de rk
# rkvlist es la lista generada hasta el momento
def getRKVSolution(rangeOfData, minValue, maxValue, rkvList):    
    seed()
    
    rkvList.append([])
    nbrOfSolutions=len(rkvList)
    max=rangeOfData

    lista_val = range(minValue, maxValue)
    
    for i in range(max):
        randomKey=randint(minValue,maxValue)
        #randomKey = lista_val.pop(lista_val.index(choice(lista_val)))
        flag=True
        while flag==True:
            j=0        
            while j<nbrOfSolutions:
                if randomKey not in rkvList[j]:
                    j+=1
                else:                    
                    j = nbrOfSolutions+10
            if j < nbrOfSolutions+10:
                flag=False
            else:
                randomKey=randint(minValue,maxValue)
    
        rkvList[nbrOfSolutions-1].append(randomKey)           
    

def getObjFunctionValue(distanceMatrix,solution):
    objFunctionValue=0.0
    max = len(solution)

    for i in range(max-1):
        vertexI=solution[i]
        vertexJ=solution[i+1]

        if vertexI<vertexJ:
            objFunctionValue+=distanceMatrix[vertexI][vertexJ-vertexI-1]
        else:
            objFunctionValue+=distanceMatrix[vertexJ][vertexI-vertexJ-1]

    vertexI=solution[max-1]    
    vertexJ=solution[0]        

    if vertexI<vertexJ:        
        objFunctionValue+=distanceMatrix[vertexI][vertexJ-vertexI-1]
    else:
        objFunctionValue+=distanceMatrix[vertexJ][vertexI-vertexJ-1]
   
    return objFunctionValue


def getInitialRKVs(rangeOfData, population, minValue, maxValue):
    rkvList=[]

    for i in range(population):        
        getRKVSolution(rangeOfData, minValue, maxValue, rkvList)
       
    return rkvList

	
def dist(i, j, m):
    if i < j:
        return m[i][j-i-1]
    else: 
        return m[j][i-j-1]	

"""
def opt2(sol_orig, matrix_dist):
    leng = len(sol_orig)
    soluc = sol_orig[:]
    for i in xrange(leng-3):
    for j in xrange(i+2,leng-1):
        d1 = dist(i, i+1, matrix_dist) + dist(j, j+1, matrix_dist)
        d2 = dist(i, j, matrix_dist) + dist(i+1, j+1, matrix_dist)
        if d1 > d2:
        #d = d1 ; pj = j ; pi = i
            ini = soluc[:i]
            medio = soluc[i+1:j+1]
            medio.reverse()
            fin = soluc[j+1:]
            soluc = ini + medio + fin
    return soluc
"""

# obtiene una solucion al tsp desde un random key vector
def decodeRKV(position, rkvList):
    max = len(rkvList[position])
    randomList = rkvList[position][:]
    positionList = [elem for elem in range(max)]
    tspSol = []

    for i in range(max-1):
        min = i
        for j in range(i+1,max):
            if randomList[j]<randomList[min]:
                min=j
        
        auxRKV=randomList[i]
        auxPos=positionList[i]

        randomList[i] = randomList[min]
        positionList[i] = positionList[min]

        randomList[min] = auxRKV
        positionList[min] = auxPos         
    
    tspIndex = -1
    for i in range(max):
        tspIndex = randomList.index(rkvList[position][i])        
        tspSol.append(tspIndex)    
    return tspSol

def applyUCrossover(motherPos, fatherPos, rkvList, probability):
    seed()
    max = len(rkvList[motherPos])
    childRkv=[]
    for i in range(max):
        valueAtRandom=random()
        if valueAtRandom<probability:
            value=rkvList[fatherPos][i]
        else:
            value=rkvList[motherPos][i]
        childRkv.append(value)

    return childRkv

def solveTSP(data,flights,probability,drones): # tsp!!!
    bestOFValue = 9999999999
    bestIteration=-1
    bestSolution=[]
    
    distanceMatrix=getDistanceMatrix(data)  
    minValue = 500
    maxValue = 200000
    
    rkvList = []
    rkvList = getInitialRKVs(len(data), drones+1, minValue, maxValue)

    # decodifico rkv0
    tspSol = decodeRKV(0, rkvList)
    bestOFValue=getObjFunctionValue(distanceMatrix,tspSol)
    bestSolution=tspSol[:]

    print " la primera solucion es " + str(tspSol) + " funcional " + str(bestOFValue)

    fatherPos =0
    motherPos =1
    
    childRkv = applyUCrossover(motherPos, fatherPos, rkvList, probability)

    print " padre " + str(rkvList[fatherPos]) + "\n"
    print " madre " + str(rkvList[motherPos]) + "\n"
    print " hijo " + str(childRkv) + "\n"

    for iteration in range(flights):
        print " iteration: " + str(iteration)
        for candidate in range(drones):
            f=1
            
                
    print "          ... iteration: " + repr(bestIteration) + " OFValue: " + repr(bestOFValue) 
    
    nueva_sol = opt2(bestSolution, distanceMatrix)
    nueva_val = getObjFunctionValue(distanceMatrix, nueva_sol)
	
    print "mi sol :P" , nueva_val , ' otra ', repr(bestOFValue)
	
    return bestOFValue,bestSolution
   
# grabo los resultados en archivo
def saveResults(solution,flights,probability,drones,tiempo,objFunction,fileSaved):
    bandera=True
    archivo=open(fileSaved, 'w')
    archivo.write('Problema: ' + fileSaved + ' funcional: ' + repr(objFunction) + ' tpo proces: ' + repr(tiempo) + ' \n')
    archivo.write('its: ' + repr(flights) + ' Prob: ' + repr(probability) + ' Drones: ' + repr(drones)+ ' \n')
    archivo.write('====================  \n')
    for i in range(len(solution)):
        archivo.write('     vertex: ' + str(solution[i]) + ' \n')      
    archivo.close()
    return bandera
    

#### Principal ####
option=1
while option!=6:
    print "Naive algorithm for the TSP"
    print ""
    print "--- Options --- "
    print "1-Open DataSet"
    print "3-Get Best Solution with HBMO"
    print "6-Quit"
    option=input("Input Option: ")
    if option==1:
        data,problemName=openFile()
    elif option==3:
        drones=getDrones()
        probability=getProbability()
        flights=getFlights()
        print "      .... processing ... "

        objFunction,solution=solveTSP(data,flights,probability,drones)
        tiempo_ini=time()
        if solution!=[]:
            fileSaved="tsp" + str(drones) + problemName + ".u2"
            tiempo=time()-tiempo_ini
            print " El tiempo de proceso fue de " + repr(tiempo) + " segs. se genero el archivo " + fileSaved
            bandera=saveResults(solution,flights,probability,drones,tiempo,objFunction,fileSaved)            
        else:
            print " El problema " + problemName +  " no tuvo solucion "
                            
    elif option==6:
        print "me pinto de colores..."

