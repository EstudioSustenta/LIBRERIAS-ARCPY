# -*- coding: utf-8 -*-

"""
Este programa debe ejecutarse con el interpretador de PYTHON 3.X
Contiene funciones de utilería que ayudan a los preliminares para calcular la marginación 
total por manzana.
Returns: None
"""
from estados import estadosact as estados_activos
from ESUSTENTA_DBF import escritura
from UTILERIAS_SHP_PY_3 import proyectashp
from UTILERIAS_SHP_PY_3 import mover_shp

estados = estados_activos()

for estado in estados:
    print (estado)
    # proyecta y copia archivo shapefile de scince a SIG INEGI
    # shp_in = 'C:/SCINCE 2020/32_ZAC/cartografia/manzana.shp'    # es importante verificar que el archivo a proyectar sea 'GCS_Mexico_ITRF2008'
    # shp_out = f'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad_1.shp'
    # proyectashp(shp_in, shp_out)
    # mover_shp(estado) # mueve archivos de la carpeta original a SIG

    escritura('Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/campos_estados1.txt', estado)

