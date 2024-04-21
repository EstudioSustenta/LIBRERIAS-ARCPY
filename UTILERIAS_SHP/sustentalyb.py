# -*- coding: utf-8 -*-

import arcpy
import os
import json
from itertools import islice
import codecs
import traceback
import time
from dbfread import DBF
import pandas as pd


def escribearch(cadena, modo, archlog):
    # -*- coding: utf-8 -*-
    with codecs.open(archlog, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena1 = u"\n{}\t{}".format(cadena,fecha_hora_actual)
        archivo_log.write(cadena1)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena1.encode('utf-8'))

# REGRESA EL VALOR DE CAMPO
def archjson(campo):
    # Ruta al archivo de texto
    ruta_json = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/DESCRIPTORES.json"     # este es el archivo que contiene las descripciones

    try:
        # escribearch(u"'archjson' iniciando... '{}'".format(campo),'a',archlog)  ---->>   NO ACTIVAR ESTA LÍNEA, HACE MUY LENTO EL CÓDIGO Y GENERA UN ARCHIVO LOG MUY GRANDE
        if (not os.path.exists(ruta_json)):
            raise Exception(u"EL ARCHIVO {} NO EXISTE.".format(ruta_json))

        # Leer datos desde el archivo JSON
        with open(ruta_json, 'r') as archivo: # , encoding='utf-8'
            datos_json = json.load(archivo)
        
        # escribearch(u"'archjson' terminado con éxito '{}'".format(campo),'a',archlog)  ---->>   NO ACTIVAR ESTA LÍNEA, HACE MUY LENTO EL CÓDIGO Y GENERA UN ARCHIVO LOG MUY GRANDE
        return datos_json[campo]

    except Exception as err:
        titsus = str(err)
        print(titsus)
        escribearch(u"ERROR RECUPERANDO VALOR DE '{}'".format(campo),'a',archlog)
        return u"---VERIFICAR---\n{}".format(titsus)


    # ---finaliza rutina para asignar una descripción al campo

def creacampo(valores):    

    archivo = valores['archivo1']
    camp = valores['campo']
    tipo = valores['tipo']
    precision = valores['precision']
    longit = valores['long']
    archlog = valores['archlog']

    escribearch(u"'creacampo' iniciando...",'a',archlog)

    if os.path.exists(archivo):
        escribearch(u"El archivo \n'{}' \nexiste".format(archivo),'a',archlog)

        camposs = [campo.name for campo in arcpy.ListFields(archivo)]

        print(">>>>>>>>>>>>")
        print(camposs)

        if camp in camposs:       # Verificar si el campo existe
            escribearch(u"El campo '{}' ya existe, no se creará".format(camp),'a',archlog)
            # None
        else:
            escribearch(u"El campo '{}' no existe, se creará".format(camp),'a',archlog)
            arcpy.AddField_management(in_table=archivo,
                                    field_name=camp,
                                    field_type=tipo,
                                    field_precision=precision,
                                    field_scale="",
                                    # field_length=longit,
                                    field_alias="",
                                    field_is_nullable="NULLABLE",
                                    field_is_required="NON_REQUIRED",
                                    field_domain="")
            escribearch(u"El campo '{}' se ha creado en {}".format(camp,archivo),'a',archlog)
    else:
        escribearch(u"El archivo: \n'{}' \n no existe".format(archivo),'a',archlog)
        # raise ValueError("Este es un mensaje de error.")
        
def calculacampo(valores):

    archlog = valores['archlog']
    archivo1 = valores['archivo1']
    campo = valores['campo']
    expresion = valores['expresion']
    tipoexp = valores['tipoexp']
    bloquecodigo = valores['bloquecodigo']  # esta variable está pendiente de usar

    escribearch(u"\nProceso de cálculo de campo iniciando...",'a', archlog)
    escribearch(u"\nvalores: archivo:{}, campo: {}, expresion:{}, tipo: {}, bloque: {}".format(archivo1,campo,expresion,tipoexp,bloquecodigo),'a', archlog)

    # arcpy.CalculateField_management(archivo, camp, expresion, "PYTHON")

    arcpy.CalculateField_management(in_table=archivo1,
                                field=campo,
                                expression=expresion,
                                expression_type=tipoexp
                                )

    escribearch(u"\nProceso de cálculo de campo terminado",'a', archlog)

def eliminar_archivo(archivoselim, archlog):
    escribearch(u"\nProceso eliminación de archivos iniciando...",'a',archlog)
    escribearch(u"\nArchivos a eliminar:\n{}".format(archivoselim),'a',archlog)
    try:
        for archivo in archivoselim:
                if os.path.exists(archivo):
                    os.remove(archivo)
                    escribearch(u"\nArchivo eliminado:\n{}".format(archivo),'a',archlog)
                else:
                    escribearch(u"\n{}\nno existe.".format(archivo),'a',archlog)
    except OSError as e:
        # print("Error al eliminar el archivo: {e}".format(archivo))
        escribearch(u"\nError al eliminar el archivo:\n{}\n{}".format(archivo,e),'a',archlog)

