# -*- coding: utf-8 -*-

"""
Usar con Python 2.x
Utilerías miscelaneas para archivo
"""

import codecs
import os
import time
import shutil


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

def eliminar_carpeta(carpeta_a_eliminar):

    try:
        # Verificar si la carpeta existe antes de intentar eliminarla
        if os.path.exists(carpeta_a_eliminar):
            # Eliminar la carpeta y su contenido de manera recursiva
            shutil.rmtree(carpeta_a_eliminar)
            return u"La carpeta {}\ny su contenido han sido eliminados.".format(carpeta_a_eliminar)
        else:
            return u"La carpeta {}\nno existe.".format(carpeta_a_eliminar)
    except Exception as e:
        return str(e)

def copiar_carpeta(origen, destino):
    try:
        if os.path.exists(origen):
            shutil.copytree(origen, destino)
            return u'La carpeta se copió correctamente'
        else:
            return u'La carpeta origen no existe'
    except Exception as e:
        return str(e)
    
def copiar_archivo(origen, destino, sobreescr=False):
    try:
        if os.path.exists(origen):
            if sobreescr == False and os.path.exists(destino):
                return u'el archivo existe y no será sobreescrito (cambiar parámetro si se desea)'
            else:
                shutil.copy(origen, destino)
                return u'El archivo se copió correctamente'
        else:
            return u'El archivo origen no existe'
    except Exception as e:
        return str(e)

def listar_carpeta(carpeta):
    # Lista de carpetas en la carpeta principal
    archivos = [nombre for nombre in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, nombre))]
    return archivos

