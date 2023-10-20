# -*- coding: utf-8 -*-

#----> PROCESO PARA APLICAR TRANSPARENCIA A UNA CAPA

import arcpy
import importlib
import sys
# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"aplica_transparencia.py cargado con éxito")

mxd = arcpy.env.mxd

def transp(capa,transparencia):

    log.log(u"'transp.transp' iniciando...")

    try:
    
        df = arcpy.env.df
        for capatr in arcpy.mapping.ListLayers(mxd, "*", df):
            if capatr.name == capa:
                capatr.transparency = transparencia
                arcpy.RefreshActiveView()
        log.log(u"Proceso transparencia al " + str(transparencia) + u"% para la capa '" + capa + u"' terminado")
    
    except Exception as e:
        log.log(u">> ERROR, el proceso aplicar transparencia falló")
        log.log(str(e))

    log.log(u"'transp.transp' terminado")
    
    