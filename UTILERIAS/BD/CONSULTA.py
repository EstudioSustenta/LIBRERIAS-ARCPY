# -*- coding: utf-8 -*-

# programa para abrir una base de datos y hacer una consulta

import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite

ruta_salida1 = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatán/tablas/compedio.db' # 
# base_de_datos = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatán/tablas/cpv2020_manzana.db'

conn = sqlite3.connect(ruta_salida1)

# Valor específico de 'gvegeo' que estás buscando
valor_CVEGEO = '3100100010107001'
nomcampo = 'VIV0'

# Consulta SQL para seleccionar el valor de 'VIV0' donde 'gvegeo' coincide con el valor específico
consulta_sql = "SELECT {} FROM nombre_de_la_tabla WHERE CVEGEO = '{}'".format(nomcampo,valor_CVEGEO)

# Ejecutar la consulta y cargar los resultados en un DataFrame
df_resultado = pd.read_sql_query(consulta_sql, conn)

# Cerrar la conexión
conn.close()

# Mostrar el valor recuperado
if not df_resultado.empty:
    valor_recuperado = df_resultado[nomcampo].iloc[0]
    print("\nEl valor de '{}' para 'CVEGEO' {} es: {}\n".format(nomcampo, valor_CVEGEO, valor_recuperado))
else:
    print("\nNo se encontraron resultados para 'CVEGEO' = {}\n".format(valor_CVEGEO))
