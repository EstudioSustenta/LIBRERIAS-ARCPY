# -*- coding: utf-8 -*-

import arcpy

# Obtener acceso al documento actual
mxd = arcpy.mapping.MapDocument("CURRENT")

print ("ARCHIVO PARA CARGAR Y REMOVER CAPAS CARGADO CON ÉXITO")

def carga_capas(ruta_arch, nombre_capa):

    # EJEMPLO: Lista de nombres de capas a agregar
    #nombres_capas = ["emas01", "emas02"]

    # EJEMPLO: Ruta de la carpeta donde se encuentran las capas
    #ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/0 UBICACION"

    
    # mxd = arcpy.mapping.MapDocument("CURRENT")

    # Obtener el data frame por su nombre
    df = arcpy.mapping.ListDataFrames(mxd, "layers")[0]

    # Verificar si la capa ya está agregada al mapa
    capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)
    if not capa_existente:
        # Construir la ruta completa a la capa
        ruta_capa = ruta_arch + "/" + nombre_capa + ".shp"
        # Agregar la capa al data frame
        capa = arcpy.mapping.Layer(ruta_capa)
        arcpy.mapping.AddLayer(df, capa)

    # Actualizar la vista del mapa

def remover_capas(capa_remover):
    # mxd = arcpy.mapping.MapDocument("CURRENT")
    try:

        # Obtener el DataFrame activo
        df = arcpy.mapping.ListDataFrames(mxd)[0]

        capa = arcpy.mapping.ListLayers(mxd, capa_remover, df)[0]
        arcpy.mapping.RemoveLayer(df, capa)

        
        print(capa_remover + " removida exitosamente.")
    except Exception as e:
        print("Error:", str(e))