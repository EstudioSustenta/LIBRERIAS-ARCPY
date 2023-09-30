# -*- coding: utf-8 -*-

import arcpy

def zoom_extent(layout_name, nombre_capa):
    # Obtener acceso al documento actual
    mxd = arcpy.env.mxd

    # Obtener acceso a la vista de datos activa
    df = arcpy.env.df

    # Obtener acceso a la capa "nombre_capa" por su nombre
    print(mxd)
    print(nombre_capa)
    import time
    time.sleep(10)
    lyr_sistema = arcpy.mapping.ListLayers(mxd, nombre_capa)[0]

    # Obtener la extensión de la capa "nombre_capa"
    extent = lyr_sistema.getExtent()

    # Establecer la extensión de la vista de datos a la extensión de la capa "nombre_capa"
    df.extent = extent
    
# ejemplo de uso: 
# zoom_extent("Layout", "ESTATAL")
