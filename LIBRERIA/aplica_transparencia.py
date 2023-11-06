# -*- coding: utf-8 -*-

#----> PROCESO PARA APLICAR TRANSPARENCIA A UNA CAPA

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

log.log(repet,u"Librería 'aplica_transparencia.py' cargado con éxito")

mxd = arcpy.env.mxd

def transp(capa,transparencia):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_transp_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"'transp.transp' iniciando...")

    try:
    
        df = arcpy.env.df
        for capatr in arcpy.mapping.ListLayers(mxd, "*", df):
            if capatr.name == capa:
                capatr.transparency = transparencia
        log.log(repet,u"Transparencia al " + str(transparencia) + u"% para la capa '" + capa + u"' aplicado")
    
    except Exception as e:
        log.log(repet,u">> ERROR, el proceso aplicar transparencia falló")
        log.log(repet,str(e))
    
    tiempo_transp_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería aplica_transparencia.py: {}".format(tiempo.tiempo([tiempo_transp_ini,tiempo_transp_fin])))

    log.log(repet,u"'transp.transp' finalizado")

    arcpy.env.repet = arcpy.env.repet - 1
