# -*- coding: utf-8 -*-

# ----HACER IDENTITY DEL SISTEMA CON CAPAS DEFINIDAS

import arcpy
# import os
import importlib
import sys
import codecs
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

mxd = arcpy.env.mxd
df = arcpy.env.df
arcpy.env.overwriteOutput = True

repet = arcpy.env.repet

log.log(repet,u"Librería 'identity_sistema.py' cargado con éxito")

def idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_iden_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(repet,u"'idproy.idproy' iniciando...")
    log.log(repet,u"rutaCl: " + rutaCl)
    log.log(repet,u"capaCl: " + capaCl)
    log.log(repet,u"capa_salida: " + capa_salida)
    for campo in camposCons:
        log.log(repet,u"campo: " + campo)
    for dato in dAlter:
        log.log(repet,u"dAlter: " + dato)


    # rutina para generar identidad
    try:
        arch = ("{}/{}".format(rutaCl,capaCl))
        capaidetidad = ("{} identity".format(capa_salida))
        archtxt = ("{}{} {}.txt".format(arcpy.env.carp_cliente, capaidetidad, arcpy.env.fechahora))

        with codecs.open(archtxt, 'w', encoding='utf-8') as archivo:
            archivo.write('Archivo de datos identity.\n')
            archivo.write('Archivo fuente: ' + arch + "\n\n")
            log.log(repet,u"El archivo '{}' ha sido creado con datos de '{}'".format(archtxt, arch))

        arcpy.env.overwriteOutput = True

        # #rutina para crear archivo de identidad
        
        capasalida = (u"Y:/0_SIG_PROCESO/X TEMPORAL/{}.shp".format(capaidetidad))
        log.log(repet,u"archivo para identidad: {}".format(arch))
        log.log(repet,u"archivo de salida: {}".format(capasalida))

        arcpy.Identity_analysis(in_features="SISTEMA",
            identity_features=arch,
            out_feature_class=capasalida,
            join_attributes="ALL",
            cluster_tolerance="",
            relationship="NO_RELATIONSHIPS")

        archivo = open(archtxt, 'a')

        # Escribir los campos y sus valores si coinciden con la lista 'campos'
        for campo in camposCons:
            archivo.write(campo + ":\n")
            cursor = arcpy.SearchCursor(capasalida, [campo])
            for row in cursor:
                archivo.write(str(row.getValue(campo)) + "\n")  # Escribir el contenido del campo en el archivo .txt
            del cursor
            archivo.write("\n")

        archivo.close()

        log.log(repet,u"'idproy.idproy' Se ha ejecutado satisfactoriamente para {}.".format(arch))

    except Exception as e:
        log.log(repet,u">> ERROR, no se ha podido ejecutar identity_sistema.py adecuadamente para {}".format(arch))
        log.log(repet,str(e))

    
    tiempo_iden_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_iden_ini,tiempo_iden_fin])))
    
    log.log(repet,u"'idproy.idproy' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
    
