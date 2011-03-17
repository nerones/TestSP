#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plantilla creada por Ricardo D. Quiroga
# licencia: GPL2
# email: l2radamanthys@gmail.com, ricardoquiroga.dev@gmail.com
# http://www.l2radamanthys.tk

import pygtk
pygtk.require('2.0')
import gtk
from gtk import glade

#importe aqui los Form que utilizara su App, por ejemplo:
import frm_main

class MiApp:
    def __init__(self):
        #parse referente al XML remplace ".glade" por el nombre
        #del archivo generado por glade que usara
        self.xml = glade.XML('calc.glade')

        #Aplicacion principal
        #llame aqui a todas las ventanas que utilizara por ejemplo:
        self.frm_main = frm_main.Form(self.xml)

    def main(self):
        #pasar el control principal a GTK
        gtk.main()

    def destroy(self):
        #detener la ejecucion de la aplicacion
        gtk.main_quit()

if __name__ == "__main__":
    app = MiApp()
    app.main()
