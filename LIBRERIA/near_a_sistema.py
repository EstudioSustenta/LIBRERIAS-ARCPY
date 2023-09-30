# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR EL PROCESO 'NEAR' EN UNA CAPA CON RELACIÓN A LA UBICACIÓN DEL SISTEMA
print ("libreria cargada")
import arcpy
import datetime
import importlib
import sys

# Agrega la ruta del paquete al path de Python
# ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
# sys.path.append(ruta_libreria)

elireg = importlib.import_module("LIBRERIA.elimina_registros")
reload(elireg)
ordexp = importlib.import_module("LIBRERIA.ordenar_y_exportar")
ccapas = importlib.import_module("LIBRERIA.cargar_capas")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)

# rutaorigen = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/"   --->RUTA DEL ARCHIVO ORIGEN
# capa = "Corrientes de agua"                                       --->NOMBRE DE LA CAPA A ANALIZAR
# distancia = 50                                                    --->DISTANCIA DEL RADIO DE BÚSQUEDA NEAR
# campo = "NEAR_DIST"                                               --->CAMPO DE DISTANCIA NEAR
# valor = -1                                                        --->VALOR QUE VA A ELIMINAR DEL CAMPO DE DISTANCIA NEAR
# camporef = "NOMBRE"                                               --->CAMPO DE REFERENCIA CON EL QUE CONSTRUYE LA TABLA DE DISTANCIAS (ARCHIVO DE TEXTO)
# archivo = capa + " near"                                          --->NOMBRE DEL ARCHIVO DE TEXTO, LA RUTA DEL ARCHIVO LA TOMA DE LA CARPETA DEL PROYECTO
# cantidad = 20                                                     --->CANTIDAD DE REGISTROS QUE SE INCLUYEN EN EL ARCHIVO DE DISTANCIAS

def nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad):
    
    arcpy.env.overwriteOutput = True

    try:
        # verifica si distancia es una cadena de texto
        if not isinstance(distancia, str):
            print("La variable no es de tipo string (cadena)")
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
        print ("Proceso Copy realizado correctamente")
    except:
        print ("Error en proceso copy")

    try:
        arcpy.Near_analysis(in_features=capa,
            near_features="SISTEMA",
            search_radius=radio,
            location="NO_LOCATION",
            angle="NO_ANGLE",
            method="PLANAR")

        print ("Proceso Near realizado correctamente")
    except:
        print ("Error en proceso near")
    
    try:
        elireg.eliminaregistros(capa, campo, valor)
        print("Registros eliminados satisfactoriamente")
    except:
        print("Error en proceso para eliminar registros")
    try:
        reload(ordexp)
        ordexp.ordenayexporta(capa, campo, camporef, archivo, cantidad)
        print("Archivo exportado satisfactoriamente")
    except:
        print("Error en proceso para exportar el archivo near")
    ccapas.remover_capas(capa)
    print("Proceso Near de " + capa + " finalizado satisfactoriamente")