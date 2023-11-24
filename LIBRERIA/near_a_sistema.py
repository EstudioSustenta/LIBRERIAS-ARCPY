# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR EL PROCESO 'NEAR' EN UNA CAPA CON RELACIÓN A LA UBICACIÓN DEL SISTEMA
import arcpy
import importlib
import sys
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

elireg = importlib.import_module(u"LIBRERIA.elimina_registros")
ordexp = importlib.import_module(u"LIBRERIA.ordenar_y_exportar")
ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

# rutaorigen = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/"   --->RUTA DEL ARCHIVO ORIGEN
# capa = u"Corrientes de agua"                                       --->NOMBRE DE LA CAPA A ANALIZAR
# distancia = 50                                                    --->DISTANCIA DEL RADIO DE BÚSQUEDA NEAR
# campo = u"NEAR_DIST"                                               --->CAMPO DE DISTANCIA NEAR
# valor = -1                                                        --->VALOR QUE VA A ELIMINAR DEL CAMPO DE DISTANCIA NEAR
# camporef = u"NOMBRE"                                               --->CAMPO DE REFERENCIA CON EL QUE CONSTRUYE LA TABLA DE DISTANCIAS (ARCHIVO DE TEXTO)
# archivo = capa + " near"                                          --->NOMBRE DEL ARCHIVO DE TEXTO, LA RUTA DEL ARCHIVO LA TOMA DE LA CARPETA DEL PROYECTO
# cantidad = 20                                                     --->CANTIDAD DE REGISTROS QUE SE INCLUYEN EN EL ARCHIVO DE DISTANCIAS

repet = arcpy.env.repet

log.log(repet,u"Librería 'near_a_sistema' cargado con éxito")

def nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_nearproceso_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'nearproceso' iniciando...")
    arcpy.env.overwriteOutput = True

    try:
        # verifica si distancia es una cadena de texto
        if not isinstance(distancia, str):
            log.log(repet,u"La variable '{}' no es de tipo string (cadena)".format(str(distancia)))
            distancia = str(distancia) # si no es cadena, la convierte a cadena
            log.log(repet,u"La variable '{}' se ha convertido a cadena".format(str(distancia)))

        origen = rutaorigen + capa + u".shp"
        capadest = capa + u" near"
        destino = u"{}{}.shp".format(arcpy.env.carp_temp,capadest)
        radio = distancia + u" Kilometers"

        arcpy.CopyFeatures_management(in_features=origen,
            out_feature_class=destino,
            config_keyword="",
            spatial_grid_1="0",
            spatial_grid_2="0",
            spatial_grid_3="0")
        log.log(repet,u"Proceso Copy realizado correctamente para '{}' en '{}'".format(origen, destino))
    except Exception as e:
        log.log(repet,u"Error en proceso copy")
        log.log(repet,str(e))

    try:
        arcpy.Near_analysis(in_features=destino,
            near_features=u"SISTEMA",
            search_radius=u"",
            location=u"NO_LOCATION",
            angle=u"NO_ANGLE",
            method=u"PLANAR")

        log.log(repet,u"Proceso Near realizado correctamente para '{}' con un radio de '{}'".format(capadest, radio))
    except Exception as e:
        log.log(repet,u">> ERROR, no se ha ejecutado near para '{}' con un radio de '{}'".format(capadest, radio))
        log.log(repet,str(e))
    
    ordexp.ordenayexporta(destino, campo, camporef, archivo, cantidad)
    
    tiempo_nearproceso_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'nearproceso': {}".format(tiempo.tiempo([tiempo_nearproceso_ini,tiempo_nearproceso_fin])))

    log.log(repet,u"Proceso 'nearproceso' de " + capa + u" finalizado satisfactoriamente")

    arcpy.env.repet = arcpy.env.repet - 1
