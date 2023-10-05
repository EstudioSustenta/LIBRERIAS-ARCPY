# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"Librería 'activa_rotulos' se ha cargado con éxito")

def activar_rotulos(capa, campo_rotulo):
    log.log(u"Iniciando 'activar_rotulos'...")
    capa = arcpy.mapping.Layer(capa)
    # Habilita los rótulos para la capa
    capa.showLabels = True

    # Configura la expresión de rótulo
    labelClass = capa.labelClasses[0]
    labelClass.expression = "[{}]".format(campo_rotulo)
    log.log(u"'activar_rotulos' terminado...")


def desactivar_rotulos(capa):
    log.log(u"Iniciando 'desactiva_rotulos'...")
    # Obtiene el mapa actual
    mxd = arcpy.mapping.MapDocument("CURRENT")

    # Obtiene la capa activa del mapa
    capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica

    # Habilita los rótulos para la capa
    capa.showLabels = False
    log.log(u"'desactivar_rotulos' terminado...")

    # Refresca la vista de datos para aplicar los cambios de rótulos

# Ejemplo de uso:
# desactivar_rotulos("MUNICIPAL CENSO 2020 DECRETO 185")