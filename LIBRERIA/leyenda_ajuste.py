# -*- coding: utf-8 -*-

import arcpy
import sys
import importlib
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'leyenda_ajuste' cargada con éxito")
# mxd = arcpy.mapping.MapDocument(u"CURRENT")
mxd = arcpy.env.mxd

def leyenda():

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_leyenda_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(repet,u"'leyenda' iniciando...")
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
        if y_leyenda + alto_leyenda > alto_layout - 2.5:
            # Calcula la nueva altura para ajustar al alto del layout
            nueva_altura = alto_layout - 2.5 - y_leyenda

            # Establece la nueva altura para el cuadro de leyendas
            cuadro_de_leyendas.elementHeight = nueva_altura
            log.log(repet,u"Se ha ajustado la leyenda a " + str(nueva_altura) + "cm")
        
        numero_de_elementos = len(cuadro_de_leyendas.items)

        log.log(repet,u"No se requiere ajuste de leyenda ")

    except Exception as e:
        log.log(repet,u">> ERROR, el proceso de ajuste de leyenda falló")
        log.log(repet,str(e))

    tiempo_leyenda_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'leyenda': {}".format(tiempo.tiempo([tiempo_leyenda_ini,tiempo_leyenda_fin])))

    log.log(repet,u"'leyenda' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1