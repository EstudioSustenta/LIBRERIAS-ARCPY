# -*- coding: utf-8 -*-

# FUNCIONES PARA ENCENDER O APAGAR UN GRUPO DETERMINADO
# SÍ FUNCIONA

import arcpy

print (u"control_de_grupo CARGADO EXITOSAMENTE")
#------------------------------FUNCIÓN PARA APAGAR UN GRUPO-----------------------
def apagagr(group_name):
    # Redefine el nombre con comillas
    #group_name = '"' + group_name + '"'
    print(u"APAGANDO GRUPO " + group_name)

    # Obtener el mapa actual
    mxd = arcpy.mapping.MapDocument(u"CURRENT")

    # Iterar a través de los data frames en el mapa
    for df in arcpy.mapping.ListDataFrames(mxd):
        # Iterar a través de las capas en el data frame
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if lyr.isGroupLayer and lyr.name == group_name:
                lyr.visible = False  # Apagar el grupo


#------------------------------FUNCIÓN PARA APAGAR UN GRUPO-----------------------

def enciendegr(group_name):
    # Redefine el nombre con comillas
    #group_name = '"' + group_name + '"'
    print(u"ENCENDIENDO GRUPO " + group_name)

    # Obtener el mapa actual
    mxd = arcpy.mapping.MapDocument(u"CURRENT")

    # Iterar a través de los data frames en el mapa
    for df in arcpy.mapping.ListDataFrames(mxd):
        # Iterar a través de las capas en el data frame
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if lyr.isGroupLayer and lyr.name == group_name:
                lyr.visible = True  # Encender el grupo
