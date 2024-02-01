# -*- coding: utf-8 -*-

"""
Este programa debe ejecutarse con el interpretador de PYTHON 3.X
contiene funciones que calculan la marginación por manzana.
Returns: None
"""

import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS/BD"
sys.path.append(ruta_libreria)
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS"
sys.path.append(ruta_libreria)

from ESUSTENTADB import calc_promedio
from ESUSTENTADB import new_db_table
from ESUSTENTADB import eliminar_tabla
from ESUSTENTADB import calcula_inversos
from ESUSTENTADB import margedu
from ESUSTENTADB import margviv
from ESUSTENTADB import margeco
from ESUSTENTADB import margtot
from ESUSTENTADB import marg_deciles
from ESUSTENTADB import rangos_edad
from UTILERIAS_SHP_PY_3 import proyectashp
from UTILERIAS_SHP_PY_3 import mover_shp
from INTEGRADOR_EN_SHAPEFILE import shp
import ESUSTENTA_DBF as ESDBF
from ESUSTENTA_DBF import escritura



#Definición de variables
estados = [
        u"Aguascalientes",
        u"Baja California",
        u"Baja California Sur",
        u"Campeche",
        u"Chiapas",
        u"Chihuahua",
        u"Ciudad de Mexico",
        u"Coahuila",
        u"Colima",
        u"Durango",
        u"Guanajuato",
        u"Guerrero",
        u"Hidalgo",
        u"Jalisco",
        u"Mexico",
        u"Michoacan de Ocampo",
        u"Morelos",
        u"Nayarit",
        u"Nuevo Leon",
        u"Oaxaca",
        u"Puebla",
        u"Queretaro",
        u"Quintana Roo",
        u"San Luis Potosi",
        u"Sinaloa",
        u"Sonora",
        u"Tabasco",
        u"Tamaulipas",
        u"Tlaxcala",
        u"Veracruz de Ignacio de la Llave",
        u"Yucatan",
        u"Zacatecas"
    ]
tabla_elim = 'marginacion'
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
# columnas_a_sumar = ['POB42', 'POB84']
# nueva_columna = 'Gustavito'


#Proceso
for estado in estados:

    print(f'\n>>>>>>>>>>>>  Iniciando proceso para {estado}\n')
        
    database_path = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_manzanas.db'.format(estado,estado)
    ruta_shapefile = f"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad.shp"

    marg_param['database_path'] = database_path
    marg_param['nueva_columna_deciles'] = 'marg_decil'
    marg_param['columna_deciles'] = 'marg_tot'
    
    valores2['database_path'] = database_path

    # proyecta y copia archivo shapefile de scince a SIG INEGI
    # shp_in = 'C:/SCINCE 2020/32_ZAC/cartografia/manzana.shp'    # es importante verificar que el archivo a proyectar sea 'GCS_Mexico_ITRF2008'
    # shp_out = f'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad_1.shp'
    # proyectashp(shp_in, shp_out)
    # mover_shp(estado) # mueve archivos de la carpeta original a SIG
    escritura('Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/campos_estados.txt', estado)

    # # Calcula la marginación
    # eliminar_tabla(database_path, tabla_elim)
    # new_db_table(database_path, sql_query)
    # calcula_inversos(valores2)
    # margedu(marg_param)
    # margviv(marg_param)
    # margeco(marg_param)
    # margtot(marg_param)
    # marg_deciles(marg_param)

    # # Crea rangos de edad
    # rangos_edad(database_path, 'cpv2020_manzana_poblacion')

    # # Actualiza el archivo shapefile con los datos de la base de datos
    # shp(database_path, ruta_shapefile)

    

    print(f'\nproceso terminado para {estado}   >>>>>>>>>>>>\n')
print('\n\nproceso terminado exitosamente   >>>>>>>>>>>>>>>>>>>>>>>\n\n')
