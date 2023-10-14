# -*- coding: utf-8 -*-


import arcpy
import datetime
import codecs



def log(mensaje):
    if mensaje == None:
          mensaje =">>> Sin mensaje"
    archivo = arcpy.env.carp_cliente + "00 archivo_log.txt"
    fechahora = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

#     mensaje = mensaje.encode('utf-8')  # Codificar el mensaje en UTF-8
#     print(mensaje)  # Imprimir el mensaje decodificado en UTF-8

#     print(archivo)
#     print(fechahora)

    with codecs.open(archivo, "a", encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
            archivo.write(u"\n" + fechahora + u"\t" + mensaje)
            archivo.close()