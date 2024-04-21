# -*- coding: utf-8 -*-

"""
Diccionarios con datos para cargar capas
"""

def caminos(dbasicos):
    datos={
        'mxd'           :   dbasicos['mxd'],
        'df'            :   dbasicos['df'],
        'shapefile'     :   dbasicos['rednalcaminos'],
        'layer'         :   dbasicos['rutasimbologia'] + 'Caminos_RNC.lyr',
        'nombreshape'   :   'Caminos',
        'transparencia' :   50,
        'campo_rotulos' :   "NOMBRE",
        }
    return datos

def estataldecreto(dbasicos):
    datos={
        'mxd'           :   dbasicos['mxd'],
        'df'            :   dbasicos['df'],
        'shapefile'     :   dbasicos['rutamapadigital'] + "GEOPOLITICOS/ESTATAL decr185.shp",
        'layer'         :   dbasicos['rutasimbologia'] + 'ESTATAL decr1851.lyr',
        'nombreshape'   :   'Estados',
        'transparencia' :   50,
        'campo_rotulos' :   "NOM_ENT",
        }
    return datos

def cuerposdeagua(dbasicos):

    datos={
        "mxd"           :   dbasicos['mxd'],
        "df"            :   dbasicos['df'],
        "shapefile"     :   dbasicos['rutamapadigital'] + "cuerpos de agua.shp",
        "nombreshape"   :   "Cuerpos de agua",
        "layer"         :   dbasicos['rutasimbologia'] + "Cuerpos de agua.lyr",
        "transparencia" :   50,
        "campo_rotulos" :   "NOMBRE",
        }
    return datos

def corrientesdeagua(dbasicos):

    datos={
        "mxd"           :   dbasicos['mxd'],
        "df"            :   dbasicos['df'],
        "shapefile"     :   dbasicos['rutamapadigital'] + "Corrientes de agua.shp",
        "nombreshape"   :   "Corrientes de agua",
        "layer"         :   dbasicos['rutasimbologia'] + "Corrientes de agua1.lyr",
        "transparencia" :   50,
        "campo_rotulos" :   "NOMBRE",
        }
    return datos

def subestacioneselec(dbasicos):

    datos={
        "mxd"           :   dbasicos['mxd'],
        "df"            :   dbasicos['df'],
        "shapefile"     :   dbasicos['rutamapadigital'] + "Subestacion electrica.shp",
        "nombreshape"   :   "Subestacion electrica",
        "layer"         :   dbasicos['rutasimbologia'] + "Subestacion electrica.lyr",
        "transparencia" :   50,
        "campo_rotulos" :   "NOMBRE",
        }
    return datos

def manzanas(dbasicos):

    datos={
        "mxd"           :   dbasicos['mxd'],
        "df"            :   dbasicos['df'],
        "shapefile"     :   "Sustituir este valor por la ruta real del archivo",
        "nombreshape"   :   "Manzanas",
        "layer"         :   dbasicos['rutasimbologia'] + "manzana_localidad.lyr",
        "transparencia" :   50,
        "campo_rotulos" :   "CVEGEO",
        }
    return datos

def rnc(dbasicos):

    datos={
        "mxd"           :   dbasicos['mxd'],
        "df"            :   dbasicos['df'],
        "shapefile"     :   dbasicos['rednalcaminos'],
        "nombreshape"   :   "Caminos R.N.",
        "layer"         :   dbasicos['rutasimbologia'] + "red nacional de caminos1.lyr",
        "transparencia" :   50,
        "campo_rotulos" :   "NOMBRE",
        }
    return datos



