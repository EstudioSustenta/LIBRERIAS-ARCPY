# -*- coding: utf-8 -*-

# rutina para ajustar la escala de un mapa a para que se visualicen un número (ordinal) determinado de elementos de una lista de objetos a una distancia
# determinada almacenados en un archivo (archivo), extrayendo el valor de la columna (columna), entendiendo que el valor debe
# ser numérico y que representa la distancia en metros a la que se aplicará el ajuste de escala.

import arcpy
import sys
import importlib
import datetime

mxd = arcpy.env.mxd
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'extrae_dato' cargada con éxito")

def extraedato(archivo, ordinal, columna):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_extraedato_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"Proceso 'extraedato' iniciando para '{}'...".format(archivo))

    try:
    
        ordinal = str(ordinal) + "\t"

        # Abrir el archivo para lectura
        with open(archivo, 'r') as file:
            # Iterar a través de cada línea en el archivo
            for line in file:
                # Verificar si la línea comienza con el valor ordinal
                if line.startswith((ordinal)):
                    # Dividir la línea en columnas utilizando tabuladores como separadores
                    columns = line.split('\t')
                    
                    # Verificar si hay al menos tres columnas
                    if len(columns) >= columna:
                        # Extraer el valor de la tercera columna (índice 2)
                        log.log(repet,u"Ordinal = " + str(ordinal))
                        log.log(repet,u"Columna = " + str(columna))
                        distancia = int(columns[2].strip())  # strip() elimina espacios en blanco adicionales y saltos de línea
                        log.log(repet,u"distancia = " + str(distancia))

                        escala = (distancia * 2) / 20 * 100
                        z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
                        log.log(repet,u"escala = u" + str(escala))
                        df.scale = escala
        log.log(repet,u"Se han extraido los datos de '{}' correctamente".format(archivo))

    except Exception as e:
        log.log(repet,u">> ERROR. Se ha producido un error en el proceso de extracción de datos para el archivo '{}', ordinal '{}', columna '{}'".format(archivo, ordinal, columna))
        log.log(repet,str(e))

    tiempo_extraedato_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'extraedato': {}".format(tiempo.tiempo([tiempo_extraedato_ini,tiempo_extraedato_fin])))
    
    log.log(repet,u"Proceso 'extraedato' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
