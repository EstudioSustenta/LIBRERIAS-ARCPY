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

def elimina_campos(archivo1, campos):
    """
    Elimina los campos de la lista 'campos' de un archivo shapefile 'archivo1'
    """
    try:
        arcpy.DeleteField_management(archivo1, campos)
        return True
    except:
        return False

def calcula_campo_shp(shape,campo,expresion,tipo):
    """
    Calcula el área y densidad de el shapefile 'shape' agregando el contenido
    en el campo 'campo' con la expresión 'expresion' del tipo 'tipo'
    se entiende que el tipo de expresiones puede ser 'PYTHON' o 'VB'
    """
    try:
        arcpy.AddField_management(in_table=shape, field_name=campo,field_type='FLOAT', field_precision="4")
        arcpy.CalculateField_management(in_table=shape,field=campo,expression=expresion,expression_type=tipo) # calcula el área
        arcpy.AddField_management(in_table=shape, field_name='densidad',field_type='FLOAT', field_precision="2")
        arcpy.CalculateField_management(in_table=shape,field='densidad',expression='[POB1] / [area_has]',expression_type='VB')     #Calcula la densidad

        return u'Campos "{}" y "densidad" creados y calculados'.format(campo)
    except Exception as e:
        return e

def borra_campos(shape, campos):
    """
    Elimina los campos suministrado en la lista 'campos' en el archivo 'shape'
    """
    try:
        # for campo in campos:
        arcpy.DeleteField_management(in_table=shape, drop_field=campos)
        return 'Campos eliminados de shapefile {}'.format(shape)
    except Exception as e:
        return e

def crea(shapeorig, destino, campos):
    """
    Esta función copia un archivo shapefile y borra los campos definidos en el parámetro 'campos'
    Esto se realiza para eliminar las columnas de la tabla que contienen palabras con acentos,
    puesto que no fue posible integrar columnas de texto con acentos a la base de datos y
    conservar el contenido del campo 'CVEGEO' con ceros iniciales.
    ejemplos de parámetros
    shapeorig = "C:/SCINCE 2020/01_AGS/cartografia/municipal.shp"
    campos = 'NOM_ENT;NOMGEO'
    return: estado del resultado del script
    """
    if not os.path.exists(destino) and os.path.exists(shapeorig):
        arcpy.CopyFeatures_management(in_features=shapeorig,
                                    out_feature_class=destino,
                                    config_keyword="",
                                    spatial_grid_1="0",
                                    spatial_grid_2="0",
                                    spatial_grid_3="0")
        arcpy.DeleteField_management(in_table=destino, drop_field=campos)
        if os.path.exists(destino):
            return '\n\n"{}" copiado satisfactoriamente'.format(destino)
        else:
            return '\n\n"===>> ERROR: {}" no se copió.'.format(destino)
    else:
        return '\n\n===>> ERROR: Origen no existe o destino ya existe'.format(destino)

def borrashp(shape):
    if os.path.exists(shape):
        arcpy.Delete_management(shape)
    # arcpy.DeleteFeatures_management(in_features=shape)
        if not os.path.exists(shape):
            return '\n\n"{}" borrado satisfactoriamente'.format(shape)
        else:
            return '\n\n"{}" no se pudo borrar'.format(shape)
    else:
        return '\n\n"{}" no existe en disco'.format(shape)

def elimina_shp(shape):
    try:
        if os.path.exists(shape):
            arcpy.DeleteFeatures_management(shape)
        else:
            return 'El archivo "{}" no existe en disco'.format(shape)
        if os.path.exists(shape):
            return 'No se ha podido eliminar el shapefile "{}"'.format(shape)
        else:
            return 'El shapefile "{}" ha sido eliminado de disco'.format(shape)
    except Exception as e:
        return '>>>>ERROR {}'.format(e)
    
if __name__ == '__main__':

    

    shape = "C:/SCINCE 2020/01_AGS/cartografia/municipal.shp"
    campos = 'NOM_ENT;NOMGEO'
            #   'NOM_MUN'

    # crea(shape, campos)    


