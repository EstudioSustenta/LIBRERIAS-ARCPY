# -*- coding: utf-8 -*-

# SCRIPT PARA DAR formato AL MAPA
# DEBE EXISTIR UN FRAMEWORK LLAMADO 'Layers', TRES OBJETOS LLAMADOS 'TITULO', 'SUBTITULO' Y 'FECHA' PARA QUE FUNCIONE ADECUADAMENTE
# DEBE TEMBIÉN CONTENER UNA LEYENDA.
# ÉSTOS DEBERÁN ESTAR EN EL LAYOUT DE ARCMAP.

import arcpy
import importlib
import sys
# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")

log.log(u"formato.py cargado con éxito")

mxd = arcpy.env.mxd

def formato_layout(subtitulo1):

    log.log(u"'formato.formato_layout' iniciando ...")
   
    
    try:
        # Acceder a elementos de diseño por su nombre
        titulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"TITULO")[0]             #debe de existir el elemento de texto en layout llamado "TITULO"
        subtitulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"SUBTITULO")[0]       #debe de existir el elemento de texto en layout llamado "SUBTITULO"
        tfecha = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"FECHA")[0]              #debe de existir el elemento de texto en layout llamado "FECHA"
        leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", u"Legend")[0]          #debe de existir el elemento de leyenda en layout llamado "Legend"

        titulo.text = arcpy.env.proyecto        # Actualiza el título
        subtitulo.text = subtitulo1             # Actualiza el subtítulo
        tfecha.text = arcpy.env.fecha           # Actualiza la fecha
        leyenda.title = u"SIMBOLOGÍA"            # Asigna el rótulo a la simbología
    
    except Exception as e:
        log.log(u">> ERROR, el proceso formato falló")
        log.log(str(e))

    log.log(u"'formato.formato_layout' terminado")