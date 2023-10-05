# -*- coding: utf-8 -*-


import arcpy
import datetime
import codecs

# capa = "Cuerpoaguaintermitente"
# campo = "NEAR_DIST"
# camporef = "NOMBRE"
# archivo = "i.txt"
# cantidad = 20

def ordenayexporta(capa, campo, camporef, archivo, cantidad):

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
        archivo.write("Resultados de proceso de seleccion de registros en base a su valor de ordenamiento" + '\n')
        archivo.write("Proyecto: " + arcpy.env.proyecto + "\n")
        archivo.write("Capa de trabajo: " + capa + '\n')
        archivo.write("Campo de ordenamiento: " + campo + '\n')
        archivo.write("Campo anexo: " + camporef + '\n')
        archivo.write("Fecha: " + str((datetime.datetime.now()).date()) + ", Hora: " + str((datetime.datetime.now()).time()) + '\n\n')
        archivo.write(chr(9) + camporef + chr(9) + campo + chr(9) + "UNIDADES\n\n")

        # Imprimir los primeros 'cantidad' valores ordenados con sus valores 'camporef'
        for i in range(cantidad):
            linea = "{n}{tab}{valor_camporef}{tab}{valor}{tab}metros".format(n=i+1, valor_camporef=valores[i][1], valor=int(valores[i][0]), tab=chr(9))
            print(linea)
            archivo.write(linea + '\n')
        archivo.close()