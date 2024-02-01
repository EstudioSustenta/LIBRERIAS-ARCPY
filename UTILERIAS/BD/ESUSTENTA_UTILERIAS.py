# -*- coding: utf-8 -*-

import codecs
import os
import time

def escribearch(fichero, cadena):
    """
    Escribe a un archivo los la cadena que se le envíe en modo
    
    """
    if os.path.exists(fichero):
        modo = 'a'
    else:
        modo = 'w'
    # -*- coding: utf-8 -*-
    with codecs.open(fichero, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena1 = u"\n{}\t{}".format(cadena,fecha_hora_actual)
        archivo_log.write(cadena1)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena1.encode('utf-8'))