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
    i=0

    for campo in camposCons:
        log.log(repet,u"campo: " + campo)
        log.log(repet,u"dAlter: " + dAlter[i])
        i+=1

    # rutina para generar identidad
    try:
        arch = (u"{}/{}".format(rutaCl,capaCl))
        capaidetidad = (u"{} identity".format(capa_salida))
        archtxt = (u"{}{} {}.txt".format(carpeta_proy, capaidetidad, arcpy.env.fechahora))

        with codecs.open(archtxt, 'w', encoding='utf-8') as archivo:
            archivo.write(u"Archivo de datos identity.\n")
            archivo.write(u"Archivo fuente: \n\n".format(arch))
            log.log(repet,u"El archivo '{}' ha sido creado con datos de '{}'".format(archtxt, arch))

        arcpy.env.overwriteOutput = True

        # #rutina para crear archivo de identidad
        
        capasalida = (u"{}{}.shp".format(arcpy.env.carp_temp,capaidetidad))
        log.log(repet,u"archivo para identidad: {}".format(arch))
        log.log(repet,u"archivo de salida: {}".format(capasalida))

        arcpy.Identity_analysis(in_features="SISTEMA",
            identity_features=arch,
            out_feature_class=capasalida,
            join_attributes="ALL",
            cluster_tolerance="",
            relationship="NO_RELATIONSHIPS")
        
        log.log(repet,u"Identidad creada con éxito: {}".format(capasalida))

        archivo = open(archtxt, 'a')
        log.log(repet,u"se abre el archivo")

        # Escribir los campos y sus valores si coinciden con la lista 'campos'
        for campo in camposCons:
            archivo.write(u"{}:\n".format(campo))
            cursor = arcpy.SearchCursor(capasalida, [campo])
            for row in cursor:
                campo_valor = row.getValue(campo)
                tipo_variable = type(campo_valor).__name__
                log.log(repet,u"'campo' es variable de tipo {}".format(tipo_variable))

                if isinstance(tipo_variable, unicode) or isinstance(tipo_variable, str):
                    log.log(repet,u"{}".format(campo_valor))
                    try:
                        archivo.write("{}\n".format(campo_valor))  # Escribe el campo con formato numérico en el archivo .txt
                    except Exception as e:
                        archivo.write("{}\n".format(campo_valor.encode('utf-8')))  # Escribir el contenido del campo de texto en el archivo .txt
                
                log.log(repet,u"se escribe el contenido del campo en archivo")
            del cursor
            archivo.write(u"\n")
            

        archivo.close()
        log.log(repet,u"se cierra el archivo")

        log.log(repet,u"'idproy.idproy' Se ha ejecutado satisfactoriamente para {}.".format(arch))

    except Exception as e:
        log.log(repet,u">> ERROR, no se ha podido ejecutar identity_sistema.py adecuadamente para {}".format(arch))
        log.log(repet,str(e))

    
    tiempo_iden_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_iden_ini,tiempo_iden_fin])))
    
    log.log(repet,u"'idproy.idproy' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
    
