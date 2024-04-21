# -*- coding: utf-8 -*-


import arcpy
import datetime
import codecs



def log(repet,mensaje):

    try:
        caracter = "   "
        indentacion = caracter * repet
        uni_verif = ""

        if isinstance(mensaje, unicode):
             uni_verif = 0
        
        else:
             mensaje = unicode(mensaje, 'utf-8')

        if mensaje == None:
            mensaje =">>> Sin mensaje"
        archivo = arcpy.env.archivolog
        fechahora = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    #     mensaje = mensaje.encode('utf-8')  # Codificar el mensaje en UTF-8

        with codecs.open(archivo, "a", encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
                archivo.write(u"\n{}\t{}{}".format(fechahora,indentacion,mensaje))
                # if uni_verif != "":
                #      archivo.write(u"\n{}\t{} convertida a formato unicode".format(fechahora,mensaje))
                archivo.close()

    except Exception as e:
        with codecs.open(archivo, "a", encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
                archivo.write(u"\n{}\t{}>>ERROR escribiendo en archivo log: {}".format(fechahora,indentacion,mensaje))
                archivo.close()

if __name__ == '__main__':
    arcpy.env.archivolog = 'D:/PRUEBITA1.txt'
    log(2,'mensajé')
