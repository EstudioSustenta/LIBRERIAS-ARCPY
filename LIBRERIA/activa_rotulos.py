# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys

mxd = arcpy.env.mxd

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"Librería 'activa_rotulos' se ha cargado con éxito")

def activar_rotulos(capa, campo_rotulo):
    log.log(u"Iniciando 'activar_rotulos'...")

    try:
        capa = arcpy.mapping.Layer(capa)
        # Habilita los rótulos para la capa
        capa.showLabels = True
        # Configura la expresión de rótulo
        labelClass = capa.labelClasses[0]
        labelClass.expression = "[{}]".format(campo_rotulo)
        log.log(u"Rótulos activados satisfactoriamente para capa " + capa.name)
    except Exception as e:
        log.log(u">> ERROR, los rótulos no se han activado para capa " + capa.name)
        log.log(str(e))

    log.log(u"'activar_rotulos' finalizado")


def desactivar_rotulos(capa):
    log.log(u"Iniciando 'desactiva_rotulos'...")

    try:
        # Obtiene la capa activa del mapa
        capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica
        # Habilita los rótulos para la capa
        capa.showLabels = False
        log.log(u"Rótulos desactivados satisfactoriamente para capa " + capa.name)
    except Exception as e:
        log.log(u">> ERROR, los rótulos no se han desactivado para capa " + capa.name)
        log.log(str(e))

    log.log(u"'desactivar_rotulos' terminado...")

    # Refresca la vista de datos para aplicar los cambios de rótulos

# Ejemplo de uso:
# desactivar_rotulos("MUNICIPAL CENSO 2020 DECRETO 185")
