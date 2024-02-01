# -*- coding: utf-8 -*-

"""
ESTE CÓDIGO ES EL ÚLTIMO PASO PARA AGREGAR INFORMACIÓN DE LA BASE DE DATOS DE LAS MANZANAS
AL ARCHIVO SHP. 
ESTE PROCESI FUE POSIBLE REALIZARLO ÚNICAMENTE MEDIANTE EL USO DE LA BIBLIOTECA 'GEOPANDAS'
LA CUAL CORRE ÚNICAMENTE EN PYTHON 3.X, POR LO QUE DEBE CORRERSE EN ESTA VERSIÓN
"""


import geopandas as gpd
from sqlalchemy import create_engine
import pandas as pd  # Agregado para importar pandas
import os



def shp(ruta_base_datos, ruta_shapefile):

    # Ruta de la base de datos SQLite
    tabla_migracion = 'marginacion'
    tabla_salud = 'cpv2020_manzana_servicios_de_salud'
    tabla_poblacion = 'cpv2020_manzana_poblacion'
    campo_clave= 'CVEGEO'

    # Conexión a la base de datos SQLite
    engine = create_engine(f'sqlite:///{ruta_base_datos}')

    consulta_sql_marginacion = f'SELECT * FROM {tabla_migracion}'     # Consulta SQL para seleccionar los datos de la tabla 'migracion'
    consulta_sql_salud = f'SELECT * FROM {tabla_salud}'     # Consulta SQL para seleccionar los datos de la tabla 'salud'
    consulta_sql_poblacion = f'SELECT * FROM {tabla_poblacion}'     # Consulta SQL para seleccionar los datos de la tabla 'salud'

    # Leer la tabla seleccionada en un DataFrame de Pandas
    df_marginacion = pd.read_sql_query(consulta_sql_marginacion, engine)
    df_salud = pd.read_sql_query(consulta_sql_salud, engine)
    df_poblacion = pd.read_sql_query(consulta_sql_poblacion, engine)

    # Lista de campos a agregar al GeoDataFrame
    campos_marginacion = ['CVEGEO',
                          'marg_viv', 
                          'marg_edu',
                          'marg_eco',
                          'marg_tot',
                          'marg_decil']
    campos_salud = ['CVEGEO',
                    'SALUD2_R']
    
    # usar 'campos_poblacion' cuando se inicie el proceso desde cero (ver proceso en obsidian)
    campos_poblacion = ['CVEGEO',
                        # 'area_has',
                        # 'dens_ha',
                        'POB1',
                        'POB42',
                        'POB84',
                        'POB130_es',
                        'POB131_es',
                        'POB132_es',
                        'POB133_es',
                        'POB134_es',
                        'POB135_es',
                        'POB136_es'
                        ]

    
    # usar 'campos_poblacion1' cuando se inicie el proceso con avance
    campos_poblacion1 = ['CVEGEO',
                        'POB1',
                        'POB42',
                        'POB84',
                        'POB130_es',
                        'POB131_es',
                        'POB132_es',
                        'POB133_es',
                        'POB134_es',
                        'POB135_es',
                        'POB136_es',
                        "POB2",
                        "POB4",
                        "POB5",
                        "POB7",
                        "POB9",
                        "POB13",
                        "POB30",
                        "POB31",
                        "POB32",
                        "POB33",
                        "POB34",
                        "POB35",
                        "POB36",
                        "POB16",
                        "POB37",
                        "POB38",
                        "POB39",
                        "POB40",
                        "POB41",
                        ]

    # Ruta del archivo shapefile existente

    # Cargar el GeoDataFrame existente desde el shapefile
    gdf_existente = gpd.read_file(ruta_shapefile)

    # usar campos_poblacion o campos_poblacion1 según el caso
    gdf_existente = gdf_existente.merge(df_poblacion[campos_poblacion], how='left', left_on=campo_clave, right_on=campo_clave)
    print('unión población hecha')
    gdf_existente = gdf_existente.merge(df_salud[campos_salud], how='left', left_on=campo_clave, right_on=campo_clave)
    print('unión salud hecha')
    gdf_existente = gdf_existente.merge(df_marginacion[campos_marginacion], how='left', left_on=campo_clave, right_on=campo_clave)
    print('unión marginación hecha')
    

    gdf_existente.rename(columns={'SALUD2_R': 'marg_sal'}, inplace=True)

    # # Guardar el GeoDataFrame actualizado en el mismo archivo shapefile
    gdf_existente.to_file(ruta_shapefile)
    print('unión consolidada en archivo')


def renombra_archivos(ruta_archivo_actual, nombre_nuevo):
    """
    Reemplaza el nombre del archivo definido en 'renombra_archivos'
    con el texto definido en 'nombre_nuevo'.
    Se separa la ruta y el nombre del archivo original sustituyéndolo
    por el nombre del nuevo archivo
    Returns: none
    """

    # Construir la ruta y nombre del archivo nuevo
    ruta_archivo_nuevo = os.path.join(os.path.dirname(ruta_archivo_actual), nombre_nuevo)

    # Renombrar el archivo
    os.rename(ruta_archivo_actual, ruta_archivo_nuevo)

    print(f'El archivo: \n{ruta_archivo_actual}\nha sido renombrado a: \n{ruta_archivo_nuevo}')
