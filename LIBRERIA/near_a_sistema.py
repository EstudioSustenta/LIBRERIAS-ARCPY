# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR EL PROCESO 'NEAR' EN UNA CAPA CON RELACIÓN A LA UBICACIÓN DEL SISTEMA
print ("libreria cargada")
import arcpy
import importlib
import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

elireg = importlib.import_module("LIBRERIA.elimina_registros")
ordexp = importlib.import_module("LIBRERIA.ordenar_y_exportar")
ccapas = importlib.import_module("LIBRERIA.cargar_capas")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
log = importlib.import_module("LIBRERIA.archivo_log")


# rutaorigen = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/"   --->RUTA DEL ARCHIVO ORIGEN
# capa = "Corrientes de agua"                                       --->NOMBRE DE LA CAPA A ANALIZAR
# distancia = 50                                                    --->DISTANCIA DEL RADIO DE BÚSQUEDA NEAR
# campo = "NEAR_DIST"                                               --->CAMPO DE DISTANCIA NEAR
# valor = -1                                                        --->VALOR QUE VA A ELIMINAR DEL CAMPO DE DISTANCIA NEAR
# camporef = "NOMBRE"                                               --->CAMPO DE REFERENCIA CON EL QUE CONSTRUYE LA TABLA DE DISTANCIAS (ARCHIVO DE TEXTO)
# archivo = capa + " near"                                          --->NOMBRE DEL ARCHIVO DE TEXTO, LA RUTA DEL ARCHIVO LA TOMA DE LA CARPETA DEL PROYECTO
# cantidad = 20                                                     --->CANTIDAD DE REGISTROS QUE SE INCLUYEN EN EL ARCHIVO DE DISTANCIAS

log.log(u"Proceso 'near_a_sistema' cargado con éxito")

def nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad):

    log.log(u"'near_a_sistema' iniciando...")
    arcpy.env.overwriteOutput = True

    try:
        # verifica si distancia es una cadena de texto
        if not isinstance(distancia, str):
            log.log(u"La variable no es de tipo string (cadena)")
            distancia = str(distancia) # si no es cadena, la convierte a cadena

        origen = rutaorigen + capa + ".shp"
        destino = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capa + ".shp"
        radio = distancia + " Kilometers"

        arcpy.CopyFeatures_management(in_features=origen,
            out_feature_class=destino,
            config_keyword="",
            spatial_grid_1="0",
            spatial_grid_2="0",
            spatial_grid_3="0")
        log.log("Proceso Copy realizado correctamente")
    except Exception as e:
        log.log("Error en proceso copy")
        log.log(str(e))

    try:
        arcpy.Near_analysis(in_features=capa,
            near_features="SISTEMA",
            search_radius=radio,
            location="NO_LOCATION",
            angle="NO_ANGLE",
            method="PLANAR")

        log.log("Proceso Near realizado correctamente")
    except Exception as e:
        log.log("Error en proceso near")
        log.log(str(e))
    
    try:
        elireg.eliminaregistros(capa, campo, valor)
        log.log("Registros eliminados satisfactoriamente")
    except Exception as e:
        log.log("Error en proceso para eliminar registros")
        log.log(str(e))
    try:
        reload(ordexp)
        ordexp.ordenayexporta(capa, campo, camporef, archivo, cantidad)
        log.log("Archivo exportado satisfactoriamente")
    except Exception as e:
        log.log("Error en proceso para exportar el archivo near")
        log.log(str(e))
    ccapas.remover_capas(capa)
    log.log(u"Proceso Near de " + capa + u" finalizado satisfactoriamente")