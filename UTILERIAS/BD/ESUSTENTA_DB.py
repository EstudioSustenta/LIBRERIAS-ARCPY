# -*- coding: utf-8 -*-
"""
Para ejecutarse con python 3.x
Este módulo cuenta con varias funciones para realizar acciones básicas con bases de datos sqlite.
Se creó para poder generar indices de marginación por manzana basados en los datos del SCINCE 2020
del INEGI
Para la documentación de este proceso, ver el proyecto OBSIDIAN 'programacion'
"""

import sqlite3
import pandas as pd
import geopandas as gpd
# import numpy as np
# from dbfpy import dbf
import os
from dbfread import DBF
from simpledbf import Dbf5


# import dbfread
# import dbf

sql_query = """
    CREATE TABLE marginacion AS
    SELECT
        CAST(poblacion.CVEGEO AS TEXT) AS CVEGEO,
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



def new_db(nueva_db):
    connection = sqlite3.connect(nueva_db)
    connection.close()
    return u'Nueva base de datos creada en {}'.format(nueva_db)

def existe_tabla(db, tabla):
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect(db)
        cursor = conexion.cursor()

        # Consultar si la tabla existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
        tabla_existente = cursor.fetchone()

        # Cerrar la conexión
        conexion.close()

        # Devolver True si la tabla existe, False si no existe
        return tabla_existente is not None

    except sqlite3.Error as e:
        # print(u"Error al verificar la existencia de la tabla: {}".format(e))
        conexion.close()
        return False

def marg_base_table(database_path, sql_query):

    """
    Esta función crea una nueva tabla en la base de datos especificada con los parámetros definidos
    en la variable 'sql_query'
    """
    print(database_path)
    try:
        # Verifica que la base de datos exista
        if os.path.exists(database_path) and existe_tabla(database_path,'poblacion'):
            # Conectarse a la base de datos
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()

            # Ejecutar la sentencia SQL
            cursor.execute(sql_query)

            # Confirmar los cambios y cerrar la conexión
            connection.commit()
            connection.close()

            return(f'Se ha completado la consulta en la tabla "poblacion" de la base de datos "{database_path}"')
        else:
            return(f'>>>>>>>>>>ERROR: No existe la tabla "poblacion" y/o la base de datos "{database_path}"')
    except Exception as e:
        return(f'>>>>>>>>>>ERROR: {e}')

def sumacols(database_path, tabla, nvocampo):
    # FUNCIÓN PARA SUMAR COLUMNAS EN UNA TABLA DE UNA BASE DE DATOS
    try:
        # Conectar a la base de datos
        connection = sqlite3.connect(database_path)

        # Consulta SQL para obtener los datos de la tabla 'marginacion'
        sql_query = "SELECT * FROM {};".format(tabla)

        # Cargar los datos en un DataFrame de pandas
        df = pd.read_sql_query(sql_query, connection)

        # Lista de columnas a sumar
        columnas_a_sumar = ['VIV0', 'VIV1', 'VIV2']  # Agrega más columnas según sea necesario

        # Crear una nueva columna con la suma de las columnas seleccionadas
        df['{}'.format(nvocampo)] = df[columnas_a_sumar].sum(axis=1)

        # Actualizar la tabla en la base de datos con la nueva columna
        df.to_sql('{}'.format(tabla), connection, index=False, if_exists='replace')

        # Cerrar la conexión
        connection.close()

        return("Operación completada con éxito. Se ha agregado la columna 'SUMA_TOTAL' a la tabla 'marginacion' en la base de datos.")
    except Exception as e:
        return(f'>>>>>>>>>>ERROR: {e}')

def eliminar_columnas(database_path, tabla, columnas_a_eliminar):
    """
    Elimina las columnas especificadas de una tabla en una base de datos SQLite.

    Parametros:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla (str): Nombre de la tabla en la que se eliminarán las columnas.
    - columnas_a_eliminar (list): Lista de nombres de columnas que se eliminarán.

    Returns:
    - None
    """

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Obtener la lista de todas las columnas en la tabla original
        obtener_columnas_query = "PRAGMA table_info({});".format(tabla)
        cursor.execute(obtener_columnas_query)
        columnas_actuales = [columna[1] for columna in cursor.fetchall()]

        # Verificar si las columnas a eliminar existen en la tabla
        for columna in columnas_a_eliminar:
            if columna not in columnas_actuales:
                raise ValueError("La columna '{}' no existe en la tabla '{}'.".format(columna, tabla))

        # Crear una nueva definición de la tabla sin las columnas especificadas
        nuevas_columnas = [columna for columna in columnas_actuales if columna not in columnas_a_eliminar]
        nueva_definicion_query = "CREATE TABLE {}_temp AS SELECT {} FROM {};".format(tabla, ', '.join(nuevas_columnas), tabla)
        cursor.execute(nueva_definicion_query)

        # Eliminar la tabla original
        eliminar_tabla_query = "DROP TABLE {};".format(tabla)
        cursor.execute(eliminar_tabla_query)

        # Renombrar la nueva tabla con el nombre original
        renombrar_tabla_query = "ALTER TABLE {}_temp RENAME TO {};".format(tabla, tabla)
        cursor.execute(renombrar_tabla_query)

        # Confirmar los cambios
        connection.commit()

        print("Columnas {} eliminadas de la tabla '{}' con éxito.".format(', '.join(columnas_a_eliminar), tabla))

    except sqlite3.Error as e:
        print("Error: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def eliminar_tabla(database_path, tabla_elim):
    """
    Elimina una tabla de respaldo de una base de datos SQLite.

    Parameters:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla_elim (str): Nombre de la tabla de respaldo que se eliminará.

    Returns:
    - None
    """

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Verificar si la tabla de respaldo existe
        verificar_tabla_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tabla_elim)
        cursor.execute(verificar_tabla_query)
        tabla_existente = cursor.fetchone()

        if tabla_existente:
            # Eliminar la tabla de respaldo
            eliminar_tabla_query = "DROP TABLE {};".format(tabla_elim)
            cursor.execute(eliminar_tabla_query)

            # Confirmar los cambios
            connection.commit()

            return("La tabla de respaldo '{}' ha sido eliminada con éxito.".format(tabla_elim))
        else:
            return("La tabla de respaldo '{}' no existe en la base de datos.".format(tabla_elim))

    except sqlite3.Error as e:
        return("Error: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def agregar_campo_y_calcular_valor(valores2):
    """
    
    """

    database_path = valores2['database_path']
    tabla = valores2['tabla']
    campocalc = valores2['campo']
    nuevoedu = '{}i'.format(campocalc)

    print('\n\n>>>>>>>>>>>>>>>>db: {}\ntabla: {}\ncampo a invertir: {}\ncampo invertido: {}'.format(database_path, tabla, campocalc, nuevoedu))

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:

        # Verificar si la columna ya existe
        cursor.execute(f"PRAGMA table_info({tabla})")
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if nuevoedu not in columnas_existentes:
            # Si la columna no existe, intentar agregarla
            cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {nuevoedu};")

            # Actualizar los valores en la nueva columna
            cursor.execute(f"""
                UPDATE {tabla} 
                SET {nuevoedu} = CASE WHEN {campocalc} >= 0 THEN 100 - {campocalc} ELSE -6 END;
            """)

            # Confirmar los cambios
            connection.commit()
            return("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {} y se han calculado sus valores.\n".format(nuevoedu, tabla))

        else:
            return("\nLa columna {} ya existe en la tabla {}.\n".format(nuevoedu, tabla))

    except sqlite3.Error as e:
        return("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()
    
def sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna):
    """
    Suma los valores de las columnas 'columnas_a_sumar' de la tabla 'tabla'
    en una base de datos SQLite y crea una nueva columna 'nueva_columna' con los resultados.
    Realiza la suma siempre y cuando ninguno de los valores a sumar sea 
    menor a 0, en ese caso asigna a la celda un valor = -6.

    Parámetros:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla (str): Nombre de la tabla en la que se realizará la suma.
    - nueva_columna (str): Nombre de la nueva columna que se creará.
    - columnas_a_sumar (lista): lista de columnas que contienen los valores a sumar.

    Returna:
    - Nada
    """

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)

    try:
        # Consulta SQL para obtener los datos de la tabla 'marginacion'
        sql_query = "SELECT * FROM {};".format(tabla)

        # Cargar los datos en un DataFrame de pandas
        df = pd.read_sql_query(sql_query, connection)

        df = convertir_columnas_numericas(df)


        # Crear una nueva columna con la suma de las columnas seleccionadas
        df[nueva_columna] = df[columnas_a_sumar].sum(axis=1)

        # Aplicar la condición de que si algún valor es negativo, el resultado sea '-6'
        # df[nueva_columna] = df[nueva_columna].apply(lambda x: -6 if x < 0 else x)
        df[nueva_columna] = df[nueva_columna].apply(lambda x: -6 if float(x) < 0 else x)

        # Actualizar la tabla en la base de datos con la nueva columna
        df.to_sql(tabla, connection, index=False, if_exists='replace')

        print("Operación completada con éxito. Se ha agregado la columna '{}' a la tabla '{}' en la base de datos.".format(nueva_columna, tabla))

    except sqlite3.Error as e:
        print("Error: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def obtener_campos_por_cvegeo(database_path, tabla, cvegeo):
    """
    Obtiene los campos 'POB1', 'POB2' y 'POB3' del registro con el valor de 'CVEGEO' especificado.

    Parameters:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla (str): Nombre de la tabla en la que se realizará la consulta.
    - cvegeo (str): Valor de 'CVEGEO' para identificar el registro deseado.

    Returns:
    - dict: Diccionario con los campos 'POB1', 'POB2' y 'POB3' del registro encontrado.
            Si no se encuentra el registro, retorna None.
    """

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Consulta SQL para obtener los campos especificados del registro con 'CVEGEO' igual a cvegeo
        sql_query = "SELECT POB1, POB32, POB84 FROM {} WHERE CVEGEO = '{}';".format(tabla, cvegeo)

        # Ejecutar la consulta
        cursor.execute(sql_query)

        # Obtener el resultado
        resultado = cursor.fetchone()

        if resultado:
            # Crear un diccionario con los nombres de los campos y sus valores
            campos = ['POB1', 'POB32', 'POB84']
            resultado_dict = dict(zip(campos, resultado))
            return resultado_dict
        else:
            print("No se encontró ningún registro con CVEGEO igual a '{}' en la tabla '{}'.".format(cvegeo, tabla))
            return None

    except sqlite3.Error as e:
        print("Error: {}".format(e))
        return None

    finally:
        # Cerrar la conexión
        connection.close()

def creacol(database_path, tabla, nueva_columna, operacion, condicion):
    """
    Esta función crea una nueva columna 'nueva_columna' con el resultado de una expresión
    sql definida en 'operacion' o la actualiza si ya existe, condicionada a 'condicion'.
    Si la condición no se cumple, se asigna el valor -6.
    """
    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if nueva_columna not in columnas_existentes:
            # Si la columna no existe, intentar agregarla
            cursor.execute("ALTER TABLE {} ADD COLUMN {};".format(tabla, nueva_columna))

        # Ejecutar la sentencia SQL UPDATE con condición y manejo de valor no positivo
        sql_update = """
            UPDATE {} SET {} = 
            CASE WHEN {} THEN {} ELSE -6 END;
        """.format(tabla, nueva_columna, condicion, operacion)

        cursor.execute(sql_update)

        # Confirmar los cambios
        connection.commit()
        print("\nOperación completada con éxito. Se ha actualizado o creado la columna {} en la tabla {}.\n".format(nueva_columna, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def crear_columna_vacia(database_path, tabla, nueva_columna, valor_predeterminado):

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if nueva_columna not in columnas_existentes:
            # Si la columna no existe, intentar agregarla con el valor predeterminado
            cursor.execute("ALTER TABLE {} ADD COLUMN {} DEFAULT {};".format(tabla, nueva_columna, valor_predeterminado))

        # Confirmar los cambios
        connection.commit()
        # print("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {}.\n".format(nueva_columna, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def calc_promedio(marg_param):

    database_path = marg_param['database_path']
    tabla = marg_param['tabla']
    nueva_columna = marg_param['nvocampo']
    campos = marg_param['campos']
    valor_predeterminado = None

    crear_columna_vacia(database_path, tabla, nueva_columna, valor_predeterminado)

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Crear y ejecutar la sentencia SQL para calcular el promedio condicional
        condiciones_sql =       " + ".join([f"CASE WHEN {campo} >= 0 THEN {campo} ELSE 0 END" for campo in campos])
        count_condiciones_sql = " + ".join([f"CASE WHEN {campo} >= 0 THEN 1 ELSE 0 END" for campo in campos])
        sql_promedio = f"""
            UPDATE {tabla} SET {nueva_columna} = 
            CASE WHEN {condiciones_sql} + {count_condiciones_sql} > 0 
            THEN ROUND((({condiciones_sql}) / NULLIF({count_condiciones_sql}, 0)),1) 
            ELSE -6 
            END;
            """

        cursor.execute(sql_promedio)

        # Confirmar los cambios
        connection.commit()
        return("\nOperación completada con éxito. Se ha actualizado la columna {} en la tabla {}.\n".format(nueva_columna, tabla))

    except sqlite3.Error as e:
        return("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def margedu(marg_param):        # calcula la marginación educativa
    """
    Calcula la marginación promedio para el vector de educación
    """
    marg_param['campos'] = ['EDU28_R',
                            'EDU43_Ri',
                            'EDU46_Ri'
                            ]
    
    marg_param['nvocampo'] = 'marg_edu'

    return(calc_promedio(marg_param))

def margviv(marg_param):        # calcula la marginación en vivienda
    """
    Calcula la marginación promedio para el vector de vivienda
    """
    marg_param['campos'] = ['VIV7_R',
                            'VIV10_R',
                            'VIV14_R',
                            'VIV16_R',
                            'VIV18_R',
                            'VIV21_R',
                            'VIV24_R',
                            'VIV26_R',
                            'VIV30_R',
                            'VIV31_R',
                            'VIV39_R',
                            'VIV40_R',
                            'VIV41_R',
                            'VIV42_R']
    
    marg_param['nvocampo'] = 'marg_viv'

    return(calc_promedio(marg_param))    # calcula la marginación educativa

def margeco(marg_param):        # calcula la marginación económica
    """
    Calcula la marginación promedio para el vector de economía
    """
    marg_param['campos'] = [
                            'ECO1_R',
                            'ECO2_R',
                            'ECO3_R',
                            'ECO25_R',
                            'ECO26_R',
                            'ECO27_R'
                            ]
    
    marg_param['nvocampo'] = 'marg_eco'

    return(calc_promedio(marg_param))    # calcula la marginación educativa

def margtot(marg_param):        # calcula la marginación total
    """
    Calcula la marginación total promedio en base e la marginacion educativa, de vivienda, económica y de salud
    """
    marg_param['campos'] = [
                            'marg_edu',
                            'marg_viv',
                            'marg_eco',
                            'SALUD2_R'
                            ]
    
    marg_param['nvocampo'] = 'marg_tot'

    return(calc_promedio(marg_param))    # calcula la marginación educativa

def marg_deciles(marg_param):  # 
    database_path = marg_param['database_path']
    tabla = marg_param['tabla']

    columna_decil = marg_param['columna_deciles']
    nueva_columna_decil = marg_param['nueva_columna_deciles']

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if nueva_columna_decil not in columnas_existentes:
            # Si la columna no existe, intentar agregarla con valores calculados
            cursor.execute("ALTER TABLE {} ADD COLUMN {};".format(tabla, nueva_columna_decil))

            # Calcular y actualizar los valores en la nueva columna
            cursor.execute(f"""
                UPDATE {tabla} 
                SET {nueva_columna_decil} = 
                CASE WHEN {columna_decil} >= 0 
                THEN CAST({columna_decil} / 10 AS INTEGER)
                ELSE -6
                END;
            """)

            # Confirmar los cambios
            connection.commit()
            return("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {}.\n".format(nueva_columna_decil, tabla))

        else:
            return("\nLa columna {} ya existe en la tabla {}.\n".format(nueva_columna_decil, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def asignar_valor_nulo(marg_param):
    """
    Esta función asigna un nuevo valor a los campos NULL en una columna de una tabla,
    condicionada a una expresión específica.
    """
    database_path = marg_param['database_path']
    tabla = marg_param['tabla']
    columna_decil = marg_param['nueva_columna_deciles']
    nuevo_valor = -6
    condicion = '{} IS NULL'.format(columna_decil)

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Verificar si la columna existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if columna_decil in columnas_existentes:
            # Actualizar los valores en la columna condicionados a la expresión
            cursor.execute("""
                UPDATE {} 
                SET {} = {}
                WHERE {};
            """.format(tabla, columna_decil, nuevo_valor, condicion))

            # Confirmar los cambios
            connection.commit()
            print("\nOperación completada con éxito. Se han asignado los valores en la columna {} en la tabla {}.\n".format(columna_decil, tabla))

        else:
            print("\nLa columna {} no existe en la tabla {}.\n".format(columna_decil, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def calcula_inversos(valores2):
    """calcula los inversos para los campos 'EDU43_R', 'EDU46_R'
    puesto aue en los datos del inegi estos son valores positivos,
    es decir, que son personas que cuentan con educación, cuando
    lo que buscamos medir con la marginación, es el porcentaje de
    personas que NO cuentan con educación, de esta manera, cuando se
    sumen los valores de este cálculo con los valores de los otros
    tipos de carencias socioeconómocas, podremos calcular adecuadamente
    la marginación total"""

    print(f">>>>>> Valores a invertir: {valores2['campocalc']}")

    for campo in valores2['campocalc']:
        print(f'>>>>>>>>>>>>  Calculando inverso para {campo}')
        valores2['campo'] = campo
        resultado = agregar_campo_y_calcular_valor(valores2)
    # return(resultado)

def contar_registros(database_path, tabla):
    """
    Esta función cuenta los registros de una tabla en una base de datos SQLite.
    """
    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Ejecutar la consulta para contar los registros
        cursor.execute("SELECT COUNT(*) FROM {}".format(tabla))
        count = cursor.fetchone()[0]

        print("\nLa tabla '{}' tiene {} registros.\n".format(tabla, count))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def exportar_a_dbf1(database_path, tabla, archivo_dbf):      # exporta los registros de una tabla de una base de datos a un archivo dbf
    """
    Exporta la tabla especificada de la base de datos SQLite a un archivo DBF.

    Parameters:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla (str): Nombre de la tabla que se exportará.
    - archivo_dbf (str): Ruta del archivo DBF de destino.
    """
    # Conectar a la base de datos SQLite
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Obtener los datos de la tabla
        cursor.execute("SELECT * FROM {}".format(tabla))
        datos = cursor.fetchall()

        # Obtener los nombres de las columnas
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas = [columna[1] for columna in cursor.fetchall()]

        # Crear un nuevo archivo DBF
        dbf_file = dbf.Dbf(archivo_dbf, new=True)

        # Agregar las columnas al archivo DBF
        for columna in columnas:
            dbf_file.addField((columna, "C", 50))

        # Agregar los datos al archivo DBF
        for fila in datos:
            nueva_fila = dbf_file.newRecord()

            for i, valor in enumerate(fila):
                nueva_fila[columnas[i]] = str(valor)

            nueva_fila.store()

        print("Exportación a DBF completada con éxito.")

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión y el archivo DBF
        connection.close()
        dbf_file.close()

import sqlite3
import geopandas as gpd

def append_to_shapefile(db, table, shapefile):
    """
    Append data from a SQLite table to an existing shapefile.

    Parameters:
    - db (str): Path to the SQLite database file.
    - table (str): Name of the table to export.
    - shapefile (str): Path to the existing shapefile to append data to.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        # Retrieve data from the specified table
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()

        # Retrieve column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [column[1] for column in cursor.fetchall()]

        # Convert data to a GeoDataFrame
        gdf = gpd.GeoDataFrame(data, columns=columns)

        # Convert 'CVEGEO' column to string type
        gdf['CVEGEO'] = gdf['CVEGEO'].astype(str)

        # Append data to the existing shapefile
        existing_gdf = gpd.read_file(shapefile)
        combined_gdf = gpd.GeoDataFrame(pd.concat([existing_gdf, gdf], ignore_index=True))

        # Save the combined GeoDataFrame back to the shapefile
        combined_gdf.to_file(shapefile)

        print("Data appended to shapefile successfully.")

    except sqlite3.Error as e:
        print("Error during process:", e)

    finally:
        # Close the connection to the SQLite database
        if connection:
            connection.close()

def rangos_edad(database_path, tabla):

    """
    Crea columnas de rangos de edad definidos en la variable 'rangos_edad'
    en la tabla y base de datos definidas
    variables:
    'database_path': base de datos (incluye la ruta de archivo completa)
    'tabla': tabla existente en la base de datos
    'columnas_a_sumar': lista de 
    Returns: none
    """

    rangos_edad = {'POB130_es':['POB2'],
                   'POB131_es':['POB4', 'POB5'],
                   'POB132_es':['POB7', 'POB9'],
                   'POB133_es':['POB13', 'POB30', 'POB31'],
                   'POB134_es':['POB32', 'POB33', 'POB34'],
                   'POB135_es':['POB35', 'POB36', 'POB16'],
                   'POB136_es':['POB37', 'POB38', 'POB39', 'POB40', 'POB41']
                    }
    

    for rango_edad in rangos_edad:
        nueva_columna = rango_edad
        columnas_a_sumar = rangos_edad[nueva_columna]
        print ('nueva columna: {}, columnas: {}'.format(nueva_columna, columnas_a_sumar))

        sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna)
    return(f'Se han creado rangos de edad para la tabla "{tabla}" en la base de datos "{database_path}"')

def convertir_columnas_numericas(df):
    """
    Convierte las columnas de un DataFrame a tipo numérico,
    excepto la columna 'CVEGEO'.

    Parámetros:
    - df (DataFrame): DataFrame de pandas.

    Retorna:
    - DataFrame: DataFrame con las columnas convertidas.
    """
    # Obtener una lista de todas las columnas excepto 'CVEGEO'
    columnas_a_convertir = [col for col in df.columns if col != 'CVEGEO']

    # Convertir las columnas a tipo numérico
    df[columnas_a_convertir] = df[columnas_a_convertir].apply(pd.to_numeric, errors='coerce')

    return df



def ejecuta(valores):
    estados = valores['estados']
    sql_query = valores['sql_query']
    tabla = 'marginacion'
    nvocampo = 'SUM_TO1'
    tabla_a_actualizar = 'cpv2020_manzana_poblacion'
    columnas_a_eliminar = ['POB130_es', 'POB131_es', 'POB132_es', 'POB133_es', 'POB134_es', 'POB135_es', 'POB136_es']# Agrega más columnas según sea necesario
    tabla_elim = 'marginacion'

    # Lista de columnas a sumar
    columnas_a_sumar = ['POB42', 'POB84']
    cvegeo = '0100600010051005'

    marg_param = {'tabla' : tabla}

    valores2 = {'campocalc' : ['EDU43_R', 'EDU46_R'],
                'tabla' : tabla
                }

    for estado in estados:
        # Ruta de la base de datos SQLite

        database_path = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_manzanas.db'.format(estado,estado)
        marg_param['database_path'] = database_path
        marg_param['nueva_columna_deciles'] = 'marg_decil'
        marg_param['columna_deciles'] = 'marg_tot'

        archivo_dbf = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/cpv2020_manzana_{}.dbf'.format(estado,tabla)

        valores2['database_path'] = database_path

        print ('\n\n')
        print (estado)
        print (database_path)
        print ('\n')

        nueva_columna = 'pobtot'

        # DESCOMENTAR LAS INSTRUCCIONES SIGUIENTES PARA EJECUTAR LAS FUNCIONES CORRESPONDIENTES

        # sumacols(database_path, tabla, nvocampo)
        # sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna)
        # eliminar_tabla(database_path, tabla_elim)
        # marg_base_table(database_path, sql_query) # crea la tabla base de marginación
        # calcula_inversos(valores2)
        # eliminar_columnas(database_path, tabla_a_actualizar, columnas_a_eliminar)
        # sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna)
        # print (obtener_campos_por_cvegeo(database_path, tabla, cvegeo))
        # margedu(marg_param)    # calcula la marginación educativa
        # margviv(marg_param)    # calcula la marginación en vivienda
        # margeco(marg_param)     # calcula la marginación económica
        # margtot(marg_param)     # calcula la marginación económica
        # marg_deciles(marg_param)    # Llamar a la función para crear la columna de deciles
        # asignar_valor_nulo(marg_param)
        # eliminar_columnas(database_path, tabla_a_actualizar, valores['cols_temp'])

        # contar_registros(database_path, 'marginacion')
        # rangos_edad(database_path, 'cpv2020_manzana_poblacion', columnas_a_sumar, nueva_columna)





if __name__ == "__main__":

    estados = [
            # u"Aguascalientes",
            # u"Baja California",
            # u"Baja California Sur",
            # u"Campeche",
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

    cols_temp = [
                'POB1',
                'POB42',
                'POB84',
                'ECO1_R',
                'ECO2_R',
                'ECO3_R',
                'ECO25_R',
                'ECO26_R',
                'ECO27_R',
                'SALUD2_R',
                'VIV0',
                'VIV7_R',
                'VIV10_R',
                'VIV14_R',
                'VIV16_R',
                'VIV18_R',
                'VIV21_R',
                'VIV24_R',
                'VIV26_R',
                'VIV30_R',
                'VIV31_R',
                'VIV39_R',
                'VIV40_R',
                'VIV41_R',
                'VIV42_R',
                'EDU28_R',
                'EDU43_R',
                'EDU46_R'
                ]

    valores = {'estados' : estados,
               'sql_query': sql_query,
               'cols_temp' : cols_temp}

    # new_db_table(valores)
    # ejecuta(valores)
    db = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/tablas/manzana.db'
    tabla1 = 'poblacion'
    dbff = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia/municipal.shp'
    camposborr = [
        'POB130_es',
        'POB131_es',
        'POB132_es',
        'POB133_es',
        'POB134_es',
        'POB135_es',
        'POB136_es',
    ]

    # Example usage:
    # append_to_shapefile(db, tabla1, dbff)
    eliminar_columnas(db, tabla1, camposborr)