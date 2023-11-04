# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys
# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")

log.log(u"'quitar_registros.py' cargado con éxito")

def quitaregistros(capa, campoord):

    try:
        log.log(u"'quitar_registros.quitaregistros' iniciando para " + capa + u"...")
        # Ruta al shapefile o capa de interés
        capa = u"Cuerpoaguaintermitente"

        # Nombre del campo 'distancia'
        campoord = u"NEAR_DIST"

        # Crear una lista vacía para almacenar los valores de distancia
        cercanos = []

        # Utilizar SearchCursor para obtener los valores de 'distancia'
        with arcpy.da.SearchCursor(capa, [campoord]) as cursor:
            for row in cursor:
                distancia = row[0]
                cercanos.append(distancia)

        # Ordenar la lista de mayor a menor
        cercanos.sort(reverse=False)

        # Ahora, la lista 'cercanos' contiene los valores ordenados de mayor a menor
        for i in range(10):
            log.log(cercanos[i])
        log.log(u"'quitar_registros.quitaregistros' finalizado para " + capa)

    except Exception as e:
        log.log(u">> ERROR, el proceso 'quitar_registros.quitaregistros' falló para " + capa)
        log.log(str(e))

    log.log(u"'quitar_registros.quitaregistros' finalizado!")