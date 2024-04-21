# -*- coding: utf-8 -*-

"""
Usar con Python 2.x
Utilerías miscelaneas para archivo
"""

import codecs
import os
import time
import shutil
# import sys
# import arcpy
import datetime


def escribearch(fichero, cadena):
    """
    Escribe a un archivo la cadena que se le envíe en modo
    
    """
    if os.path.exists(fichero):
        modo = 'a'
    else:
        modo = 'w'
    # -*- coding: utf-8 -*-
    with codecs.open(fichero, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena1 = u"\n{}\t{}".format(cadena,fecha_hora_actual)
        archivo_log.write(cadena1)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena1.encode('utf-8'))

def eliminar_carpeta(carpeta_a_eliminar):

    try:
        # Verificar si la carpeta existe antes de intentar eliminarla
        if os.path.exists(carpeta_a_eliminar):
            # Eliminar la carpeta y su contenido de manera recursiva
            shutil.rmtree(carpeta_a_eliminar)
            return u"La carpeta {}\ny su contenido han sido eliminados.".format(carpeta_a_eliminar)
        else:
            return u"La carpeta {}\nno existe.".format(carpeta_a_eliminar)
    except Exception as e:
        return str(e)

def copiar_carpeta(origen, destino):
    try:
        if os.path.exists(origen):
            shutil.copytree(origen, destino)
            return u'La carpeta se copió correctamente'
        else:
            return u'La carpeta origen no existe'
    except Exception as e:
        return str(e)
    
def copiar_archivo(origen, destino, sobreescr=False):
    try:
        if os.path.exists(origen):
            if sobreescr == False and os.path.exists(destino):
                return u'el archivo existe y no será sobreescrito (cambiar parámetro si se desea)'
            else:
                shutil.copy(origen, destino)
                return u'El archivo se copió correctamente'
        else:
            return u'El archivo origen no existe'
    except Exception as e:
        return str(e)

def listar_carpeta(carpeta):
    # Lista de carpetas en la carpeta principal
    archivos = [nombre for nombre in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, nombre))]
    return archivos

def obtener_subcarpetas(ruta_carpeta):
    """
    Obtiene una lista de subcarpetas en una carpeta dada.

    Parámetros:
    - ruta_carpeta (str): Ruta de la carpeta.

    Retorna:
    - Lista de subcarpetas.
    """
    subcarpetas = [nombre for nombre in os.listdir(ruta_carpeta) if os.path.isdir(os.path.join(ruta_carpeta, nombre))]
    return subcarpetas

def obtener_archivos_por_extension(ruta_carpeta, extension):
    """
    Obtiene una lista de archivos con una extensión específica en una carpeta.

    Parámetros:
    - ruta_carpeta (str): Ruta de la carpeta.
    - extension (str): Extensión de archivo a buscar.

    Retorna:
    - Lista de archivos con la extensión especificada.
    """
    archivos_con_extension = []
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(extension):
            archivos_con_extension.append(os.path.join(ruta_carpeta, archivo))
    return archivos_con_extension

def reporte_dbs():
    """
    Genera un reporte del contenido de las bases de datos de los estados
    returns: none
    """
    import ESUSTENTA_DB_2 as esdb
    


    carpeta = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/'
    archlog=u'{}001-2_reporte_de_registros.txt'.format(carpeta)

    escribearch1(fichero=archlog, cadena='Reporte de registros', presalto=0, postsalto=3, modo='w')
    subcarpetas = obtener_subcarpetas(carpeta)
    for subcarpeta in subcarpetas:
        estado = '{}{}/'.format(carpeta,subcarpeta)
        escribearch1(fichero=archlog, cadena =('=' * 60), presalto=1)
        escribearch1(fichero=archlog, cadena=estado.upper())
        subsubcarpetas = obtener_subcarpetas(estado)
        if 'tablas' in subsubcarpetas:
            ruta='{}tablas/'.format(estado)
            dbs= obtener_archivos_por_extension(ruta, 'db')
            escribearch1(fichero=archlog, cadena=ruta, tabuladores=1)
            escribearch1(fichero=archlog, cadena =('-' * 60), tabuladores=1)
            for db in dbs:
                tablas = esdb.obtener_tablas_sqlite(db)
                escribearch1(fichero=archlog, cadena=db, tabuladores=2)
                for tabla in tablas:
                    campos = '\tCampos: {}'.format(esdb.contar_campos_tabla(db, tabla))
                    registros = '\tRegistros: {}'.format(esdb.contar_reg_tabla(db, tabla))
                    escribearch1(fichero=archlog, cadena=tabla + campos + registros, tabuladores=3)
    escribearch1(fichero=archlog, cadena='Reporte de registros terminado para "{}"'.format(archlog), presalto=2, postsalto=3)

def listar_archivos(carpeta):
    archivos = []
    for archivo in os.listdir(carpeta):
        if os.path.isfile(os.path.join(carpeta, archivo)):
            archivos.append(archivo)
    return archivos

def listar_archivos_con_extension(carpeta):
    archivos = []
    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_completa):
            archivos.append(archivo)
    return archivos

def log(mensaje, archivo, imprimir=False, presalto=0, postsalto=0, tiempo=False, tabuladores=0, modo="a"):
    """
    Escribe a un archivo la cadena que se le envíe
    \n'presalto' es la cantidad de saltos de línea antes de la cadena
    \n'postsalto' es la cantidad de saltos de línea después de la cadena
    \n'tabuladores' es la cantidad de tabuladores antes de la cadena
    \n'modo' es el modo de escritura del archivo puede ser 'append' ('a') o 'write' ('w')
    \n'imprimir' modo para enviar la cadena formateada a la consola
    \n'tiempo' agrega una valor del tiempo al momento de realizar la impresión en archivo
    \nreturns: none
    """


    try:
        if tabuladores > 0:
            mensaje=('\t' * tabuladores) + mensaje
        if presalto > 0:
            mensaje=('\n' * presalto) + mensaje
        if tiempo == True:
            fechahora = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
            mensaje += '------>' + fechahora
        if postsalto > 0:
            mensaje+= ('\n' * postsalto)
        if imprimir == True:
            print(mensaje)
        
        if isinstance(mensaje, unicode):
             uni_verif = 0
        
        else:
             mensaje = unicode(mensaje, 'utf-8')

        if mensaje == None:
            mensaje =">>> Sin mensaje"
        

        with codecs.open(archivo, modo, encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
            archivo.write(u"\n{}".format(mensaje))
            archivo.close()
    except Exception as e:
        with codecs.open(archivo, modo, encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
                archivo.write(u">>ERROR escribiendo en archivo log: '{}'".format(e))
                archivo.close()

def escribevar(fichero, elementos):
    """
    Escribe a un archivo la cadena que se le envíe.
    Si los elementos son una lista, la escribe separada por saltos de página.
    Si la cadena es un diccionario, escribe la llave y el valor separados por un tabulador
    y cada binomio separado por un salto de página.
    parámetros:
    fichero: nombre del archivo a crear (ruta completa)
    elementos:  lista o diccionario de elementos a escribir
    returns: Cadena con el resultado de las operaciones.
    """

    with codecs.open(fichero, "w", encoding='utf-8') as archivo_log:
        if isinstance(elementos, list):
            for elemento in elementos:
                cadena = u"{}".format(elemento)
                if elemento!=elementos[-1]:
                    cadena += "\n"
                archivo_log.write(cadena)
        if isinstance(elementos, dict):
            numero=len(elementos)
            contador=0
            for elemento in elementos:
                cadena = u"{}\t{}".format(elemento,elementos[elemento])
                contador +=1
                if numero != contador:
                    cadena += "\n"
                archivo_log.write(cadena)
        archivo_log.close()
    if os.path.exists(fichero):
        mensaje=u"Archivo creado satisfactoriamente."
    else:
        mensaje=u"No se ha creado el archivo."
    return mensaje



if __name__ == '__main__':
    # fichero="Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/00 archivo_log_gus.txt"
    # # elementos=[1,2,3,4,5,6,"a","b","c"]
    # elementos={
    #     "uno":1,
    #     "dos":2,
    #     "tres":3,
    #     "cuatro":4,
    # }
    # print(escribevar(fichero, elementos))
    pass
