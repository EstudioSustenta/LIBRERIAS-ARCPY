# -*- coding: utf-8 -*-

# SCRIPT PARA exportar_mapas A LA CARPETA POR DEFAULT
# TOMA COMO REFERENCIA LA r_dest DEFINIDA COMO VARIABLE EN LA FUNCIÓN
# GENERA DOS MAPAS CON EL NOMBRE DEL PROYECTO Y LA ESPECIALIDAD.

import arcpy
import importlib
import sys

mxd = arcpy.env.mxd

ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
renombra = importlib.import_module("LIBRERIA.renombrar_capa")
log = importlib.import_module("LIBRERIA.archivo_log")
leyenda = importlib.import_module("LIBRERIA.leyenda_ajuste")

log.log(u"Librería 'exportar_mapas' cargada con éxito")

def exportar(r_dest):
    log.log(u"'exportar_mapas' iniciando ...")

    # Proceso de ajuste de leyenda
    for elemento in arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT"):
        cuadro_de_leyendas = elemento
    alto_leyenda_orig = cuadro_de_leyendas.elementHeight
    leyenda.leyenda()
    
    arcpy.env.overwriteOutput = True  # Permitir sobrescribir archivos de salida
    renombra.renomb("SISTEMA", arcpy.env.proyecto)
    arcpy.RefreshActiveView()  # Actualizar la vista
    # r_dest = r_dest('utf-8')
    r_dest_utf8 = r_dest.encode('utf-8')
    
    try:
        # arcpy.mapping.ExportToJPEG(mxd, r_dest_utf8 + ".jpg", "page_layout", 1024, 768, 250)  # Exportar a JPEG
        arcpy.mapping.ExportToPDF(mxd, r_dest_utf8 + ".pdf", "page_layout", 1024, 768, 350)  # Exportar a PDF
        log.log(u"archivo .pdf exportado con éxito")
    except Exception as e:
        log.log(u">> ERROR. Se ha producido un error en el proceso de exportacion")
        log.log(str(e))
        
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    cuadro_de_leyendas.elementHeight = alto_leyenda_orig
    log.log(u"'exportar_mapas' terminado")
