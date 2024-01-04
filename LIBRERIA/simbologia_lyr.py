# -*- coding: utf-8 -*-

# SCRIPT PARA APLICAR SIMBOLOGÍA A UNA CAPA.
# PARTE DEL PRINCIPIO DE QUE EXISTE UNA CAPA DE SIMBOLOGÍA EN EL DIRECTORIO CORRESPONDIENTE
# CON UN ARCHIVO .lyr DEL MISMO NOMBRE QUE LA CAPA QUE SE ESTÁ CARGANDO. LA RUTA DEL ARCHIVO
# TAMBIÉN ES LA PREDEFINIDA: (u"Y:\0_SIG_PROCESO\MAPAS\SIMBOLOGIA")

import arcpy
import importlib
import sys
import datetime

mxd = arcpy.env.mxd
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'simbologia_lyr' cargado con éxito")


def aplica_simb(capa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_aplica_simb_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:
        log.log(repet,u"'simbologia_lyr.aplica_simb' iniciando para '{}'...".format(capa))

        simbologia = 'Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/{}.lyr'.format(capa)
        lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
        lyr_capa = lyr_capa.datasetName
        arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)
        log.log(repet,u"Simbología de capa '{}' aplicada con la plantilla '{}'.".format(capa,simbologia))

    except Exception as e:
        log.log(repet,u">> ERROR, aplicar simbología falló para '{}' con '{}'".format(capa,simbologia))
        log.log(repet,str(e))

    tiempo_aplica_simb_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'aplica_simb': {}".format(tiempo.tiempo([tiempo_aplica_simb_ini,tiempo_aplica_simb_fin])))

    log.log(repet,u"'simbologia_lyr.aplica_simb' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1


def aplica_simb2(capa,lyr):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_aplica_simb2_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    try:
        log.log(repet,u"'simbologia_lyr.aplica_simb2' iniciando para '{}'...".format(capa))

        simbologia = "{}{}.lyr".format(arcpy.env.carp_simb,lyr)
        lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
        lyr_capa = lyr_capa.datasetName
        arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)
        log.log(repet,u"'simbologia_lyr.aplica_simb' en '{}' con '{}' finalizado!".format(capa,simbologia))

    except Exception as e:
        log.log(repet,u">> ERROR, aplicar simbología falló para '{}' con '{}'".format(capa,simbologia))
        log.log(repet,str(e))
    
    tiempo_aplica_simb2_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'aplica_simb2': {}".format(tiempo.tiempo([tiempo_aplica_simb2_ini,tiempo_aplica_simb2_fin])))

    log.log(repet,u"'simbologia_lyr.aplica_simb2' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1