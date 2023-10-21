# -*- coding: utf-8 -*-

# rutina para ajustar la escala de un mapa a para que se visualicen un número (ordinal) determinado de elementos de una lista de objetos a una distancia
# determinada almacenados en un archivo (archivo), extrayendo el valor de la columna (columna), entendiendo que el valor debe
# ser numérico y que representa la distancia en metros a la que se aplicará el ajuste de escala.

import arcpy
import sys
import importlib

# Agrega la ruta del paquete al path de Python

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
print(ruta_libreria)
sys.path.append(ruta_libreria)

z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")
log = importlib.import_module(u"LIBRERIA.archivo_log")


log.log(u"Librería 'extrae_dato' cargada con éxito")
def extraedato(archivo, ordinal, columna):

    log.log(u"Proceso 'extraedato' iniciando...")
    
    mxd = arcpy.mapping.MapDocument(u"CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    ordinal = str(ordinal) + "\t"

    # Abrir el archivo para lectura
    with open(archivo, 'r') as file:
        # Iterar a través de cada línea en el archivo
        for line in file:
            # Verificar si la línea comienza con '4'
            if line.startswith((ordinal)):
                # Dividir la línea en columnas utilizando tabuladores como separadores
                columns = line.split('\t')
                
                # Verificar si hay al menos tres columnas
                if len(columns) >= columna:
                    # Extraer el valor de la tercera columna (índice 2)
                    log.log(u"Ordinal = u" + str(ordinal))
                    log.log(u"Columna = u" + str(columna))
                    distancia = int(columns[2].strip())  # strip() elimina espacios en blanco adicionales y saltos de línea
                    log.log(u"distancia = u" + str(distancia))

                    escala = (distancia * 2) / 20 * 100
                    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
                    log.log(u"escala = u" + str(escala))
                    df.scale = escala
                    arcpy.RefreshActiveView()
    log.log(u"Proceso 'extraedato' finalizado!")