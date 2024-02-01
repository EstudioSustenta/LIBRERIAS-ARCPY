# -*- coding: utf-8 -*-
"""
El código  extraer datos de consultas SQL en una base de datos SQLite y guardar los resultados en 
archivos DBF.

Aquí está un resumen paso a paso:

1.- Conexión a la Base de Datos SQLite:

Establece una conexión a la base de datos SQLite especificada en database_path.
Crea un objeto cursor para ejecutar consultas SQL.
Ejecución de Consultas SQL y Construcción de DataFrame:

2.- Itera sobre un diccionario de consultas SQL (queries).
Para cada consulta, ejecuta la consulta SQL utilizando el cursor.
Construye un DataFrame de pandas (result_df) con los resultados de las consultas.
Creación y Manipulación de Archivos DBF:

3.- Crea un archivo temporal DBF utilizando la biblioteca dbfpy.
Itera sobre las columnas del DataFrame resultante y agrega campos al archivo DBF.
Itera sobre las filas del DataFrame y agrega registros al archivo DBF.
Gestión de Archivos y Extensiones:

4.- Verifica si el archivo DBF de salida ya existe y lo elimina si es necesario.
Cambia la extensión del archivo temporal DB a .dbf.
Cierre de Conexión y Finalización:

5.- Cierra la conexión a la base de datos SQLite.
Proceso para Varios Estados:

6.- Define una lista de estados a procesar.
Itera sobre la lista de estados y realiza el proceso de extracción y almacenamiento para cada estado.
Muestra mensajes informativos durante el proceso.

En resumen, el código automatiza la extracción de datos de consultas SQL específicas de una base de datos SQLite 
para varios estados, y guarda los resultados en archivos DBF, teniendo en cuenta la manipulación de archivos 
temporales y la gestión de extensiones. También proporciona información sobre el progreso del proceso a través 
de mensajes en la consola.

"""

import pandas as pd
import sqlite3
from dbfpy import dbf
import os

def executa(database_path, queries, output_dbf_path):
    # Crear un DataFrame vacío
    result_df = pd.DataFrame()

    # Establecer conexión directa a la base de datos SQLite
    connection = sqlite3.connect(database_path)

    # Crear un objeto cursor para ejecutar consultas
    cursor = connection.cursor()

    # Iterar sobre las consultas y extraer resultados
    for query_name, query in queries.items():
        # Ejecutar la consulta SQL y cargar el resultado en un DataFrame
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=columns)

        # Agregar las columnas al resultado
        result_df = pd.concat([result_df, df], axis=1)

    # Guardar el DataFrame resultante en un archivo DBF utilizando dbfpy
    output_temp_path = output_dbf_path.replace('.dbf', '.db')
    dbf_writer = dbf.Dbf(output_temp_path, new=True)

    # Agregar campos al archivo DBF
    for col_name in result_df.columns:
        dbf_writer.addField((col_name, 'C', 20))  # Puedes ajustar el tipo y tamaño según tus necesidades

    # Agregar registros al archivo DBF
    for _, row in result_df.iterrows():
        record = dbf_writer.newRecord()

        for col_name in result_df.columns:
            record[col_name] = str(row[col_name])

        record.store()

    # Cerrar el archivo DBF
    dbf_writer.close()

    # Verifica si el archivo DBF existe, de ser así lo elimina.
    if os.path.exists(output_dbf_path):
        print('\nEl archivo:\n{}\nexiste, se borrara de disco'.format(output_dbf_path))
        os.remove(output_dbf_path)

    # Cambiar la extensión del archivo a .dbf    
    os.rename(output_temp_path, output_dbf_path)

    # Cerrar la conexión
    connection.close()

def extrae(valores):
    estados = valores['estados']
    print('\n\nIniciando proceso...')
    
    for estado in estados:
        print('\n{}'.format(estado))
        output_dbf_path = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/00_marginacion.dbf'.format(estado)
        queries = valores['queries']
        database_path = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_manzanas.db'.format(estado, estado)

        executa(database_path, queries, output_dbf_path)
        print('{} terminado.\n'.format(estado))
    print('\n\nProceso terminado!\n\n')

queries_to_extract = {
    "query_poblacion": "SELECT POB1, POB32, POB84 FROM cpv2020_manzana_poblacion",
    "query_vivienda": "SELECT CVEGEO, VIV0, VIV1, VIV2 FROM cpv2020_manzana_vivienda"
    # Agrega más consultas según sea necesario
}

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

valores = {'estados': estados, 'queries': queries_to_extract}

if __name__ == "__main__":
    extrae(valores)














# -------------------------------------------------------------------------

# este código convierta los campos de las tablas a un archivo txt.



# # -*- coding: utf-8 -*-

# import pandas as pd
# import sqlite3

# def executa(database_path, queries, output_txt_path):
#     # Crear un DataFrame vacío
#     result_df = pd.DataFrame()

#     # Establecer conexión directa a la base de datos SQLite
#     connection = sqlite3.connect(database_path)

#     # Crear un objeto cursor para ejecutar consultas
#     cursor = connection.cursor()

#     # Iterar sobre las consultas y extraer resultados
#     for query_name, query in queries.items():
#         # Ejecutar la consulta SQL y cargar el resultado en un DataFrame
#         cursor.execute(query)
#         columns = [desc[0] for desc in cursor.description]
#         df = pd.DataFrame(cursor.fetchall(), columns=columns)

#         # Agregar las columnas al resultado
#         result_df = pd.concat([result_df, df], axis=1)

#     # Guardar el DataFrame resultante en un archivo de texto (CSV o TXT)
#     result_df.to_csv(output_txt_path, index=False, sep='\t')  # Puedes cambiar '\t' por ',' si prefieres formato CSV

#     # Cerrar la conexión
#     connection.close()

# def extrae(valores):
#     estados = valores['estados']

#     for estado in estados:
#         output_txt_path = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/00extraido.txt'.format(estado)
#         queries = valores['queries']
#         database_path = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_manzanas.db'.format(estado, estado)

#         executa(database_path, queries, output_txt_path)

# queries_to_extract = {
#     "query_vivienda": "SELECT VIV0, VIV1, VIV2 FROM cpv2020_manzana_vivienda"
#     "query_poblacion": "SELECT POB1, POB32, POB84 FROM cpv2020_manzana_poblacion",
#     # Agrega más consultas según sea necesario
# }

# estados = [
#     u"Aguascalientes",
#     u"Zacatecas"
# ]

# valores = {'estados': estados, 'queries': queries_to_extract}

# if __name__ == "__main__":
#     extrae(valores)


