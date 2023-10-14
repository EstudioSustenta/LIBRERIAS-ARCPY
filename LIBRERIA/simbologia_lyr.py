# -*- coding: utf-8 -*-

# SCRIPT PARA APLICAR SIMBOLOGÍA A UNA CAPA.
# PARTE DEL PRINCIPIO DE QUE EXISTE UNA CAPA DE SIMBOLOGÍA EN EL DIRECTORIO CORRESPONDIENTE
# CON UN ARCHIVO .lyr DEL MISMO NOMBRE QUE LA CAPA QUE SE ESTÁ CARGANDO. LA RUTA DEL ARCHIVO
# TAMBIÉN ES LA PREDEFINIDA: ("Y:\0_SIG_PROCESO\MAPAS\SIMBOLOGIA")

import arcpy
import importlib
import sys

mxd = arcpy.env.mxd
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"Proceso 'simbologia_lyr' cargado con éxito")


def aplica_simb(capa):

    log.log(u"'simbologia_lyr.aplica_simb' iniciando ...")

    simbologia = 'Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/' + capa + '.lyr'
    lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
    lyr_capa = lyr_capa.datasetName
    arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)
    print("Simbología de capa " + capa + " aplicada.")

    log.log(u"'simbologia_lyr.aplica_simb' finalizado")

def aplica_simb2(capa,lyr):

    log.log(u"'simbologia_lyr.aplica_simb2' iniciando ...")

    simbologia = 'Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/' + lyr + '.lyr'
    lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
    lyr_capa = lyr_capa.datasetName
    arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)

    log.log(u"'simbologia_lyr.aplica_simb2' finalizado")
