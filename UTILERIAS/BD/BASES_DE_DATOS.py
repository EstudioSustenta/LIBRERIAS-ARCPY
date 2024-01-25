# -*- coding: utf-8 -*-

import pandas as pd
from dbfread import DBF
import sqlite3 as sql
import traceback
from simpledbf import Dbf5
import dbf
import time
import os
import sys

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS"
sys.path.append(ruta_libreria)
from sustentalyb import escribearch as escr


def creacmpo():

    inicio = time.time()

    # Ruta al archivo DBF
    ruta_dbf = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Yucatan/tablas/cpv2020_manzana_viviendaCopy.dbf'

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

    print (df)

    # Guarda el DataFrame actualizado en el archivo DBF original usando dbfpy
    dbf_writer = dbf.Writer(ruta_dbf)
    dbf_writer.fields = dbf_data.fields  # Copia la estructura de campos del archivo original
    for _, row in df.iterrows():
        dbf_writer.add_record(list(row))
    dbf_writer.close()

    # Muestra el tiempo transcurrido
    print("Tiempo transcurrido:", time.time() - inicio)
        
def combinatablas(valores):
    try:
        print("\n\n\n\n\n\nINICIANDO!!!!")
        ruta = valores['ruta']
        basededatos = valores['basededatos']
        estados = valores['estados']

        print archivos_dbf

        def compacta(valores, ruta_db, estado):
            tablas = valores['tablas']
            try:

                inicio = time.time()

                def proc(valores, ruta_db, estado):    
                    
                    # Crear una conexión a la base de datos SQLite
                    with sql.connect(ruta_db) as conn:
                        # Iterar sobre las tablas DBF especificadas
                        for tabla in tablas:

                            rutatabla = u"{}{}/tablas/{}".format(valores['ruta'], estado, tabla)
                            if os.path.exists(rutatabla) and os.path.getsize(rutatabla) > 0:
                                print (u'\n\nLa tabla \n{}\nSí existe con un tamano mayor a 0 bytes'.format(rutatabla))

                                # Obtener el nombre de la tabla (sin la extensión)
                                nombre_tabla = tabla.split('.')[0]

                                # Leer el archivo DBF usando simpledbf
                                dbf_data = Dbf5(rutatabla, codec='latin-1')

                                # Convertir los datos a un DataFrame de Pandas
                                df = dbf_data.to_dataframe()

                                # Escribir el DataFrame en la base de datos SQLite
                                df.to_sql(nombre_tabla, conn, index=False, if_exists='replace')

                                print('Tabla {} cargada en la base de datos.'.format(nombre_tabla))
                            
                            else:
                                print (u'\n\nLa tabla \n{}\nno existe. No se puede agragar a la base de datos'.format(rutatabla))

                    if os.path.exists(ruta_db) and os.path.getsize(ruta_db) > 0:
                        print (u'\nLa base de datos existe, iniciando proceso de borrado de tablas origen\n')
                        for tabla in tablas:
                            rutatabla = "{}{}/tablas/{}".format(valores['ruta'], estado, tabla)
                            print('borrando tabla {}'.format(rutatabla))
                            os.remove(rutatabla)
                            if not os.path.exists(rutatabla):
                                print(u'La tabla se ha eliminado satisfactoriamente del disco')
                            else:
                                print('La tabla existe, el borrado no fue exitoso')

                if (not os.path.exists(ruta_db)) or (os.path.getsize(ruta_db) == 0):
                    print(u'el archivo no existe o tiene un tamaño = 0 bits, se creará')
                    proc(valores, ruta_db, estado)

                else:
                    print('escapando')
                    respuesta = raw_input(u'\n\nLa base de datos \n{}\nya existe con un tamano mayor a 0 bytes, sobreescribirla? (s/n)...'.format(ruta_db))
                    if respuesta.lower() == 's':
                        print('\nIniciando proceso de sobreescritura de la base de datos\n')
                        os.remove(ruta_db)
                        proc(valores, ruta_db, estado)
                    
                    else:
                        print (u'el archivo no se sobreescribirá')
                
                tiempo_transcurrido = time.time() - inicio
                print('Tiempo transcurrido en {}: {} segundos'.format(estado, tiempo_transcurrido))

            except Exception as e:
                print("\n\nError durante el proceso: {}".format(str(traceback.format_exc())))

        for estado in estados:
            print("\n")
            print (estado)
            
            ruta_db = '{}{}/{}_{}'.format(ruta,estado,estado,basededatos)

            print (u'Ruta de base de datos: {}'.format(ruta_db))
            # print (u'Base de datos: {}'.format(basededatos))

            compacta(valores, ruta_db, estado)

        print ('\nproceso terminado.\n\n')

    except Exception as err:
        print(u">> ERROR DE PROCESO.\n {}\n".format(str(traceback.print_exc())))

    #-------------------------------------------------------------------------------------------

def combinatablascampos(valores):
    """
    
    # Esta función crea una nueva tabla en una base de datos en base a otras tablas de la misma base de datos
    transfiriendo las columnas seleccionadas, las tablas y sus campos se envían en forma de diccionario
    en la variable 'columnas_seleccionadas'

    """
    try:
        print("\n\n\n\n\n\nINICIANDO!!!!")
        archivos_dbf = valores['tablas']
        ruta = valores['ruta']
        tabladest = valores['tabladest']
        basededatos = valores['basededatos']
        ruta_destinodb = valores['ruta_destinodb']

        print archivos_dbf

        # DataFrame inicial
        df_inicial = pd.DataFrame()

        # Itera sobre la lista de archivos dbf
        for archivo_dbf in archivos_dbf:

            # Selecciona columnas específicas para cada tabla, modificar de acuerdo a las necesidades.
            columnas_seleccionadas = {
                u'cpv2020_manzana_poblacion.dbf': ['CVEGEO', 'POB1', 'POB42', 'POB84'], #, 'POB2', 'POB4', 'POB5', 'POB7', 'POB9', 'POB13', 'POB30', 'POB31', 'POB32', 'POB33', 'POB34', 'POB35', 'POB36', 'POB36_a', 'POB37', 'POB38', 'POB39', 'POB40', 'POB41'],
                u'cpv2020_manzana_caracteristicas_economicas.dbf': ['CVEGEO', 'ECO1_R', 'ECO2_R', 'ECO3_R', 'ECO25_R', 'ECO26_R', 'ECO27_R'],
                # 'cpv2020_manzana_discapacidad.dbf': ['CVEGEO'],
                u'cpv2020_manzana_educacion.dbf': ['CVEGEO', 'EDU46_R', 'EDU47_R', 'EDU48_R'],
                # 'cpv2020_manzana_etnicidad.dbf': ['CVEGEO', 'INDI1', 'INDI10', 'afro1'],
                # 'cpv2020_manzana_fecundidad.dbf': ['CVEGEO', 'FEC1_R', 'FEC2_R'],
                # 'cpv2020_manzana_hogares_censales.dbf': ['CVEGEO'],
                # 'cpv2020_manzana_migracion.dbf': ['CVEGEO'],
                # 'cpv2020_manzana_mortalidad.dbf': ['CVEGEO'],
                # 'cpv2020_manzana_religion.dbf': ['CVEGEO'],
                u'cpv2020_manzana_servicios_de_salud.dbf': ['CVEGEO', 'SALUD2_R'],
                # 'cpv2020_manzana_situacion_conyugal.dbf': ['CVEGEO'],
                u'cpv2020_manzana_vivienda.dbf': ['CVEGEO', 'VIV0', 'VIV7_R', 'VIV10_R', 'VIV14_R', 'VIV16_R', 'VIV18_R', 'VIV21_R', 'VIV24_R', 'VIV26_R', 'VIV30_R', 'VIV31_R', 'VIV39_R', 'VIV40_R', 'VIV41_R', 'VIV42_R']
                # Agrega más tablas y columnas según sea necesario
                }


                # poblacion = ('POB1',  'POB42',  'POB84', 'POB2', 'POB4', 'POB5', 'POB7', 'POB9', 'POB13', 'POB30', 'POB31', 'POB32', 'POB33', 'POB34', 'POB35', 'POB36', 'POB36_a', 'POB37', 'POB38', 'POB39', 'POB40', 'POB41')
                # educacion = ('EDU46_R', 'EDU47_R', 'EDU48_R')
                # vivienda = ('VIV0', 'VIV7_R', 'VIV10_R', 'VIV14_R', 'VIV16_R', 'VIV18_R', 'VIV21_R', 'VIV24_R', 'VIV26_R', 'VIV30_R', 'VIV31_R', 'VIV39_R', 'VIV40_R', 'VIV41_R', 'VIV42_R')
                # economia = ('ECO1_R', 'ECO2_R', 'ECO3_R', 'ECO25_R', 'ECO26_R', 'ECO27_R')
                # salud = ('SALUD2_R')



            if archivo_dbf in columnas_seleccionadas:
                columnas = columnas_seleccionadas[archivo_dbf]
                print (columnas)
                dbf_file = DBF(ruta + archivo_dbf)
                df = pd.DataFrame(iter(dbf_file), columns=columnas)

                # Combina el DataFrame con el DataFrame inicial usando una columna común
                if df_inicial.empty:
                    df_inicial = df
                else:
                    df_inicial = pd.merge(df_inicial, df, on='CVEGEO', how='inner')

        # Escribe el DataFrame resultante en un archivo de base de datos .db
        ruta_db = ruta + basededatos
        with sql.connect(ruta_db) as conn:
            df_inicial.to_sql(tabladest, conn, index=False, if_exists='replace')

        print(u"\n\Tabla '{}' creada exitosamente en: {}".format(tabladest, ruta_db))
              
    except Exception as err:
        print(u">> ERROR DE PROCESO.\n {}\n".format(str(traceback.print_exc())))

def borraarchivo(estados):
    print(u'\n\nIniciando proceso de borrado\n')
    for estado in estados:
        archivo = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/cpv2020_manzana_vivienda.dbf'.format(estado)
        # print(archivo)
        if os.path.exists(archivo):
            print (u'Borrando \n{}'.format(archivo))
            os.remove(archivo)
            if not os.path.exists(archivo):
                print (u'Archivo \n{}\nborrado satisfactoriamente'.format(archivo))
            else:
                print('Error borrando el archivo')
        else:
            print(u'\nEl archivo \n{}\nno existe')

def borraarchivo1(estados):
    def eliminar(ruta, extension):
        try:
            for archivo in os.listdir(ruta):
                if archivo.endswith(extension):
                    ruta_completa = os.path.join(ruta, archivo)
                    os.remove(ruta_completa)
                    print("Archivo eliminado: {}".format(ruta_completa))
                print("Eliminación de archivos completada.")
        except Exception as e:
            print("Error al eliminar archivos: {}".format(e))

    for estado in estados:
        ruta = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/'.format(estado)
        extension = 'dcm'
        eliminar(ruta, extension)
    print('\n\nProceso terminado')

def listadetablas(valores):
    ruta_db = valores['basededatos']
    archivos_dbf = valores['archivos_dbf']

    # Ruta de tu base de datos SQLite
    ruta_db = "ruta_de_tu_base_de_datos.db"

    # Crear conexión a la base de datos
    conn = sql.connect(ruta_db)

    # Crear un objeto cursor
    cursor = conn.cursor()

    # Obtener la lista de tablas en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    # Iterar sobre las tablas y obtener la cantidad de registros
    for tabla in tablas:
        nombre_tabla = tabla[0]
        cursor.execute("SELECT COUNT(*) FROM {};".format(nombre_tabla))
        cantidad_registros = cursor.fetchone()[0]
        print(u"Tabla: {}, Registros: {}".format(nombre_tabla, cantidad_registros))

    # Cerrar la conexión
    conn.close()

def buscar_tabla(valores):
    ruta_db = valores['ruta_db']
    nombre_tabla = valores['nombre_tabla']
    # Crear conexión a la base de datos
    conn = sql.connect(ruta_db)

    # Crear un objeto cursor
    cursor = conn.cursor()

    # Verificar si la tabla existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (nombre_tabla,))
    tabla_encontrada = cursor.fetchone()

    if tabla_encontrada:
        # La tabla existe, obtener la cantidad de registros
        cursor.execute("SELECT COUNT(*) FROM {};".format(nombre_tabla))
        cantidad_registros = cursor.fetchone()[0]
        resultado = (cantidad_registros, 'existe')
    else:
        # La tabla no existe
        resultado = (0, 'no existe')

    # Cerrar la conexión
    conn.close()

    return resultado

def verificadb(valores):

    archlog = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/00_log_verif_tablas.txt'
    escr('Verificacion de tablas en bases de datos.\nGustavo Martinez\n\n','w',archlog)

    estados = valores['estados']
    tablas = valores['tablas']

    for estado in estados:
        ruta_db = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}_compendio.db'.format(estado,estado)
        
        escr('\n{}'.format(estado), 'a', archlog)
        for tabla in tablas:
            nombre_tabla = tabla.split('.')[0]
            valores2 = {'ruta_db' : ruta_db,
                        'nombre_tabla' : nombre_tabla}
            resultados = buscar_tabla(valores2)
            escr(u'\tTabla {}\t{}\t\tregistros:\t{}'.format(nombre_tabla,resultados[1],resultados[0]), 'a', archlog)
    escr('\n\n Se ha terminado la verificacion\n\n','a',archlog)

def agregar_nueva_tabla_dbf_a_sqlite(ruta_db, ruta_dbf, nombre_tabla_sqlite):
    # Conectar a la base de datos SQLite
    conn = sql.connect(ruta_db)
    cursor = conn.cursor()

    # Leer la tabla DBF
    records = list(DBF(ruta_dbf, load=True))

    # Obtener el nombre de las columnas
    columnas = records[0].keys()

    # Crear y llenar la nueva tabla en la base de datos SQLite
    cursor.execute("CREATE TABLE {} ({});".format(nombre_tabla_sqlite,', '.join(columnas)))
    cursor.executemany("INSERT INTO {} VALUES ({});".format(nombre_tabla_sqlite,', '.join(['?']*len(columnas))), [tuple(record.values()) for record in records])

    # Commit para guardar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()

def combinatablas1(valores):
    # esta función es una alternativa a combinatablas1 para tratar de no saturar la memoria
    estados = valores['estados']
    tablas = valores['tablas']
    ruta = valores['ruta']
    bd = valores['basededatos']
    for estado in estados:
        
        ruta_db = "{}{}/{}_{}".format(ruta,estado,estado,bd)
        print (u'\n\n\nestado: {}'.format(estado,ruta_db))
        for tabla in tablas:
            ruta_dbf = "{}{}/tablas/{}".format(ruta,estado,tabla)
            nombre_tabla_sqlite = tabla.split('.')[0]
            print (u'tabla dbf: {}\ntabla SQL: {}'.format(ruta_dbf,nombre_tabla_sqlite))
            agregar_nueva_tabla_dbf_a_sqlite(ruta_db, ruta_dbf, nombre_tabla_sqlite)




if __name__ == '__main__':

    # Definir valores
    archivos_dbf = [
        u'cpv2020_manzana_poblacion.dbf',
        u'cpv2020_manzana_caracteristicas_economicas.dbf',
        u'cpv2020_manzana_discapacidad.dbf',
        u'cpv2020_manzana_educacion.dbf',
        u'cpv2020_manzana_etnicidad.dbf',
        u'cpv2020_manzana_fecundidad.dbf',
        u'cpv2020_manzana_hogares_censales.dbf',
        u'cpv2020_manzana_migracion.dbf',
        u'cpv2020_manzana_mortalidad.dbf',
        u'cpv2020_manzana_religion.dbf',
        u'cpv2020_manzana_servicios_de_salud.dbf',
        u'cpv2020_manzana_situacion_conyugal.dbf',
        u'cpv2020_manzana_vivienda.dbf'
        # # Agrega más archivos según sea necesario  cpv2020_manzana_vivienda.dbf
    ]

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

    valores = {
        'ruta': u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/',
        'tablas': archivos_dbf,
        'tabladest': 'marginacion',
        'basededatos': 'Aguascalientes_compendio - copia.db',
        'ruta_destinodb': u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/',
        'estados' : estados
    }

    # Llamar a la función
    # combinatablas(valores)
    combinatablascampos(valores)
    # borraarchivo(estados)
    # combinatablas1(valores)
    # verificadb(valores)

