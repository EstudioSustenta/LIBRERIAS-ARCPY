# -*- coding: utf-8 -*-

"""
Para ejecutarse con python 2.x
Este módulo cuenta con varias funciones para realizar acciones básicas con bases de datos sqlite.
Para la documentación de este proceso, ver el proyecto OBSIDIAN 'programacion'
"""

import sqlite3
from dbfread import DBF
from dbfpy import dbf
import os
import dbf as dbf1


# import dbfread
# import dbf

def new_db(nueva_db):
    connection = sqlite3.connect(nueva_db)
    connection.close()
    return u'Nueva base de datos creada en {}'.format(nueva_db)

def agregar_tabla_dbf_a_db1(dbf_path, sqlite_db_path, tabla_sqlite):
    """
    Esta función no pasa los ceros
    """
    # Conectar a la base de datos SQLite
    connection = sqlite3.connect(sqlite_db_path)
    # connection.set_trace_callback(print)
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
        # return

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

def agregar_tabla_dbf_a_db(dbf_file, db_file, tabla_nueva):
    """
    Esta función no pasa los acentos
    Transfiere datos desde un archivo DBF a una tabla SQLite.

    :param dbf_file: Ruta al archivo DBF.
    :param db_file: Nombre de la tabla existente en SQLite.
    :param tabla_nueva: Nombre de la tabla nueva en SQLite.
    """
    try:
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Crear una tabla en SQLite con todos los campos del archivo DBF
        dbf_table = dbf.Dbf(dbf_file)
        campos_dbf = [field.name for field in dbf_table.header.fields]
        campos_sqlite = ', '.join(campos_dbf)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                {}
            );
        '''.format(tabla_nueva, campos_sqlite))

        # Leer datos del archivo DBF y transferirlos a la tabla SQLite
        for registro in dbf_table:
            valores = tuple(str(registro[field].decode('iso-8859-1')) if isinstance(registro[field], bytes) else str(registro[field]) for field in campos_dbf)
            placeholders = ', '.join(['?'] * len(campos_dbf))
            cursor.execute('INSERT OR IGNORE INTO {} VALUES ({})'.format(tabla_nueva, placeholders), valores)

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        return(u"Transferencia completada con éxito a la tabla {}.".format(tabla_nueva))
    except sqlite3.Error as e:
        return(u"Error SQLite al transferir datos:", e)
    except Exception as e:
        return(u"Error desconocido al transferir datos:", e)

def agregar_tabla_dbf_a_db3(dbf_file, db_file, tabla_nueva):
    """
    Esta función no pasa algunas columnas del DBF
    Transfiere datos desde un archivo DBF a una tabla SQLite.

    :param dbf_file: Ruta al archivo DBF.
    :param db_file: Nombre de la tabla existente en SQLite.
    :param tabla_nueva: Nombre de la tabla nueva en SQLite.
    """
    try:
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Crear una tabla en SQLite con todos los campos del archivo DBF
        dbf_table = dbf.Dbf(dbf_file)
        campos_dbf = [field.name for field in dbf_table.header.fields]

        # Verificar si las columnas 'NOM_ENT', 'NOM_MUN' y 'NOMGEO' existen en el archivo DBF
        columnas_a_excluir = ['NOM_ENT', 'NOM_MUN', 'NOMGEO']
        campos_sqlite = [campo for campo in campos_dbf if campo not in columnas_a_excluir]
        campos_sqlite_str = ', '.join(campos_sqlite)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                {}
            );
        '''.format(tabla_nueva, campos_sqlite_str))

        # Leer datos del archivo DBF y transferirlos a la tabla SQLite
        for registro in dbf_table:
            valores = tuple(str(registro[field].decode('latin-1')) if isinstance(registro[field], bytes) else str(registro[field]) for field in campos_dbf)
            valores_sin_excluir = [valores[i] for i in range(len(valores)) if campos_dbf[i] not in columnas_a_excluir]
            placeholders = ', '.join(['?'] * len(valores_sin_excluir))
            cursor.execute('INSERT OR IGNORE INTO {} ({}) VALUES ({})'.format(tabla_nueva, campos_sqlite_str, placeholders), valores_sin_excluir)

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        print("Transferencia completada con éxito a la tabla {}.".format(tabla_nueva))
    except sqlite3.Error as e:
        print("Error SQLite al transferir datos:", e)
    except Exception as e:
        print("Error desconocido al transferir datos:", e)

def agregar_caracter_a_columna(tabla, columna):
    """
    Agrega el caracter 'a' al inicio de una columna de una tabla DBF cargada en memoria.

    :param tabla: Objeto de tabla DBF cargado en memoria.
    :param columna: Nombre de la columna a la que se le agregará el caracter.
    """
    try:
        # Verificar si la columna existe en la tabla
        if columna not in tabla.field_names:
            print("La columna '{}' no existe en la tabla.".format(columna))
            return

        # Modificar los datos en la columna
        for record in tabla:
            valor_actual = record[columna]
            if isinstance(valor_actual, str):
                record[columna] = 'a' + valor_actual
            elif isinstance(valor_actual, int):
                record[columna] = 'a' + str(valor_actual)
            # Añadir más conversiones según sea necesario para otros tipos de datos

        print("Caracter 'a' agregado al inicio de la columna '{}'.".format(columna))

    except Exception as e:
        print("Error al agregar el caracter:", e)

def contar_reg_tabla(db, tabla):
    """
    Cuenta la cantidad de registros en una tabla 'tabla'
    de la base de datos 'db'
    Returns: cantidad de registros
    """

    if os.path.exists(db) and existe_tabla(db,tabla):
    
        # Conectarse a la base de datos
        conexion = sqlite3.connect(db)

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para contar la cantidad de archivos
        cursor.execute('SELECT COUNT(*) FROM {}'.format(tabla))

        # Obtener el resultado
        cantidad_registros = cursor.fetchone()[0]

        # Cerrar la conexión
        conexion.close()

        # Imprimir la cantidad de archivos
        return cantidad_registros
    else:
        return 0

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
        # print(u"Error al verificar la existencia de la tabla: {}".format(e))
        conexion.close()
        return False

def calcular_campo(db_name, tabla_origen, campo_origen, tabla_destino, campo_destino, campo_comun):
    """
    Calcula la densidad poblacional de los shapefiles polígono de cada estado
    """
    # Conexión a la base de datos
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Seleccionar los datos necesarios de la tabla origen
    cursor.execute("SELECT {} FROM {}".format(campo_origen, tabla_origen))
    datos_origen = cursor.fetchall()

    # Iterar sobre los datos de la tabla origen y calcular el valor para el campo destino
    for dato in datos_origen:
        valor_origen = dato[0]
        
        # Obtener el valor del campo2 de tabla2 correspondiente al mismo campo_comun
        # cursor.execute(u"SELECT campo2 FROM {} WHERE {} = ?".format(tabla_destino, campo_comun), (dato[1],))
        cursor.execute(u"SELECT {} FROM {} WHERE {} = ?".format(campo_destino, tabla_destino, campo_comun), (dato[0],))

        dato_tabla2 = cursor.fetchone()
        if dato_tabla2:
            valor_destino = valor_origen * dato_tabla2[0]
            # Actualizar el campo_destino en tabla_destino
            cursor.execute("UPDATE {} SET {} = ? WHERE {} = ?".format(tabla_destino, campo_destino, campo_comun), (valor_destino, dato[1]))

    # Confirmar y cerrar la conexión
    conn.commit()
    conn.close()

def agregar_campo_y_calcular_valor(dat_accv):

    database_path = dat_accv['database_path']
    tabla = dat_accv['tabla']
    campocalc = dat_accv['campocalc']
    nvo_campo = '{}i'.format(campocalc)
    campo1 = dat_accv['campo1']
    campo2 = dat_accv['campo2']
    tabla1 = dat_accv['tabla1']
    tabla2 = dat_accv['tabla2']

    print('\n\ndb: {}\ntabla: {}\ncampo a invertir: {}\ncampo invertido: {}'.format(database_path, tabla, campocalc, nvo_campo))

    # Conectar a la base de datos
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info({})".format(tabla))
        columnas_existentes = [columna[1] for columna in cursor.fetchall()]


        if nvo_campo not in columnas_existentes:
            # Si la columna no existe, intentar agregarla
            cursor.execute("ALTER TABLE {} ADD COLUMN {};".format(tabla, nvo_campo))

            # Actualizar los valores en la nueva columna
            cursor.execute("""
                UPDATE tabla2
                SET campo_nuevo = CASE
                                    WHEN (SELECT campo1 FROM tabla1 WHERE tabla1.campo_comun = tabla2.campo_comun) < 0 THEN -6
                                    ELSE (SELECT tabla1.campo1 FROM tabla1 WHERE tabla1.campo_comun = tabla2.campo_comun) * tabla2.campo2
                                END
                WHERE EXISTS (SELECT 1 FROM tabla1 WHERE tabla1.campo_comun = tabla2.campo_comun);
            """.format(campo1))

            # Confirmar los cambios
            connection.commit()
            print("\nOperación completada con éxito. Se ha creado la columna {} en la tabla {} y se han calculado sus valores.\n".format(nvo_campo, tabla))

        else:
            print("\nLa columna {} ya existe en la tabla {}.\n".format(nvo_campo, tabla))

    except sqlite3.Error as e:
        print("Error en proceso: {}".format(e))

    finally:
        # Cerrar la conexión
        connection.close()

def verificar_columna_existente(db, tabla, columna):
    """
    Verifica si una columna existe en una tabla de una base de datos SQLite.
    Retorna True si la columna existe, False en caso contrario.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Ejecutar la pragma para obtener información sobre las columnas de la tabla
    cursor.execute("PRAGMA table_info({})".format(tabla))
    columnas = cursor.fetchall()

    # Verificar si la columna existe en la lista de columnas
    for col in columnas:
        if col[1] == columna:
            # La columna existe, cerrar la conexión y retornar True
            conn.close()
            return True

    # La columna no se encontró, cerrar la conexión y retornar False
    conn.close()
    return False

def eliminar_columna(db, tabla, columna):
    """
    Elimina una columna de una tabla en una base de datos SQLite.
    """
    try:
        if verificar_columna_existente(db, tabla, columna):
            # Conexión a la base de datos
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            # Obtener una lista de todas las columnas de la tabla original excepto la columna a eliminar
            cursor.execute("PRAGMA table_info({})".format(tabla))
            columnas = [col[1] for col in cursor.fetchall() if col[1] != columna]

            # Crear una nueva tabla sin la columna a eliminar
            nueva_definicion = ", ".join(columnas)
            cursor.execute("CREATE TABLE nueva_tabla AS SELECT {} FROM {}".format(nueva_definicion, tabla))

            # Eliminar la tabla original
            cursor.execute("DROP TABLE {}".format(tabla))

            # Renombrar la nueva tabla con el nombre de la tabla original
            cursor.execute("ALTER TABLE nueva_tabla RENAME TO {}".format(tabla))

            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()
            return u'"{}" eliminada de la tabla "{}" en "{}"'.format(columna, tabla, db)
        else:
            return u'"{}" no existe en la tabla "{}" en "{}"'.format(columna, tabla, db)
    except Exception as e:
        return e

def contar_caracteres_y_agregar_cero(sqlite_db_path, tabla, columna, longitud_minima):
    """
    Cuenta los caracteres de una columna y agrega ceros si la longitud es menor que el mínimo especificado.

    :param sqlite_db_path: Ruta de la base de datos SQLite.
    :param tabla: Nombre de la tabla en la base de datos SQLite.
    :param columna: Nombre de la columna a la que se le agregarán ceros.
    :param longitud_minima: Longitud mínima deseada para los valores de la columna.
    """
    try:
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        # Obtener los datos de la columna
        cursor.execute("SELECT {} FROM {}".format(columna, tabla))
        datos_columna = cursor.fetchall()

        # Modificar los datos de la columna
        for dato in datos_columna:
            valor_actual = str(dato[0])
            if len(valor_actual) < longitud_minima:
                ceros_agregar = longitud_minima - len(valor_actual)
                nuevo_valor = "0" * ceros_agregar + valor_actual
                cursor.execute("UPDATE {} SET {}=? WHERE {}=?".format(tabla, columna, columna), (nuevo_valor, valor_actual))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        print ("Ceros agregados a la columna '{}' si es necesario.".format(columna))

    except sqlite3.Error as e:
        print ("Error SQLite:", e)
    except Exception as e:
        print ("Error desconocido:", e)

def eliminar_caracter_de_columna(sqlite_db_path, tabla, columna, caracter_a_eliminar):
    """
    Elimina un caracter específico de una columna en una tabla de una base de datos SQLite.

    :param sqlite_db_path: Ruta de la base de datos SQLite.
    :param tabla: Nombre de la tabla en la base de datos SQLite.
    :param columna: Nombre de la columna en la tabla.
    :param caracter_a_eliminar: Caracter que se eliminará de la columna.
    """
    try:
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        # Obtener los datos de la columna
        cursor.execute("SELECT {} FROM {}".format(columna, tabla))
        datos_columna = cursor.fetchall()

        # Modificar los datos de la columna
        for dato in datos_columna:
            valor_actual = str(dato[0])
            nuevo_valor = valor_actual.replace(caracter_a_eliminar, '')
            cursor.execute("UPDATE {} SET {}=? WHERE {}=?".format(tabla, columna, columna), (nuevo_valor, valor_actual))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        print ("Caracter '{}' eliminado de la columna '{}'.".format(caracter_a_eliminar, columna))

    except sqlite3.Error as e:
        print ("Error SQLite:", e)
    except Exception as e:
        print ("Error desconocido:", e)

def sqlite_to_tabular_text(db_file, table_name, output_file):
    # Conectar a la base de datos
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Obtener los nombres de las columnas de la tabla
    cursor.execute("PRAGMA table_info({})".format(table_name))
    column_names = [col[1] for col in cursor.fetchall()]

    # Obtener los datos de la tabla
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()

    # Escribir los datos en el archivo de texto
    with open(output_file, 'w') as file:
        # Escribir encabezados de columna
        file.write('\t'.join(column_names) + '\n')
        # Escribir datos de fila
        for row in rows:
            encoded_row = [str(cell).encode('unicode_escape').decode('utf-8') for cell in row]
            file.write('\t'.join(encoded_row) + '\n')




    # Cerrar la conexión a la base de datos
    conn.close()

def obtener_tablas_sqlite(db_file):
    """
    Obtiene una lista de las tablas en una base de datos SQLite.

    Parámetros:
    - db_file (str): Ruta de la base de datos SQLite.

    Retorna:
    - Lista de nombres de tablas.
    """
    # Conectar a la base de datos
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Consulta SQL para obtener las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    # Extraer nombres de las tablas de la lista de tuplas
    nombres_tablas = [tabla[0] for tabla in tablas]

    return nombres_tablas

def contar_campos_tabla(db_file, nombre_tabla):
    """
    Cuenta el número de campos en una tabla de una base de datos SQLite.

    Parámetros:
    - db_file (str): Ruta de la base de datos SQLite.
    - nombre_tabla (str): Nombre de la tabla.

    Retorna:
    - Número de campos en la tabla.
    """
    # Conectar a la base de datos
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Obtener información de los campos de la tabla
    cursor.execute("PRAGMA table_info({})".format(nombre_tabla))
    campos_info = cursor.fetchall()

    # Contar el número de campos
    num_campos = len(campos_info)

    # Cerrar la conexión
    conn.close()

    return num_campos

def eliminar_tabla(nombre_base_datos, nombre_tabla):
    # Conexión a la base de datos
    conexion = sqlite3.connect(nombre_base_datos)
    cursor = conexion.cursor()
    
    # Sentencia SQL para eliminar la tabla
    sql = "DROP TABLE IF EXISTS {}".format(nombre_tabla)
    
    try:
        # Ejecutar la sentencia SQL
        cursor.execute(sql)
        conexion.commit()
        return("Tabla '{}' eliminada correctamente.".format(nombre_tabla))
    except sqlite3.Error as e:
        return("Error al eliminar la tabla:", e)
    finally:
        # Cerrar la conexión
        conexion.close()


if __name__ == '__main__':
    
    # Ejemplo de uso
    # sqlite_to_tabular_text('Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/tablas/municipal.db', 'conyugal', 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/tablas/datos_tabulados.txt')
    None
