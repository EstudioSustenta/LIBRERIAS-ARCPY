# -*- coding: utf-8 -*-

import arcpy
import sys
import importlib

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module(u"LIBRERIA.archivo_log")

log.log(u"Librería 'leyenda_ajuste' cargada con éxito")
# mxd = arcpy.mapping.MapDocument(u"CURRENT")
mxd = arcpy.env.mxd

def leyenda():
    log.log(u"'leyenda_ajuste' iniciando...")
    try:
            
        # Encuentra el cuadro de leyendas (legend) en el diseño
        for elemento in arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT"):
            cuadro_de_leyendas = elemento

        # Obtiene las coordenadas y el alto del cuadro de leyendas en el diseño
        x_leyenda = cuadro_de_leyendas.elementPositionX
        y_leyenda = cuadro_de_leyendas.elementPositionY
        alto_leyenda = cuadro_de_leyendas.elementHeight

        # Obtiene el alto del layout (página)
        alto_layout = mxd.pageSize.height

        nueva_altura = y_leyenda
        # Verifica si el cuadro de leyendas se sale del layout
        if y_leyenda + alto_leyenda > alto_layout:
            # Calcula la nueva altura para ajustar al alto del layout
            nueva_altura = alto_layout - 2.5 - y_leyenda

            # Establece la nueva altura para el cuadro de leyendas
            cuadro_de_leyendas.elementHeight = nueva_altura
            log.log(u"Se ha ajustado la leyenda a " + str(nueva_altura) + "cm")
        
        numero_de_elementos = len(cuadro_de_leyendas.items)

    except Exception as e:
        log.log(u">> ERROR, el proceso de ajuste de leyenda falló")
        log.log(str(e))
        
    log.log(u"'leyenda_ajuste' finalizado")


