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

log.log(u"Librería 'identity_sistema.py' cargado con éxito")

def idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter):

    tiempo_iden_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(u"'idproy.idproy' iniciando...")
    log.log(u"rutaCl: " + rutaCl)
    log.log(u"capaCl: " + capaCl)
    log.log(u"capa_salida: " + capa_salida)
    for campo in camposCons:
        log.log(u"campo: " + campo)
    for dato in dAlter:
        log.log(u"dAlter: " + dato)


    # rutina para generar identidad
    try:
        arch = ("{}/{}".format(rutaCl,capaCl))
        capaidetidad = ("{} identity".format(capa_salida))
        archtxt = ("{}{} {}.txt".format(arcpy.env.carp_cliente, capaidetidad, arcpy.env.fechahora))

        with codecs.open(archtxt, 'w', encoding='utf-8') as archivo:
            archivo.write('Archivo de datos identity.\n')
            archivo.write('Archivo fuente: ' + arch + "\n\n")
            log.log(u"El archivo '{}' ha sido creado con datos de '{}'".format(archtxt, arch))

        arcpy.env.overwriteOutput = True

        # #rutina para crear archivo de identidad
        
        capasalida = (u"Y:/0_SIG_PROCESO/X TEMPORAL/{}.shp".format(capaidetidad))
        log.log(u"archivo para identidad: {}".format(arch))
        log.log(u"archivo de salida: {}".format(capasalida))

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

        # i = 0

        # for nombre in nombres_de_campos:
        #     for cons in camposCons:
        #         if cons == nombre:
        #             capatr = arcpy.mapping.Layer(capa_salida) # Obtén una referencia a la capa "uso de suelo" en el mapa actual
        #             with arcpy.da.SearchCursor(capatr, nombre) as cursor: # Lee el primer registro
        #                 registro = next(cursor)
        #             valor_del_campo = registro[0] # El valor del campo "DESCRIP" del primer registro se encuentra en registro[0]
        #             if isinstance(valor_del_campo, int) or isinstance(valor_del_campo, float):
        #                 valor_del_campo = str(valor_del_campo)
        #                 if valor_del_campo is None or valor_del_campo == 0 or valor_del_campo == "0":
        #                     valor_del_campo = u"Sistema fuera de área de " + capa_salida
                    
        #             with codecs.open(archtxt, 'a', encoding='utf-8') as archivo:
        #                 archivo.write(nombre + chr(9) + dAlter[i] + chr(9) + valor_del_campo + "\n")
        #                 i = i + 1
        # # ccapas.remover_capas(capa_salida)

        log.log(u"'idproy.idproy' Se ha ejecutado satisfactoriamente para {}.".format(arch))

    except Exception as e:
        log.log(u">> ERROR, no se ha podido ejecutar identity_sistema.py adecuadamente para {}".format(arch))
        log.log(str(e))

    
    tiempo_iden_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_iden_ini,tiempo_iden_fin])))
    
    log.log(u"'idproy.idproy' finalizado!")
    
