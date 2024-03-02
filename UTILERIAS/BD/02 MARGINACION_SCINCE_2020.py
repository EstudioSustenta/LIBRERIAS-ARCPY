# -*- coding: utf-8 -*-

"""
Este programa debe ejecutarse con el interpretador de PYTHON 3.X
contiene funciones que calculan la marginación por manzana.
Returns: None

CUIDADO!!!
ESTA FUNCIÓN TIENE UN ERROR EN LA GENERACIÓN DE MARGINACIÓN PARA LOS ESTADOS.
NO MANEJA ADECUADAMENTE LOS ACENTOS EN EL NOMBRE DEL ESTADO
MODIFICARLA PARA QUE ELIMINE EL CAMPO DEL NOMBRE DE LA ENTIDAD
EL MOMENTO DE REALIZAR EL COPIADO DE LA INFORMACIÓN A LAS BASES
DE DATOS DE CADA ESTADO (VER REPORTE DE EXCEL "registro de incidencias 01.xlsx")
"""

import sys
from ESUSTENTA_DB import calc_promedio
from ESUSTENTA_DB import marg_base_table
from ESUSTENTA_DB import eliminar_tabla
from ESUSTENTA_DB import calcula_inversos
from ESUSTENTA_DB import margedu
from ESUSTENTA_DB import margviv
from ESUSTENTA_DB import margeco
from ESUSTENTA_DB import margtot
from ESUSTENTA_DB import marg_deciles
from ESUSTENTA_DB import rangos_edad
from INTEGRADOR_EN_SHAPEFILE import shp
from estados import estados as estados_activos
from estados import shapes
from ESUSTENTA_UTILERIAS import escribearch1 as ESU

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS/BD"
sys.path.append(ruta_libreria)
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS"
sys.path.append(ruta_libreria)


#Definición de variables
estados = estados_activos()
tabla_elim = 'marginacion'
tabla = 'marginacion'
marg_param = {'tabla' : tabla}
sql_query = f"""
    CREATE TABLE {tabla} AS
    SELECT
        poblacion.CVEGEO,
        poblacion.POB1,
        poblacion.POB42,
        poblacion.POB84,
        economia.ECO1_R,
        economia.ECO2_R,
        economia.ECO3_R,
        economia.ECO25_R,
        economia.ECO26_R,
        economia.ECO27_R,
        salud.SALUD2_R,
        vivienda.VIV0,
        vivienda.VIV7_R,
        vivienda.VIV10_R,
        vivienda.VIV14_R,
        vivienda.VIV16_R,
        vivienda.VIV18_R,
        vivienda.VIV21_R,
        vivienda.VIV24_R,
        vivienda.VIV26_R,
        vivienda.VIV30_R,
        vivienda.VIV31_R,
        vivienda.VIV39_R,
        vivienda.VIV40_R,
        vivienda.VIV41_R,
        vivienda.VIV42_R,
        educacion.EDU28_R,
        educacion.EDU43_R,
        educacion.EDU46_R
    FROM
        poblacion poblacion
    JOIN
        economia economia ON poblacion.CVEGEO = economia.CVEGEO
    JOIN
        educacion educacion ON poblacion.CVEGEO = educacion.CVEGEO
    JOIN
        salud salud ON poblacion.CVEGEO = salud.CVEGEO
    JOIN
        vivienda vivienda ON poblacion.CVEGEO = vivienda.CVEGEO;
    """
valores2 = {'campocalc' : ['EDU43_R', 'EDU46_R'],
                'tabla' : tabla
                }
tabla = 'marginacion'
shapes = shapes()
grupos_geom = [
          'estatal',
          'municipal',
          'loc_urb',
          'loc_rur',
          'ageb_urb',
          'manzana',
          ]

#Proceso
def inicio_proc():
    rutabase = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/'
    archlog = f'{rutabase}002_log_marginacion.txt'
    
    ESU(archlog, """
    Reporte LOG de incidencias en proceso de cálculo de la marginación para productos SCINCE 2020
    Autor: Gustavo Martinez Velasco

    """, modo='w')
    
    for estado in estados:
        ESU(archlog, f'\n>>>>>>>>>>>>  Iniciando proceso para {estado}\n')
        for grupo in shapes:
            if grupo in grupos_geom:
                if grupo == 'manzana':
                    shape = 'manzana_localidad'
                else:
                    shape = grupo
                database_path = f'{rutabase}{estado}/tablas/{grupo}.db'
                ruta_shapefile = f"{rutabase}{estado}/cartografia/{shape}.shp"
                marg_param['database_path'] = database_path
                marg_param['nueva_columna_deciles'] = 'marg_decil'
                marg_param['columna_deciles'] = 'marg_tot'
                valores2['database_path'] = database_path


                # Calcula la marginación
                ESU(archlog, eliminar_tabla(database_path, tabla_elim))   # Elimina la tabla marginación si existe en la base de datos, para contar con información reciente
                ESU(archlog, marg_base_table(database_path, sql_query))   # Crea una tabla llamada 'marginacion' importado datos de otras tablas usando una consulta sql
                ESU(archlog, calcula_inversos(valores2))  # Calcula los inversos de los parámetros de educación
                ESU(archlog, margedu(marg_param))     # Calcula la marginación de educación
                ESU(archlog, margviv(marg_param))     # Calcula la marginación de vivienda
                ESU(archlog, margeco(marg_param))     # Calcula la marginación de características económicas
                ESU(archlog, margtot(marg_param))     # Calcula la marginación total
                ESU(archlog, marg_deciles(marg_param))    # Calcula los deciles para la marginación

                # Crea rangos de edad
                ESU(archlog, rangos_edad(database_path, 'poblacion'))

                # Actualiza el archivo shapefile con los datos de la base de datos
                ESU(archlog, ruta_shapefile)
                ESU(archlog, shp(database_path, ruta_shapefile))
                ESU(archlog, f'Proceso terminado para -{grupo}-')
        ESU(archlog, f'\nproceso terminado para -{estado}-   >>>>>>>>>>>>\n')

    ESU(archlog, '\n\nproceso terminado exitosamente   >>>>>>>>>>>>>>>>>>>>>>>\n\n')


inicio_proc()