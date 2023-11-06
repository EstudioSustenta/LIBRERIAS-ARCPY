# -*- coding: utf-8 -*-


import arcpy
import datetime
import codecs
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'ordenar_y_exportar.py' cargado con éxito")

# capa = u"Cuerpoaguaintermitente"
# campo = u"NEAR_DIST"
# camporef = u"NOMBRE"
# archivo = u"i.txt"
# cantidad = 20

def ordenayexporta(capa, campo, camporef, archivo, cantidad):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_ordenayexporta_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'ordenar_y_exportar.ordenayexporta' iniciando para {}...".format(archivo))

    try:

        import os
        # capa = "Y:/0_SIG_PROCESO/X TEMPORAL/near Cuerpos de agua.shp"
        ruta_capa = capa
        nombre_archivo = os.path.basename(ruta_capa)  # Obtener el nombre del archivo de la ruta
        layer = os.path.splitext(nombre_archivo)[0]  # Obtener el nombre sin la extensión
        layer = arcpy.mapping.Layer(ruta_capa).name  # Utiliza el nombre de la capa sin extensión si es necesario en tu código
        archivo = "{}{} {}.txt".format(arcpy.env.carp_cliente, layer, arcpy.env.fechahora)

        log.log(repet,u"capa: '{}', archivo de texto '{}', layer en mapa '{}'".format(capa, archivo, layer))

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
            archivo.write(u"Capa de trabajo: " + layer + '\n')
            archivo.write(u"Campo de ordenamiento: " + campo + '\n')
            archivo.write(u"Campo anexo: " + camporef + '\n')
            archivo.write(u"Fecha: " + str((datetime.datetime.now()).date()) + ", Hora: " + str((datetime.datetime.now()).time()) + '\n\n')
            archivo.write(chr(9) + camporef + chr(9) + campo + chr(9) + "UNIDADES\n\n")

            # Imprimir los primeros 'cantidad' valores ordenados con sus valores 'camporef'
            for i in range(cantidad):
                linea = u"{n}{tab}{valor_camporef}{tab}{valor}{tab}metros".format(n=i+1, valor_camporef=valores[i][1], valor=int(valores[i][0]), tab=chr(9))
                archivo.write(linea + '\n')
            archivo.close()
            log.log(repet,u"Archivo '{}' exportado satisfactoriamente".format(archivo))
    except Exception as e:
        log.log(repet,u">> ERROR, el proceso ordenar y exportar falló para '{}'".format(archivo))
        log.log(repet,str(e))
    
    tiempo_ordenayexporta_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'ordenayexporta': {}".format(tiempo.tiempo([tiempo_ordenayexporta_ini,tiempo_ordenayexporta_fin])))

    log.log(repet,u"'ordenar_y_exportar.ordenayexporta' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1