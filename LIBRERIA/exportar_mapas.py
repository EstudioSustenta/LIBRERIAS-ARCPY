# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys
import re
import unicodedata
# import unicode
import datetime

mxd = arcpy.env.mxd

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")
log = importlib.import_module(u"LIBRERIA.archivo_log")
leyenda = importlib.import_module(u"LIBRERIA.leyenda_ajuste")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'exportar_mapas' cargada con éxito")



# cadena_sin_acentos = None  # Declarar cadena_sin_acentos como variable global

def quitar_acentos(texto):

    tiempo_quita_acentos_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'quitar_acentos' iniciando para {} de tipo {}...".format(texto,type(texto)))

    try:
        # unicode_texto = unicode(texto, "utf-8")  # Convierte a Unicode
        # nfkd_form = unicodedata.normalize('NFKD', unicode_texto)
        nfkd_form = unicodedata.normalize('NFKD', texto)
        cadena_sin_acentos = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        # return cadena_sin_acentos

        arcpy.env.sinacentos = cadena_sin_acentos

        if texto == cadena_sin_acentos:
            log.log(u"{} no contiene acentos, no se han hecho cambios".format(texto))
        else:
            log.log(u"se ha aplicado el proceso 'quitar_acentos' para '{}' cambiado a '{}'".format(texto, cadena_sin_acentos))
    except Exception as e:
        log.log(u">> ERROR. Se ha producido un error en el proceso de sustitución de acentos")
        log.log(str(e))

    tiempo_quita_acentos_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'quitar_acentos': {}".format(tiempo.tiempo([tiempo_quita_acentos_ini,tiempo_quita_acentos_fin])))

    log.log(u"'quitar_acentos' finalizado para {}...".format(texto))

def exportar(r_dest, nombarch):

    tiempo_exportar_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    ruta = ""  # Inicializar ruta con una cadena vacía
    try:
        log.log(u"'exportar_mapas' iniciando para {}, donde 'nombarch' es tipo {}...".format(r_dest + nombarch,"type(nombarch)"))
        

        quitar_acentos(nombarch)

        ruta = r_dest + arcpy.env.sinacentos

        # Proceso de ajuste de leyenda
        for elemento in arcpy.mapping.ListLayoutElements(mxd, u"LEGEND_ELEMENT"):
            cuadro_de_leyendas = elemento
        alto_leyenda_orig = cuadro_de_leyendas.elementHeight
        leyenda.leyenda()
        
        arcpy.env.overwriteOutput = True  # Permitir sobrescribir archivos de salida

        renombra.renomb(u"SISTEMA", arcpy.env.proyecto)
        
        # ruta = (ruta.encode('utf-8') + ".pdf").decode('utf-8')
        ruta = ruta + ".pdf"
        log.log(u"Archivo codificado: {}".format(ruta))
        
        arcpy.RefreshActiveView()  # Actualizar la vista
        # arcpy.mapping.ExportToJPEG(mxd, ruta + ".jpg", u"page_layout", 1024, 768, 250)  # Exportar a JPEG
        arcpy.mapping.ExportToPDF(mxd, ruta, "page_layout", 1024, 768, 350)  # Exportar a PDF
        cuadro_de_leyendas.elementHeight = alto_leyenda_orig
        renombra.renomb(arcpy.env.proyecto, "SISTEMA")

        log.log(u"archivo {}.pdf exportado con éxito".format(arcpy.env.sinacentos))

    except Exception as e:
        log.log(u">> ERROR. Se ha producido un error en el proceso de exportación del archivo '{}'".format(ruta))
        log.log(str(e))

    tiempo_exportar_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'exportar': {}".format(tiempo.tiempo([tiempo_exportar_ini,tiempo_exportar_fin])))    
    
    log.log(u"'exportar_mapas' para '{}' finalizado!".format(ruta))
