# -*- coding: utf-8 -*-

"""
Para ejecutarse con python 2.x
Este módulo cuenta con varias funciones para realizar acciones básicas con bases de datos sqlite.
Para la documentación de este proceso, ver el proyecto OBSIDIAN 'programacion'
"""

import sqlite3
# import pandas as pd
# import geopandas as gpd
# import numpy as np
# from dbfpy import dbf
# import arcpy
from dbfread import DBF
# from simpledbf import Dbf5


# import dbfread
# import dbf

def new_db(nueva_db):
    connection = sqlite3.connect(nueva_db)
    connection.close()
    return u'Nueva base de datos creada en {}'.format(nueva_db)

def agregar_tabla_dbf_a_db(dbf_path, sqlite_db_path, tabla_sqlite):
    # Conectar a la base de datos SQLite
    connection = sqlite3.connect(sqlite_db_path)
    cursor = connection.cursor()

    # Leer los datos desde el archivo DBF
    # with DBF(dbf_path) as table:
    with DBF(dbf_path, encoding='latin-1') as table:  # Especificar la codificación
        # Obtener nombres de campos y tipos
        nombres_campos = [field.name for field in table.fields]
        tipos_campos = [field.type for field in table.fields]

        # Crear la tabla en SQLite
        crear_tabla_sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            tabla_sqlite, ', '.join('{} {}'.format(nombre, tipo) for nombre, tipo in zip(nombres_campos, tipos_campos))
        )
        cursor.execute(crear_tabla_sql)

        # Insertar datos en la tabla SQLite
        for record in table:
            valores = [record[nombre] for nombre in nombres_campos]
            insertar_sql = "INSERT INTO {} VALUES ({})".format(
                tabla_sqlite, ', '.join(['?'] * len(nombres_campos))
            )
            cursor.execute(insertar_sql, valores)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    connection.close()

    return("Tabla DBF importada a SQLite: {}".format(tabla_sqlite))

def contar_reg_tabla(db, tabla):
    """
    Cuenta la cantidad de registros en una tabla 'tabla'
    de la base de datos 'db'
    Returns: cantidad de registros
    """
    
    # Conectarse a la base de datos
    conexion = sqlite3.connect(db)

    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Ejecutar la consulta SQL para contar la cantidad de archivos
    cursor.execute('SELECT COUNT(*) FROM {}'.format(tabla))

    # Obtener el resultado
    cantidad_registros = cursor.fetchone()[0]

    # Imprimir la cantidad de archivos
    return cantidad_registros

    # Cerrar la conexión
    conexion.close()

def existe_tabla(db, tabla):
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect(db)
        cursor = conexion.cursor()

        # Consultar si la tabla existe
        cursor.execute(u"SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tabla))
        tabla_existente = cursor.fetchone()

        # Cerrar la conexión
        conexion.close()

        # Devolver True si la tabla existe, False si no existe
        return tabla_existente is not None

    except sqlite3.Error as e:
        print(u"Error al verificar la existencia de la tabla: {}".format(e))
        return False

