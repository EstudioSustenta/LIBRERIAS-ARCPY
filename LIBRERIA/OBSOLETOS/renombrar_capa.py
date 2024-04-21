# -*- coding: utf-8 -*-


# SCRIPT PARA renombrar_capaS.

import arcpy
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'renombrar_capa.py' cargado con éxito")

mxd = arcpy.env.mxd          # Obtener acceso al documento actual

def renomb(caparen, nuevonomb):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_renomb_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'renombrar_capa.renomb' iniciando...")
    try:
        
        capas = arcpy.mapping.ListLayers(mxd)
        
        for capa in capas:
            if capa.name == caparen:
                capa.name = nuevonomb
                log.log(repet,"'{}' renombrada correctamente como '{}'".format(capa.name, nuevonomb))

    except Exception as e:
        log.log(repet,u">> ERROR, el proceso renombrar capa falló para '{}' con '{'}".format(capa.name, nuevonomb))
        log.log(repet,str(e))

    tiempo_renomb_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'renombrar_capa': {}".format(tiempo.tiempo([tiempo_renomb_ini,tiempo_renomb_fin])))

    log.log(repet,u"'renombrar_capa.renomb' finalizado!")
    arcpy.env.repet = arcpy.env.repet - 1