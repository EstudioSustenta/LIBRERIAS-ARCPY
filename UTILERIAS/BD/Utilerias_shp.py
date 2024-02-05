# -*- coding: utf-8 -*-

"""
Este programa debe ejecutarse con el interpretador de PYTHON 2.7 de arcmap para que funcione
Contiene funciones de utilería para trabajar con archivos shp
Returns: None
"""

import os
import sys
sys.path.append('Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS')
from PROYECTAR_SHP_DE_SUBCARPETAS import obtener_codigo_epsg as epsg
from PROYECTAR_SHP_DE_SUBCARPETAS import proyectar_shapefile as proy
import arcpy


def existe(elemento):
    'verifica si la carpeta o el archivo existen fisicamente en disco'
    if os.path.exists(elemento):
        return True
    else:
        return False

def proyectar(fuente, destino, codepsg = 32613, sobreescribir = True):
    """
    Proyecta el un archivo fuente a un archivo destino con el 
    código epsg definido en el parámetro, el código epsg de salida
    siempres será 
    """
    codepsgdestino = codepsg      # Código EPSG = 32613 para WGS_1984_UTM_Zone_13N

    # obtiene la ruta del archivo destino
    dirdest = (os.path.dirname(destino))

    # verifica que exista la carpeta destino, de lo contrario la crea
    if not os.path.exists(dirdest):
        os.makedirs(dirdest)
        # print ('la carpeta no existe se ha creado')
    # else:
    #     print(u'la carpeta destino sí existe')

    # verifica que exista el archivo fuente, si existe, obtiene el código epsg del archivo
    # if existe(fuente) and not existe(destino): # si ya existe destino no se proyecta
    if existe(fuente):  #si ya existe el archivo destino lo proyecta sobreescribiéndolo
        # codepsgfuente = epsg(fuente)
        # print (codepsgfuente)
        if not os.path.exists(destino) and sobreescribir:
            proy(fuente,destino, codepsgdestino)
            if os.path.exists(destino) and epsg(destino) == codepsgdestino:
                return (u'el archvo se proyectó exitosamente')
            else:
                return (u'el archvo no pudo proyectarse')
        else:
            return (u'El shapefile destino ya existe, no se proyectó')
        
    else:
        return (u'no existe el archivo fuente')

def elimina_campos(archivo, campos):
    try:
        arcpy.DeleteField_management(archivo, campos)
        return True
    except:
        return False
