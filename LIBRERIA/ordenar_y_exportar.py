# -*- coding: utf-8 -*-


import arcpy
import datetime
import codecs
import importlib
import sys
# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")

log.log(u"ordenar_y_exportar.py cargado con éxito")

# capa = u"Cuerpoaguaintermitente"
# campo = u"NEAR_DIST"
# camporef = u"NOMBRE"
# archivo = u"i.txt"
# cantidad = 20

def ordenayexporta(capa, campo, camporef, archivo, cantidad):

    try:
        log.log(u"'ordenar_y_exportar.ordenayexporta' iniciando...")

        # archivo = 'Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI/MEXICO GENERAL.txt'
        archivo = arcpy.env.carp_cliente + archivo + ".txt"

        # Crear una lista para almacenar las relaciones entre 'campo' y 'camporef'
        valores = []

        # Utilizar un cursor de búsqueda para recorrer los registros
        with arcpy.da.SearchCursor(capa, [campo, camporef]) as cursor:
            for row in cursor:
                valor_campo = row[0]
                valor_camporef = row[1]
                valores.append((valor_campo, valor_camporef))

        # Ordenar la lista de menor a mayor según el campo 'campo'
        valores.sort(key=lambda x: x[0])

        with codecs.open(archivo, 'w', encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
            archivo.write(u"Resultados de proceso de seleccion de registros en base a su valor de ordenamiento" + '\n')
            archivo.write(u"Proyecto: " + arcpy.env.proyecto + "\n")
            archivo.write(u"Capa de trabajo: " + capa + '\n')
            archivo.write(u"Campo de ordenamiento: " + campo + '\n')
            archivo.write(u"Campo anexo: " + camporef + '\n')
            archivo.write(u"Fecha: " + str((datetime.datetime.now()).date()) + ", Hora: " + str((datetime.datetime.now()).time()) + '\n\n')
            archivo.write(chr(9) + camporef + chr(9) + campo + chr(9) + "UNIDADES\n\n")

            # Imprimir los primeros 'cantidad' valores ordenados con sus valores 'camporef'
            for i in range(cantidad):
                linea = u"{n}{tab}{valor_camporef}{tab}{valor}{tab}metros".format(n=i+1, valor_camporef=valores[i][1], valor=int(valores[i][0]), tab=chr(9))
                archivo.write(linea + '\n')
            archivo.close()

    except Exception as e:
        log.log(u">> ERROR, el proceso ordenar y exportar falló")
        log.log(str(e))

    log.log(u"'ordenar_y_exportar.ordenayexporta' terminado")
