# -*- coding: utf-8 -*-

import geopandas as gpd
import os
from pyproj import Proj, transform

def proyectashp(shapefd, shapef0):
    # Rutas a tus archivos de entrada y salida

    # Definir sistemas de coordenadas de entrada y salida
    cgs = 'EPSG:4326'  # Sistema de coordenadas de salida (WGS 84)
    cgso = 6372         # sustituir None por el número CGS del shapefile origen
    if cgso:
        incgs = f'EPSG:{cgso}'  # Reemplaza 'XXXX' con el código EPSG de tu sistema de coordenadas de entrada

        # Leer el shapefile con geopandas
        gdf = gpd.read_file(shapefd)

        # Crear proyecciones utilizando pyproj
        proj_in = Proj(init=incgs)
        proj_out = Proj(init=cgs)

        # Aplicar la transformación de coordenadas a todos los puntos en el GeoDataFrame
        gdf['geometry'] = gdf['geometry'].apply(lambda geom: transform(proj_in, proj_out, geom) if geom else None)

        # Guardar el GeoDataFrame proyectado en un nuevo shapefile
        gdf.to_file(shapef0)

        print(f'Archivo \n{shapefd} proyectado en \{shapef0}')


def mover_shp(estado):

    carp_corr = {
        u'Aguascalientes' : '01_AGS',
        u'Baja California' : '02_BC',
        u'Baja California Sur' : '03_BCS',
        u'Campeche' : '',
        u'Chiapas' : '07_CHIS',
        u'Chihuahua' : '08_CHIH',
        u'Ciudad de Mexico' : '09_CDMX',
        u'Coahuila' : '05_COAH',
        u'Colima' : '06_COL',
        u'Durango' : '10_DGO',
        u'Guanajuato' : '11_GTO',
        u'Guerrero' : '12_GRO',
        u'Hidalgo' : '13_HGO',
        u'Jalisco' : '14_JAL',
        u'Mexico' : '15_MEX',
        u'Michoacan de Ocampo' : '16_MICH',
        u'Morelos' : '',
        u'Nayarit' : '',
        u'Nuevo Leon' : '19_NL',
        u'Oaxaca' : '',
        u'Puebla' : '',
        u'Queretaro' : '22_QRO',
        u'Quintana Roo' : '',
        u'San Luis Potosi' : '24_SLP',
        u'Sinaloa' : '',
        u'Sonora' : '',
        u'Tabasco' : '',
        u'Tamaulipas' : '',
        u'Tlaxcala' : '',
        u'Veracruz de Ignacio de la Llave' : '',
        u'Yucatan' : '',
        u'Zacatecas' : '32_ZAC'
        }
    
    # Rutas a tus archivos de entrada y salida
    ruta_shapefile_origen = f'C:/SCINCE 2020/{carp_corr[estado]}/cartografia/manzana_localidad.shp'
    ruta_shapefile_destino = f'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad.shp'
    ruta_destino = os.path.dirname(ruta_shapefile_destino) + '/'

    print(f'\narchivo origen:\n{ruta_shapefile_origen}\narchivo destino:\n{ruta_shapefile_destino}\n{ruta_destino}')

    if os.path.exists(ruta_shapefile_origen): # and os.path.exists(ruta_destino)
        

        # Leer el shapefile con geopandas
        print ('leyendo archivo')
        gdf = gpd.read_file(ruta_shapefile_origen)

        # verifica que no exista el archivo destino
        if os.path.exists(ruta_shapefile_destino):
            os.remove(ruta_shapefile_destino)
        else:
            print(f'el archivo \n{ruta_shapefile_destino}\nno existe')

        # Guardar el GeoDataFrame en la nueva ubicación
        print ('iniciando copia')
        gdf.to_file(ruta_shapefile_destino)
        print (f'{ruta_shapefile_destino}\ncreado exitosamente')

        # Opcional: Puedes eliminar el shapefile de la carpeta de origen si lo deseas
        os.remove(ruta_shapefile_origen)
        print(f'el archivo \n{ruta_shapefile_origen}\nse ha eliminado')
    else:
        print ('if NO ejecutado')
