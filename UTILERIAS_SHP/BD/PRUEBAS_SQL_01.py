# -*- coding: utf-8 -*-

# programa para abrir una tabla, hacer algunas operaciones, creando un nuevo campo y guardando toda la tabla en un archivo csv

import pandas as pd
from simpledbf import Dbf5
import time
import sqlite3

inicio = time.time()

# Ruta al archivo DBF
ruta_dbf = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatán/tablas/cpv2020_manzana_viviendaCopy.dbf'

# Lee el archivo DBF usando simpledbf
dbf_data = Dbf5(ruta_dbf, codec='latin-1')

# Convierte los datos a un DataFrame de Pandas
df = dbf_data.to_dataframe()

# Lista de columnas de interés
columnas_interes = ['VIV1', 'VIV2', 'VIV3']  # Agrega aquí las columnas que necesitas

# Función personalizada para aplicar a las columnas de interés
def nueva_columna(row, cols_interes):
    # Verifica si todas las columnas son mayores o iguales a 0
    if all(row[col] >= 0 for col in cols_interes):
        return sum(row[col] for col in cols_interes)
    else:
        return -6  # O cualquier valor predeterminado que desees para los casos en que no se cumpla la condición

# Aplica la función a las columnas de interés para crear la nueva columna 'nvacol'
df['nvacol'] = df.apply(nueva_columna, axis=1, cols_interes=columnas_interes)

# Guarda el DataFrame resultante en un nuevo archivo CSV
ruta_salida = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatán/tablas/cpv2020_manzana_viviendaCopy.csv'  # Reemplaza con la ruta y nombre de archivo deseado
df.to_csv(ruta_salida, index=False)

ruta_salida1 = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatán/tablas/cpv2020_manzana_viviendaCopy.db'

conn = sqlite3.connect(ruta_salida1)


# Guardar el DataFrame en la base de datos SQLite
df.to_sql('nombre_de_la_tabla', conn, index=False, if_exists='replace')  # Puedes cambiar 'replace' a 'append' si ya existe la tabla

# Cerrar la conexión
conn.close()

print(df)
# print('Duración: {time.time() - inicio} segundos')
