# -*- coding: utf-8 -*-

# CÓDIGO PARA ESCRIBIR DATOS EN UN ARCHIVO
# SI EL ARCHIVO NO EXISTE LO CREA EN LA RUTA ESPECIFICADA E INSERTA UN ENCABEZADO
# SI YA EXISTE AGREGA LA INFORMACIÓN ESPECIFICADA Y LO CIERRA
# (la información debe de estar codificada en utf-8 para evitar problemas con acentos y caracteres especiales)

import arcpy
import datetime
import codecs
import os



def texto(archivo,titulo,campos,mensaje):

    try:
        if not os.path.exists(archivo):     #verifica que el archivo no existe
            # print ("Archivo NO existe")
            fechahora = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

            fichero = open(archivo, "w")
            fichero.write("{}\n".format(titulo))
            fichero.write("Proyecto:\t{}\n".format(arcpy.env.proyecto))
            fichero.write("Fecha y hora:\t{}\n".format(fechahora))
            fichero.write("Ruta de este archivo:\t{}\n".format(archivo))
            fichero.write("Cliente:\t{}\n\n".format(arcpy.env.cliente))
            fichero.write("{}\n".format(campos))
            fichero.write("{}\n".format(mensaje))
            fichero.close()
            # print ("Archivo escrito en {}".format(archivo))

        else:   # si ya existe, escribe el mensaje
            # print ("Archivo YA existe")
            fichero = open(archivo, "a")
            fichero.write("{}\n".format(mensaje))
            fichero.close()
        # print ("Archivo escrito en {}".format(archivo))
        
    except Exception as e:
        print ("Error {}\n escribiendo archivo \n{}".format(e, archivo))
