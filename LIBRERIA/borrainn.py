# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS CON DATOS DE LA CONABIO
# RUTA DE LOS MAPAS:    Y:/GIS/MEXICO/VARIOS/conabio/WGS84

import arcpy
import importlib
import sys
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

mxd = arcpy.env.mxd
df = arcpy.env.df

arcpy.env.overwriteOutput = True

global tiempo

#------------------------------> CARGA DE LIBRERÍAS <------------------------------------------

log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")


#-----------------------------------------------------------------------------------------------
#------------------------------------> INICIO DE PROCESOS <-------------------------------------
#-----------------------------------------------------------------------------------------------

def borrainn():

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet
        
    try:

        log.log(repet,u"iniciando proceso de borrado capas innecesarias...")

        # elimina todas las capas, excepto "SISTEMA"

        capas_a_mantener = []

        # Iterar a través de todas las capas en el DataFrame
        for lyr in arcpy.mapping.ListLayers(mxd, u"", df):
            # Verificar si el nombre de la capa es "SISTEMA"
            if lyr.name == "SISTEMA":
                capas_a_mantener.append(lyr)  # Agregar la capa a la lista de capas a mantener

        # Eliminar todas las capas del DataFrame
        for lyr in arcpy.mapping.ListLayers(mxd, u"", df):
            if lyr not in capas_a_mantener:
                arcpy.mapping.RemoveLayer(df, lyr)
                log.log(repet,u"Removiendo capa " + str(lyr))

        # Actualizar el contenido del DataFrame
        arcpy.RefreshTOC()
        log.log(repet,u"Proceso de borrado capas innecesarias finalizado! \n\n")
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'borrainn'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn()

    arcpy.env.repet = arcpy.env.repet - 1