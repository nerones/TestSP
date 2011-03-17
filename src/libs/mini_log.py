#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Version: 0.0.3

    Autor: Ricardo D. Quiroga->L2Radamanthys

    Fecha: 13 de Mayo de 2010

    E-mail:
        l2radamanthys@gmail.com
        l2radamanthys@saltalug.org.ar
        ricardoquiroga.dev@gmail.com

    SitioWeb:
        http://www.l2radamanthys.com.ar
        http://l2radamanthys.blogspot.com

    Descripcion:
        Implementacion sencilla de un Mini modulo para crear logs

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

import time

from constantes import STDOUT


class SuccesLog:
    """
        Una sencilla clase que permite almacenar los succesos en un archivo
        txt.
    """
    def __init__(self, file_name=''):
        self.__file = open(file_name, 'a')


    def msj(self, msj=''):
        """
            Almacena el mensaje en el fichero de succesos junto con la fecha
            y hora que se genero
        """
        time_stamp = time.strftime("[%d/%m/%Y-%H:%M:%S]")
        self.__file.write('%s- %s\n' %(time_stamp, msj))
        self.__file.flush()


    def echo_msj(self, msj=''):
        """
            Ademas de almacenar el mensaje en el fichero de succesos lo
            muestra en la terminal
        """
        time_stamp = time.strftime("[%d/%m/%Y-%H:%M:%S]")
        _msj = '%s- %s\n' %(time_stamp, msj)
        self.__file.write(_msj)
        self.__file.flush()
        print _msj,


    def raw_msj(self, msj=''):
        """
            Este metdo permite almacenar un mensaje crudo en el fichero de
            sucesos.
        """
        self.__file.write(msj)
        self.__file.flush()


    def close(self):
        self.__file.close()


#una pequenia prueba...
if __name__ == '__main__':
    STDOUT='ht.txt'
    l = SuccesLog(STDOUT)
    l.echo_msj('hola esto es una prueva')
    l.msj('este msj no se mostrara')
    l.close()
