# -*- coding: utf-8 -*-


# SCRIPT PARA renombrar_capaS.

import arcpy
import importlib
import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"renombrar_capa.py cargado con éxito")

mxd = arcpy.env.mxd          # Obtener acceso al documento actual

def renomb(caparen, nuevonomb):
    log.log(u"'renombrar_capa.renomb' iniciando...")
    try:
        
        capas = arcpy.mapping.ListLayers(mxd)
        
        for capa in capas:
            if capa.name == caparen:
                capa.name = nuevonomb
                log.log(capa.name + u" renombrada correctamente")
                arcpy.RefreshActiveView()

    except Exception as e:
        log.log(u">> ERROR, el proceso renombrar capa falló")
        log.log(str(e))

    log.log(u"'renombrar_capa.renomb' finalizado")
