# -*- coding: utf-8 -*-

# SCRIPT PARA DAR formato AL MAPA
# DEBE EXISTIR UN FRAMEWORK LLAMADO 'Layers', TRES OBJETOS LLAMADOS 'TITULO', 'SUBTITULO' Y 'FECHA' PARA QUE FUNCIONE ADECUADAMENTE
# DEBE TEMBIÉN CONTENER UNA LEYENDA.
# ÉSTOS DEBERÁN ESTAR EN EL LAYOUT DE ARCMAP.

import arcpy
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'formato.py 'cargado con éxito")

mxd = arcpy.env.mxd

def formato_layout(subtitulo1):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_formato_layout_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:
        log.log(repet,u"'formato.formato_layout' iniciando ...")
        # Acceder a elementos de diseño por su nombre
        titulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"TITULO")[0]             #debe de existir el elemento de texto en layout llamado "TITULO"
        subtitulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"SUBTITULO")[0]       #debe de existir el elemento de texto en layout llamado "SUBTITULO"
        tfecha = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"FECHA")[0]              #debe de existir el elemento de texto en layout llamado "FECHA"
        leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", u"Legend")[0]          #debe de existir el elemento de leyenda en layout llamado "Legend"

        titulo.text = arcpy.env.proyecto        # Actualiza el título
        subtitulo.text = subtitulo1             # Actualiza el subtítulo
        tfecha.text = arcpy.env.fecha           # Actualiza la fecha
        leyenda.title = u"SIMBOLOGÍA"            # Asigna el rótulo a la simbología
        log.log(repet,u"Aplicación de formato para el layout en '{}' aplicada correctamente".format(subtitulo1))
    
    except Exception as e:
        log.log(repet,u">> ERROR, el proceso formato falló para {}".format(subtitulo1))
        log.log(repet,str(e))

    tiempo_formato_layout_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'formato_layout': {}".format(tiempo.tiempo([tiempo_formato_layout_ini,tiempo_formato_layout_fin])))

    log.log(repet,u"'formato.formato_layout' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
