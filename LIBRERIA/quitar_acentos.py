# -*- coding: utf-8 -*-

import re
import arcpy
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")


log.log(u"'Librería quitar acentos' cargado con éxito")

def acentos(texto):

    tiempo_acentos_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(u"'quitar acentos' iniciando para {}".format(texto))

    # Definir un diccionario de reemplazo para las vocales acentuadas
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }

    # Utilizar una expresión regular para buscar y reemplazar las vocales acentuadas
    patron = re.compile("|".join(re.escape(k) for k in reemplazos))
    sinacento = patron.sub(lambda m: reemplazos[m.group(0)], texto)
    arcpy.env.sinacento = sinacento
    print(arcpy.env.sinacento)

    log.log(u"se han quitado los acentos de '{}' quedando como '{}'".format(texto,sinacento))
    log.log(u"'quitar acentos' finalizado para {}".format(texto))

    tiempo_acentos_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'identity_sistema': {}".format(tiempo.tiempo([tiempo_acentos_ini,tiempo_acentos_fin])))

    return sinacento
