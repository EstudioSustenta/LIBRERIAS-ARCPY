# -*- coding: utf-8 -*-

"""
Usar con Python 2.x
Utilerías miscelaneas para archivo
"""

import codecs
import os
import time
import shutil
import sys


def escribearch(fichero, cadena):
    """
    Escribe a un archivo los la cadena que se le envíe en modo
    
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

def escribearch1(fichero, cadena, presalto=0, postsalto=0, tabuladores=0, modo='a', fechahora='n'):
    """
    Escribe a un archivo la cadena que se le envíe
    'presalto' es la cantidad de saltos de línea antes de la cadena
    'postsalto' es la cantidad de saltos de línea después de la cadena
    'tabuladores' es la cantidad de tabuladores antes de la cadena
    'modo' es el modo de escritura del archivo puede ser 'append' ('a') o 'write' ('w')
    returns: none
    
    """

    with codecs.open(fichero, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena1 = "\n{0}{1}{2}".format('\n' * presalto, '\t' * tabuladores, cadena)
        if fechahora == 's':
            cadena1 = cadena1 + ('\t{}'.format(fecha_hora_actual))
        cadena1 = cadena1 + ('\n' * postsalto)

        version_python = sys.version
        version_python = version_python.split(".")[0]
        if version_python == 2:
            archivo_log.write(cadena1.encode('utf-8'))
        else:
            archivo_log.write(cadena1)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena1.encode('utf-8'))

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


if __name__ == '__main__':
    fichero = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/PRUEBITA.txt'
    carpeta = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/'
    # escribearch1(fichero, 'INICIO', modo='w', presalto=1)
    # for n in range(1, 11):
        # cadena = u'Hola holita {}'.format(n)
        # escribearch1(fichero, cadena, presalto=0, postsalto=0, tabuladores=0)
    # escribearch1(fichero, 'FINAL')
    # reporte_dbs()

    # version_python = sys.version
    # version_python = version_python.split(".")[0]
    # print("La versión de Python es:", version_python)



