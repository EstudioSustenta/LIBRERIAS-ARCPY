import geopandas as gpd
from pyproj import Proj, transform

import fiona
from pyproj import CRS

def obtener_codigo_epsg(shapefile_path):
    with fiona.open(shapefile_path) as src:
        # Obtener el sistema de referencia espacial (CRS) del shapefile
        crs = src.crs

        # Si es un diccionario, extraer el código EPSG
        if crs and 'init' in crs:
            crs_obj = CRS.from_string(crs['init'])
            return crs_obj.to_epsg()

    return None

# Reemplazar 'ruta/a/tu_shapefile.shp' con la ruta a tu propio shapefile
codigo_epsg = obtener_codigo_epsg('C:/SCINCE 2020/32_ZAC/cartografia/manzana.shp')
# codigo_epsg = obtener_codigo_epsg('Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia/manzana_localidad.shp')

if codigo_epsg:
    print(f'Código EPSG del shapefile: {codigo_epsg}')
else:
    print('No se pudo obtener el código EPSG del shapefile.')

