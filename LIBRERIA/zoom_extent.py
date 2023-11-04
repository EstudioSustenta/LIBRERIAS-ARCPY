# -*- coding: utf-8 -*-



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

log.log(u"Librería 'zoom_extent.py' cargado con éxito")

def zoom_extent(layout_name, nombre_capa):

    tiempo_zoom_extent_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'zoom_extent.zoom_extent' iniciando para {}...".format(nombre_capa))

    try:

        # Obtener acceso a la capa "nombre_capa" por su nombre

        lyr_sistema = arcpy.mapping.ListLayers(mxd, nombre_capa)[0]

        # Obtener la extensión de la capa "nombre_capa"
        extent = lyr_sistema.getExtent()

        # Establecer la extensión de la vista de datos a la extensión de la capa "nombre_capa"
        df.extent = extent

        log.log(u"Se aplicó 'zoom extent' a la capa {}".format(nombre_capa))
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'zoom_extent'")
        log.log(str(e) + u"\n\n\n\n")

    tiempo_zoom_extent_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'zoom_extent': {}".format(tiempo.tiempo([tiempo_zoom_extent_ini,tiempo_zoom_extent_fin])))

    log.log(u"'zoom_extent.zoom_extent' finalizado!")

# ejemplo de uso: 
# zoom_extent(u"Layout", u"ESTATAL")
