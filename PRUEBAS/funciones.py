# -*- coding: utf-8 -*-

"""Este programa debe ejecutarse con el interpretador de PYTHON 3.X"""

import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS/BD"
sys.path.append(ruta_libreria)

from  ESUSTENTADB import calc_promedio
from  ESUSTENTADB import new_db_table
from  ESUSTENTADB import eliminar_tabla
from  ESUSTENTADB import calcula_inversos
from  ESUSTENTADB import margedu
from  ESUSTENTADB import margviv
from  ESUSTENTADB import margeco
from  ESUSTENTADB import margtot
from  ESUSTENTADB import crear_columna_deciles
from  ESUSTENTADB import crear_rangos_edad
from INTEGRADOR_EN_SHAPEFILE import shp


#Definición de variables
estados = [
        # u"Aguascalientes",
        # u"Baja California",
        # u"Baja California Sur",
        u"Campeche",
        # u"Chiapas",
        # u"Chihuahua",
        # u"Ciudad de Mexico",
        # u"Coahuila",
        # u"Colima",
        # u"Durango",
        # u"Guanajuato",
        # u"Guerrero",
        # u"Hidalgo",
        # u"Jalisco",
        # u"Mexico",
        # u"Michoacan de Ocampo",
        # u"Morelos",
        # u"Nayarit",
        # u"Nuevo Leon",
        # u"Oaxaca",
        # u"Puebla",
        # u"Queretaro",
        # u"Quintana Roo",
        # u"San Luis Potosi",
        # u"Sinaloa",
        # u"Sonora",
        # u"Tabasco",
        # u"Tamaulipas",
        # u"Tlaxcala",
        # u"Veracruz de Ignacio de la Llave",
        # u"Yucatan",
        # u"Zacatecas"
    ]
tabla = 'marginacion'
marg_param = {'tabla' : tabla}
sql_query = """
    CREATE TABLE {} AS
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
        cpv2020_manzana_poblacion poblacion
    JOIN
        cpv2020_manzana_caracteristicas_economicas economia ON poblacion.CVEGEO = economia.CVEGEO
    JOIN
        cpv2020_manzana_educacion educacion ON poblacion.CVEGEO = educacion.CVEGEO
    JOIN
        cpv2020_manzana_servicios_de_salud salud ON poblacion.CVEGEO = salud.CVEGEO
    JOIN
        cpv2020_manzana_vivienda vivienda ON poblacion.CVEGEO = vivienda.CVEGEO;
    """.format(tabla)
valores2 = {'campocalc' : ['EDU43_R', 'EDU46_R'],
                'tabla' : tabla
                }
tabla = 'marginacion'
# tabla = 'cpv2020_manzana_caracteristicas_economicas'
columnas_a_sumar = ['POB42', 'POB84']
nueva_columna = 'Gustavito'


#Proceso
for estado in estados:
        
    database_path = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_manzanas - copia.db'.format(estado,estado)
    ruta_shapefile = f"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad.shp"

    marg_param['database_path'] = database_path
    marg_param['nueva_columna_deciles'] = 'marg_decil'
    marg_param['columna_deciles'] = 'marg_tot'

    valores2['database_path'] = database_path

    # Calcula la marginación
    eliminar_tabla(database_path, tabla)
    new_db_table(database_path, sql_query)
    calcula_inversos(valores2)
    margedu(marg_param)
    margviv(marg_param)
    margeco(marg_param)
    margtot(marg_param)
    crear_columna_deciles(marg_param)

    # Crea rangos de edad
    crear_rangos_edad(database_path, 'cpv2020_manzana_poblacion', columnas_a_sumar, nueva_columna)

    # Actualiza el archivo shapefile con los datos de la base de datos
    shp(database_path, ruta_shapefile)





