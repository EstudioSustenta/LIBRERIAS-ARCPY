# -*- coding: utf-8 -*-
"""
Este módulo cuenta con varias funciones para realizar acciones básicas con bases de datos sqlite.
Se creó para poder generar indices de marginación por manzana basados en los datos del SCINCE 2020
del INEGI
Para la documentación de este proceso, ver el proyecto OBSIDIAN 'programacion'
"""
import sqlite3
import pandas as pd
import numpy as np

def new_db_table(database_path, sql_query):

    """
    Esta función crea una nueva tabla en la base de datos especificada con los parámetros definidos
    en la variable 'sql_query'
    """

    # Ruta de la base de datos SQLite

    # Conectarse a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Ejecutar la sentencia SQL
    cursor.execute(sql_query)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    connection.close()

    print("La nueva tabla ha sido creada con exito.")

def sumacols(database_path, tabla, nvocampo):
    # FUNCIÓN PARA SUMAR COLUMNAS EN UNA TABLA DE UNA BASE DE DATOS
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

    print("Operación completada con éxito. Se ha agregado la columna 'SUMA_TOTAL' a la tabla 'marginacion' en la base de datos.")

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

            print("La tabla de respaldo '{}' ha sido eliminada con éxito.".format(tabla_elim))
        else:
            print("La tabla de respaldo '{}' no existe en la base de datos.".format(tabla_elim))

    except sqlite3.Error as e:
        print("Error: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def agregar_campo_y_calcular_valor(valores2):

    database_path = valores2['database_path']
    tabla = valores2['tabla']
    campocalc = valores2['campocalc']
    nuevoedu = '{}i'.format(campocalc)

    print('\n\ndb: {}\ntabla: {}\ncampo a invertir: {}\ncampo invertido: {}'.format(database_path, tabla, campocalc, nuevoedu))

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]

        if nuevoedu not in columnas_existentes:
            # Si la columna no existe, intentar agregarla
            cursor.execute("ALTER TABLE {} ADD COLUMN {};".format(tabla, nuevoedu))

            # Actualizar los valores en la nueva columna
            cursor.execute("""
                UPDATE {} 
                SET {} = CASE WHEN {} >= 0 THEN 100 - {} ELSE -6 END;
            """.format(tabla, nuevoedu, campocalc, campocalc))

            # Confirmar los cambios
            connection.commit()
            print("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {} y se han calculado sus valores.\n".format(nuevoedu, tabla))

        else:
            print("\nLa columna {} ya existe en la tabla {}.\n".format(nuevoedu, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()
    
def sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna):
    """
    Suma los valores de las columnas 'columnas_a_sumar' de la tabla 'tabla'
    en una base de datos SQLite y crea una nueva columna con los resultados.

    Parameters:
    - database_path (str): Ruta de la base de datos SQLite.
    - tabla (str): Nombre de la tabla en la que se realizará la suma.
    - nueva_columna (str): Nombre de la nueva columna que se creará.
    - columnas_a_sumar: lista de columnas que contienen los valores a sumar.

    Returns:
    - None
    """

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)

    try:
        # Consulta SQL para obtener los datos de la tabla 'marginacion'
        sql_query = "SELECT * FROM {};".format(tabla)

        # Cargar los datos en un DataFrame de pandas
        df = pd.read_sql_query(sql_query, connection)

        # Crear una nueva columna con la suma de las columnas seleccionadas
        df[nueva_columna] = df[columnas_a_sumar].sum(axis=1)

        # Aplicar la condición de que si algún valor es negativo, el resultado sea '-6'
        df[nueva_columna] = df[nueva_columna].apply(lambda x: -6 if x < 0 else x)

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
        print("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {}.\n".format(nueva_columna, tabla))

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
        condiciones_sql = " + ".join(["CASE WHEN {} >= 0 THEN {} ELSE 0 END".format(campo, campo) for campo in campos])
        count_condiciones_sql = " + ".join(["CASE WHEN {} >= 0 THEN 1 ELSE 0 END".format(campo) for campo in campos])

        sql_promedio = """
            UPDATE {} SET {} = 
            CASE WHEN {} >= 0 THEN ({}) / NULLIF({}, 0) ELSE -6 END;
        """.format(tabla, nueva_columna, condiciones_sql, condiciones_sql, count_condiciones_sql)

        cursor.execute(sql_promedio)

        # Confirmar los cambios
        connection.commit()
        print("\nOperación completada con éxito. Se ha actualizado la columna {} en la tabla {}.\n".format(nueva_columna, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def margedu(marg_param):
    """
    Calcula la marginación promedio para el vector de educación
    """
    marg_param['campos'] = ['EDU28_R', 'EDU43_Ri', 'EDU46_Ri']
    marg_param['nvocampo'] = 'marg_edu'

    calc_promedio(marg_param)    # calcula la marginación educativa

def margviv(marg_param):
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

    calc_promedio(marg_param)    # calcula la marginación educativa

def margeco(marg_param):
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

    calc_promedio(marg_param)    # calcula la marginación educativa

def margtot(marg_param):
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

    calc_promedio(marg_param)    # calcula la marginación educativa

def crear_columna_deciles(marg_param):
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
            cursor.execute("""
                UPDATE {} 
                SET {} = CAST({} / 10 AS INTEGER);
            """.format(tabla, nueva_columna_decil, columna_decil))

            # Confirmar los cambios
            connection.commit()
            print("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {}.\n".format(nueva_columna_decil, tabla))

        else:
            print("\nLa columna {} ya existe en la tabla {}.\n".format(nueva_columna_decil, tabla))

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
    for campo in valores2['campocalc']:
        valores2['campocalc'] = campo
        agregar_campo_y_calcular_valor(valores2)


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





def ejecuta(valores):
    estados = valores['estados']
    sql_query = valores['sql_query']
    tabla = 'marginacion'
    nvocampo = 'SUM_TO1'
    tabla_a_actualizar = 'marginacion'
    columnas_a_eliminar = ['marg_decil']  # Agrega más columnas según sea necesario
    tabla_elim = 'marginacion'
    
    # Lista de columnas a sumar
    columnas_a_sumar = ['VIV0', 'VIV1', 'VIV2', 'POB1', 'POB32', 'POB84']
    cvegeo = '0100600010051005'

    marg_param = {'tabla' : tabla}

    valores2 = {'campocalc' : ['EDU43_R', 'EDU46_R'],
                'tabla' : tabla
                }
    
    for estado in estados:
        # Ruta de la base de datos SQLite
        database_path = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_compendio - copia.db'.format(estado,estado)
        marg_param['database_path'] = database_path
        marg_param['nueva_columna_deciles'] = 'marg_decil'
        marg_param['columna_deciles'] = 'marg_tot'
        
        valores2['database_path'] = database_path

        # sumacols(database_path, tabla, nvocampo)
        # eliminar_tabla(database_path, tabla_elim)
        new_db_table(database_path, sql_query)
        calcula_inversos(valores2)
        # eliminar_columnas(database_path, tabla_a_actualizar, columnas_a_eliminar)
        # sumar_columnas(database_path, tabla, columnas_a_sumar, nueva_columna)
        # print (obtener_campos_por_cvegeo(database_path, tabla, cvegeo))
        margedu(marg_param)    # calcula la marginación educativa
        margviv(marg_param)    # calcula la marginación en vivienda
        margeco(marg_param)     # calcula la marginación económica
        margtot(marg_param)     # calcula la marginación económica
        crear_columna_deciles(marg_param)    # Llamar a la función para crear la columna de deciles
        asignar_valor_nulo(marg_param)
        eliminar_columnas(database_path, tabla_a_actualizar, valores['cols_temp'])

        # contar_registros(database_path, 'cpv2020_manzana_servicios_de_salud')

        

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
            u"Mexico",
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

    sql_query = """
        CREATE TABLE marginacion AS
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
        """

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
    ejecuta(valores)