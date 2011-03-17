#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Version: 0.0.4

    Autor: Ricardo D. Quiroga->L2Radamanthys

    Fecha: 27 de Mayo de 2010

    E-mail:
        l2radamanthys@gmail.com
        l2radamanthys@saltalug.org.ar
        ricardoquiroga.dev@gmail.com

    SitioWeb:
        http://www.l2radamanthys.com.ar
        http://l2radamanthys.blogspot.com

    Descripcion:
        Conjunto de decoradores que comunmente uso, para controlar el tiempo
        de ejecucion de algunas funciones y otras cosas utiles.

    Terminos y Condiciones:
        Este Script es Software Libre y esta bajo terminos de la GNU General
        Public Licence publicada por la Free Software Foundation
        (http://www.fsf.org) version 2 de la licencia u/o (opcionalmente)
        otras versiones de la licencia.

        Usted puede redistribuir y/o modificar este Script
        siguiendo los terminos de la GNU General Public Licence
        para mayor informacion vease la copia de la licencia que
        se adjunta con estos Script.
"""

import datetime
import sys
from StringIO import StringIO

from mini_log import SuccesLog as Log
from constantes import STDOUT


def tiempo_ejecucion(funcion):
    """
        Sencillo decorador que muestra en la terminal cuanto tiempo
        tardo en ejecutarse la funcion decorada.

        Nota: la unidad minima de medicion que retorna el decorador es
        cantidad de segundos.
    """
    def wrapper(*args, **kwargs):
        """
            Simple envoltorio para la funcion a decorar
        """
        t_ini = datetime.datetime.today()
        resultado = funcion(*args, **kwargs) #corro la funcion decorada
        t_fin = datetime.datetime.today()
        #calculamos la diferencia de tiempo entre inicio y fin
        delta = t_fin - t_ini
        print '> El tienpo que tardo la funcion \'%s()\' es: %s' \
                    %(funcion.__name__, str(delta))
        return resultado
    return wrapper


def tiempo_ejecucion_(funcion):
    """
        Esta version ademas almacena la informacion en el fichero log
    """
    def wrapper(*args, **kwargs):
        """
            Simple envoltorio para la funcion a decorar
        """
        t_ini = datetime.datetime.today()
        resultado = funcion(*args, **kwargs) #corro la funcion decorada
        t_fin = datetime.datetime.today()
        #calculamos la diferencia de tiempo entre inicio y fin
        delta = t_fin - t_ini
        mensaje = '> El tienpo que tardo la funcion \'%s()\' es: %s' \
                    %(funcion.__name__, str(delta))
        print mensaje
        log = Log('log.txt')
        log.raw_msj(mensaje+'\n')
        log.close()
        return resultado
    return wrapper


def tiempo_ejecucion_info(function):
    """
        Esta nueva version ademas muestra el momento de inicio y fin de los
         metodos.
    """
    def wrapper(*args, **kwargs):
        """
            Simple envoltorio para la funcion a decorar
        """
        #abro el fichero de log
        log = Log('log.txt')
        #muestro la hora de inicio
        t_ini = datetime.datetime.today()
        msj = '> \'%s()\' Inicio: %s' %(funcion.__name__, str(t_ini))
        print msj
        log.raw_msj(msj + '\n')

        #corro la funcion decorada
        resultado = function(*args, **kwargs)

        #muestro la hora de finalizacion
        t_fin = datetime.datetime.today()
        msj = '> \'%s()\' Finalizo: %s'%(funcion.__name__, str(t_ini))
        print msj
        log.raw_msj(msj + '\n')

        #calculamos la diferencia de tiempo entre inicio y fin
        delta = t_fin - t_ini
        mensaje = '> El tienpo que tardo la funcion \'%s()\' es: %s' \
                    %(funcion.__name__, str(delta))
        print mensaje
        log.raw_msj(mensaje+'\n')
        log.close()
        return resultado
    return wrapper


def captura_stdout(funcion):
    """
        Captura la salida de consola de la funcion en un archivo
    """
    def wrapper(*args, **kwargs):
        """
            envoltorio para la funcion a decorar
        """
        old_stdout = sys.stdout
        fake_stdout = StringIO()
        sys.stdout = fake_stdout
        resultado = funcion(*args, **kwargs)
        sys.stdout = old_stdout
        output = fake_stdout.getvalue()
        #almacenamos la salida de pantalla
        log = Log(STDOUT)
        log.raw_msj(output)
        log.close()
        print output,
        return resultado
    return wrapper


#-------------------------------------------------#
#algunas pruebas del decorador
@tiempo_ejecucion_
def func_1():
    print "hola mundo"

@tiempo_ejecucion_
def func_2(a,b):
    print a + b


#esta dos ultima muestra de paso por que es mejor usar xrange que range :P
@tiempo_ejecucion_
def func_3a(a=0,b=0,n=0):
    c = 0
    for i in xrange(n):
        c = c + (a * b)
    print c
    return c


@tiempo_ejecucion_
def func_3b(a=0,b=0,n=0):
    c = 0
    for i in range(n):
        c = c + (a * b)
    print c
    return c


if __name__ == '__main__':
    func_1()
    func_2(100, 345)
    func_3a(12, 34, 1000000)
    func_3b(12, 34, 1000000)




