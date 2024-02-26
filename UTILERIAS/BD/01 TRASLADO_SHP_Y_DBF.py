# -*- coding: utf-8 -*-
"""
CÓDIGO A EJECUTARSE CON PYTHON 2.X
Realiza la copia y proyección de los archivos shapefile
y las tablas de las carpetas origen que genera SCINCE 2020
y las ubica en las carpetas de bases de datos de
Estudio Sustenta. adecúa los nombres de carpeta al formato
utilizado por Estudio Sustenta.
Proyecta al sistema WGS84 del sistema nativo del INEGI.
"""

"""
pasos:
1.- verificar que exista la carpeta origen (si no existe avisa y se detiene el proceso)
2.- verificar que exista la carpeta destino (de lo contrario la crea)
3.- copia las tablas (verificando que existan en origen, y destino una vez copiadas), 
    creando la carpeta en destino si no existe y eliminándola si existe
4.- crea la(s) base(s) de datos integrando los archivos dbf, borrando de disco los archivos dfb origen
5.- proyecta los archivos shapefile de origen a destino verificando que existe el shapefile destino
"""

import os
import estados as edos
from ESUSTENTA_UTILERIAS import escribearch as escr
from ESUSTENTA_UTILERIAS import eliminar_carpeta
from ESUSTENTA_UTILERIAS import copiar_carpeta
from ESUSTENTA_UTILERIAS import copiar_archivo
from ESUSTENTA_UTILERIAS import listar_carpeta
from ESUSTENTA_DB_2 import new_db
from ESUSTENTA_DB_2 import agregar_tabla_dbf_a_db as add_table
import  ESUSTENTA_DB_2 as edb2
import Utilerias_shp
import ESUSTENTA_DBF as esDBF
import ESUSTENTA_DB_2 as esDB2
import campos_pob
from Utilerias_shp import borra_campos as BC
import ESUSTENTA_UTILERIAS as ESU

# VARIABLES
estados = edos.estados()
Eods = edos.estorigdest()
carp_orig = 'C:/SCINCE 2020/'
carp_dest = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/'
archlog = carp_dest + '001_log_copia_origen.txt'
tablasdbf = edos.tablasdbf()

nicks = {
    'caracteristicas_economicas.dbf' : 'economia',
    'discapacidad.dbf' : 'discapacidad',
    'educacion.dbf' : 'educacion',
    'etnicidad.dbf' : 'etnicidad',
    'fecundidad.dbf' : 'fecundidad',
    'hogares_censales.dbf' : 'hogares',
    'migracion.dbf' : 'migracion',
    'mortalidad.dbf' : 'mortalidad',
    'poblacion.dbf' : 'poblacion',
    'religion.dbf' : 'religion',
    'servicios_de_salud.dbf' : 'salud',
    'situacion_conyugal.dbf' : 'conyugal',
    'vivienda.dbf' : 'vivienda'
}
shapes = edos.shapes()
shape_nick = {
    'ageb_urb.shp' : 'ageb_urb.shp',
    'eje_vial.shp' : 'eje_vial.shp',
    'estatal.shp' : 'estatal.shp',
    'loc_rur.shp' : 'loc_rur.shp',
    'loc_urb.shp' : 'loc_urb.shp',
    'manzana.shp' : 'manzana_localidad.shp',
    'municipal.shp' : 'municipal.shp',
    'servicios_a.shp' : 'servicios_a.shp',
    'servicios_l.shp' : 'servicios_l.shp',
    'servicios_p.shp' : 'servicios_p.shp',
            }

def impresiones():
    print('\n')
    print(estados)
    print('\n')
    print(Eods)
    print('\n')
    print(tablasdbf)
    print('\n')
    print(shapes)
    print('\n')

def procesocopiashp():
    # inicio de proceso para los estados seleccionados en 'estados'

    # Elimina el archivo log si existe en disco
    if os.path.exists(archlog):
        os.remove(archlog)
    escr(archlog, u"""
        ARCHIVO DE REPORTE DE INCIDENCIAS DE PROCESO DE COPIA Y GENERACIÓN DE BASES DE DATOS

        proceso para los estados de
        "{0}"
        Se proyectarán los archivos:
        "{3}"
        Se crearán bases de datos para los grupos:
        "{1}"
        que contendrán las tablas:
        "{2}"

        Este archivo se genera al ejecutar el código '01 TRASLADO_SHP_Y_DBF.py'
        
        Programación de código: Gustavo Martínez Velasco
        
        """.format(estados, shapes, tablasdbf, shapes))

    for estado in estados:
        escr(archlog, '=' * 120)
        escr (archlog, u'\nEstado >>>>>>>>> "{}"'.format(estado))
        carp_orig_tablas = u'{}{}/tablas'.format(carp_orig,Eods[estado])
        carp_dest_tablas = u'{}{}/tablas'.format(carp_dest,estado)
        shp_orig = u'{}{}/cartografia'.format(carp_orig,Eods[estado])
        shp_dest = u'{}{}/cartografia'.format(carp_dest,estado)

        def contenido():
            """
            Lista el contenido de la carpeta y lo imprime en consola.
            """
            archivos = listar_carpeta('Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/tablas')
            for archivo in archivos:
                print (archivo)
            
        def copiatablas():
            # verifica que no exista la carpeta 'tablas' en destino, si existe la elimina.
            if os.path.exists(carp_dest_tablas):
                escr(archlog, u'la carpeta {} ya existe, se eliminará'.format(carp_dest_tablas))
                escr(archlog, eliminar_carpeta(carp_dest_tablas))

            # copia los archivos dbf de la carpeta origen a la carpeta destino
            # print (carp_orig_tablas)
            # print (carp_dest_tablas)
            escr(archlog, copiar_carpeta(carp_orig_tablas, carp_dest_tablas))
            escr(archlog,u'Proceso de copiado de carpeta de tablas concluido para {}'.format(estado.upper()))

        def copiapob(grupos):

            # copia el archivo 'manzana.dbf' como 'cpv2020_manzana_poblacion.dbf' para su posterior uso en creacion de base de datos
            for grupo in grupos:
                pob_orig = u'{}{}/cartografia/{}.dbf'.format(carp_orig,Eods[estado],grupo)
                pob_dest = u'{}{}/tablas/cpv2020_{}_poblacion.dbf'.format(carp_dest, estado, grupo)

                escr(archlog, pob_orig)
                escr(archlog, pob_dest)
                carp_manz_dest = os.path.dirname(pob_dest)
                escr(archlog, carp_manz_dest)
                if not os.path.exists(carp_manz_dest):
                    escr(archlog, u'La carpeta>> {}\nno existe, se creará'.format(carp_manz_dest))
                    os.makedirs(carp_manz_dest)
                else:
                    escr(archlog,'La carpeta ya existe, no se ha creado')
                escr(archlog, copiar_archivo(pob_orig,pob_dest, sobreescr=True))
            escr(archlog,u'Proceso de copiado de archivo de población concluido para {}'.format(estado.upper()))

        def crea_db(grupo, tablasdbf):
            # Crea la(s) base(s) de datos integrando los archivos dbf, borrando de disco los archivos dfb origen
            db = u'{}{}/tablas/{}.db'.format(carp_dest,estado,grupo)
            escr(archlog, u'Proceso de creación de base de datos iniciando para {}'.format(db.upper()))
            dbdir = os.path.dirname(db)
            gposel = [
                'estatal',
                'loc_rur',
                'loc_urb',
                'municipal'
            ]
            if not os.path.exists(dbdir):
                os.makedirs(dbdir)
                escr(archlog, u'La carpeta de la base de datos no existe, se ha creado')
            if not os.path.exists(db): # crea la base de datos si no existe
                new_db(db)
                escr(archlog, u'Se ha creado la base de datos\n{}'.format(db))
            for tabla in tablasdbf:
                if tabla == 'poblacion.dbf' and grupo not in gposel:
                    arch_dbf = u'{}{}/cartografia/{}.dbf'.format(carp_orig, Eods[estado],grupo)
                elif tabla == 'poblacion.dbf' and grupo in gposel:
                    arch_dbf = u'{}{}/cartografia/{}_copia.dbf'.format(carp_orig, Eods[estado],grupo)
                else:
                    arch_dbf = u'{}{}/tablas/cpv2020_{}_{}'.format(carp_orig, Eods[estado], grupo, tabla)
                escr(archlog, '\n\n===={}'.format(nicks[tabla].upper()))
                if os.path.exists(arch_dbf):
                    escr(archlog, '"{}" existe'.format(arch_dbf))
                else:
                    escr(archlog, '===>>> ERROR, "{}" NO EXISTE'.format(arch_dbf))
                escr(archlog, u'Agregando tabla "{}" a base de datos "{}" en la tabla "{}"'.format(arch_dbf,os.path.basename(db),nicks[tabla]))
                tablaex = edb2.existe_tabla(db, nicks[tabla])
                tabladb = (nicks['caracteristicas_economicas.dbf'])
                if not tablaex: # Si no existe la tabla a exportar en la base de datos, la agrega

                    escr(archlog, add_table(arch_dbf, db, nicks[tabla]))
                    escr(archlog, u'La tabla {} no existe en la base de datos, se ha agregado'.format(nicks[tabla]))
                    registros = edb2.contar_reg_tabla(db, nicks[tabla])
                    escr(archlog, u'Se han agregado {} registros a la tabla {}'.format(registros, nicks[tabla]))
                else:
                    registros = edb2.contar_reg_tabla(db, tabladb)
                    escr(archlog, u'La tabla {} ya existe en la base de datos con {} registros'.format(nicks[tabla], registros))
                    
                reg_eco = edb2.contar_reg_tabla(db, tabladb)
                if reg_eco == registros and reg_eco > 0 and os.path.exists(arch_dbf):
                    escr(archlog, u'Se ha agregado la tabla "{}" a la base de datos "{}"'.format(arch_dbf,db))
                else:
                    escr(archlog, u'No se ha agregado correctamente la tabla "{}" a la base de datos'.format(arch_dbf))
            escr(archlog, u'\n\nProceso de creación de base de datos terminada para "{}"'.format(os.path.basename(db).upper()))
            
        def crea_dbs(shapes, tablasdbf):
            """
            Crea bases de datos
            """
            grupodbs={
                'estatal',
                'municipal',
                'loc_rur',
                'loc_urb',
                'ageb_urb',
                'manzana',

            }
            grupo_selecto = {
                'estatal',
                'municipal',
                'loc_rur',
                'loc_urb',
            }
            archshape = {
                'municipal': 'NOM_ENT;NOMGEO',
                'estatal': 'NOM_GEO',
                'loc_rur': 'NOM_ENT;NOM_MUN;NOMGEO',
                'loc_urb': 'NOM_ENT;NOM_MUN;NOMGEO',
            }

            escr(archlog, u'\n\n\n----------->>>Proceso de creación de bases de datos iniciando para el estado de "{}"'.format(estado.upper()))
            escr(archlog, u'Se crearán base de datos para los archivos: "{}"\n'.format(grupodbs))
            for grupo in shapes:
                escr(archlog, '-' * 120)
                if grupo in grupodbs:
                    if grupo in grupo_selecto: # para esta condición los shapefiles pasarán por un proceso de borrado de campos con acentos
                        escr(archlog, u'\n---------->>> Proceso CON copia de archivo fuente para creación de base de datos "{}"'.format(grupo))
                        shapeorig = u'{}{}/cartografia/{}.shp'.format(carp_orig, Eods[estado], grupo)
                        campos = archshape[grupo]
                        dirbase = os.path.dirname(shapeorig)
                        nombre = os.path.basename(shapeorig).split(".")[0]
                        destino = (dirbase + '/' + nombre + '_copia.shp')

                        escr(archlog, Utilerias_shp.crea(shapeorig, destino, campos))   # crea una copia del archivo origen y borra los campos definidos
                        crea_db(grupo, tablasdbf)   # crea la base de datos a partir del archivo destino
                        escr(archlog, Utilerias_shp.borrashp(destino))  # elimina el archivo destino
                    else:
                        escr(archlog, u'\n---------->>> Proceso SIN copia de archivo fuente para creación de base de datos "{}"'.format(grupo))
                        crea_db(grupo, tablasdbf)
            escr(archlog, u'\n\n\nProceso de creación de bases de datos terminada para el estado de "{}"\n\n\n'.format(estado.upper()))

        def proyecta(shapes):
            escr(archlog,u'\n\n------->>>iniciando proyección de shapefiles para "{}"'.format(estado))
            for shapeo in shapes:
                shapeo = shapeo + '.shp'
                shaped = shape_nick[shapeo]
                shpfile_orig = u'{}/{}'.format(shp_orig,shapeo)
                shpfile_dest = u'{}/{}'.format(shp_dest,shaped)
                if not os.path.exists(shp_dest):
                    os.makedirs(shp_dest)
                    escr(archlog,u'la carpeta "{}" no existe, se ha creado'.format(shp_dest))
                escr(archlog, u'Proyectando "{}" >>> "{}"'.format(shpfile_orig,shpfile_dest)) 
                escr(archlog, Utilerias_shp.proyectar(shpfile_orig, shpfile_dest, sobreescribir=True))
                if os.path.exists(shpfile_dest):
                    escr(archlog,u'El archivo "{}" existe en disco'.format(shpfile_dest))
                else:
                    escr(archlog,u'Error, el archivo "{}" no existe en disco'.format(shpfile_dest))
            escr(archlog,u'Proceso de proyección concluido para "{}"'.format(estado.upper()))

        def borracampos(shapes):
            """
            Función para borrar los campos de población del archivo manzanas
            una vez que fueron respaldados en las bases de datos correspondientes
            """
            tablasaborr = [
                'ageb_urb.dbf',
                'estatal.dbf',
                'loc_rur.dbf',
                'loc_urb.dbf',
                'manzana_localidad.dbf',
                'municipal.dbf',
                ]

            escr(archlog, u'Iniciando proceso de borrado de archivos para "{}"'.format(shapes))

            for shape in shapes:
                print(shape)
                
                shape_dbf = shape_nick[shape + '.shp']
                shape_dbf = shape_dbf.split('.')[0] + '.dbf'
                print(shape_dbf)
                if shape_dbf in tablasaborr:
                    escr(archlog, u'Eliminando campos de "{}"'.format(shape_dbf))
                    arch_dbf = u'{}/{}'.format(shp_dest, shape_dbf)
                    import campos_pob
                    campos = campos_pob.campospob()
                    escr(archlog, shape_dbf)
                    resultado = (Utilerias_shp.elimina_campos(arch_dbf, campos))
                    if resultado:
                        escr(archlog, u'Se han eliminado los campos de la tabla "{}"'.format(arch_dbf))
                    else:
                        escr(archlog, u'No se han eliminado los campos de la tabla "{}"'.format(arch_dbf))
            escr(archlog,u'Proceso de borrado de campos concluido para "{}"'.format(estado.upper()))

        def area():
            """
            Calcula el área de los polígonos
            -estado
            -municipio
            -agebs
            -loc_urb
            -manzana_localidad
            """
            escr(archlog, u'\n\n-------->>>Iniciando proceso de cálculo de área y densidad')

            from Utilerias_shp import calcula_campo_shp
            expresion = "!shape.area@hectares!"

            archivos=[
                'ageb_urb',
                'estatal',
                'municipal',
                'loc_urb',
                'manzana_localidad',
                ]
            
            for archivo in archivos:
                shapefile= u'{}{}/cartografia/{}.shp'.format(carp_dest,estado,archivo)
                if os.path.exists(shapefile):
                    escr(archlog, u'"{}" sí existe en disco'.format(shapefile))
                    escr(archlog, calcula_campo_shp(shapefile,'area_has',expresion,'PYTHON'))
                else:
                    escr(archlog, u'El archivo {} no existe en disco'.format(shapefile))
                    
        def crea_tabla_en_db(db, tablaexist, tablanva): 
            """
            Agrega los valores de la tabla dbf 'tablaexist' a una nueva tabla 'tablanva' en la base de datos 'db'
            db = ruta completa de la base de datos, incluyendo carpetas y nombre
            tablaexist = ruta completa de la tabla dbf, incluyendo carpetas y nombre
            tablanva = nombre de la nueva tabla a crear en la base de datos.
            returns: nothing
            """

            excepciones = (
                'estatal.dbf',
                'municipal.dbf',
                'loc_urb.dbf',
            )

            archshape = {
                'municipal': 'NOM_ENT;NOMGEO',
                'estatal': 'NOM_GEO',
                'loc_rur': 'NOM_ENT;NOM_MUN;NOMGEO',
                'loc_urb': 'NOM_ENT;NOM_MUN;NOMGEO',
            }
            tabla=os.path.basename(tablaexist)
            ruta=os.path.dirname(tablaexist) + "/"
            print(ruta)
            print(tabla)
            if tabla in excepciones:
                escr(archlog, u'Tabla "{}" con posibles acentos, se copiará y eliminarán los campos con acentos'.format(tabla))
                shpor=ruta + tabla.split(".")[0] + ".shp"
                shpde=ruta + tabla.split(".")[0] + "_copia.shp"
                campos=archshape[tabla.split(".")[0]]
                print(shpor)
                print(shpde)
                print(campos)
                escr(archlog, Utilerias_shp.crea(shpor, shpde, campos))   # crea una copia del archivo origen y borra los campos definidos
                print('Tabla a borrar campos: ' + tabla)
                import campos_pob
                camposaborrar=campos_pob.campospob()
                print (camposaborrar)
                escr(archlog, BC(shpde, camposaborrar))
                tablaexist = shpde.split(".")[0] + ".dbf"
                print (tablaexist)
            escr(archlog, u'\n\nProceso de creación de base de datos iniciando para {}'.format(db.upper()))
            dbdir = os.path.dirname(db)
            if not os.path.exists(dbdir): # Verifica si existe el directorio de la db, si no, lo crea
                os.makedirs(dbdir)
                escr(archlog, u'La carpeta de la base de datos no existe, se ha creado')
            if not os.path.exists(db): # crea la base de datos si no existe
                new_db(db)
                escr(archlog, u'Se ha creado la base de datos\n{}'.format(db))

            escr(archlog, u'agregando tabla "{}" a base de datos "{}" en la tabla "{}"'.format(tablaexist,os.path.basename(db),tablanva))
            tablaex = edb2.existe_tabla(db, tablanva)
            if tablaex: #si existe la tabla nueva en la DB agrega la tabla dbf
                registros = edb2.contar_reg_tabla(db, tablanva)
                escr(archlog, u'La tabla {} ya existe en la base de datos con {} registros'.format(tablanva, registros))
                escr(archlog, esDB2.eliminar_tabla(db, tablanva))
            escr(archlog, add_table(tablaexist, db, tablanva))
            registros = edb2.contar_reg_tabla(db, tablanva)
            escr(archlog, u'Se han agregado {} registros a la tabla {}'.format(registros, tablanva))
            if '_copia' in tablaexist:
                shape='{}{}'.format(ruta, shpde)
                Utilerias_shp.elimina_shp(shape)
                
            escr(archlog, u'Proceso de creación de base de datos terminada para "{}"'.format(os.path.basename(db).upper()))
            
        def geom(shapes):
            """
                Realiza el proceso de agregar tablas de geometría a las bases de datos correspondientes,
                toma los valores de la tabla dbf del archivo shapefile de los shapes,
                crea una nueva tabla en la base de datos y agrega los valores del dbf
            """
            shapesel = [
                'estatal',
                'municipal',
                'loc_urb',
                'ageb_urb',
                'manzana',
                    ]
            
            escr(archlog, u'Proceso de creación de tablas de geometría iniciando para "{0}"'.format(shapes))
            for shape in shapes:

                if shape in shapesel:
                    escr(archlog, u'Creando tabla "{0}"'.format(shape))            
                    db = u'{}{}/tablas/{}.db'.format(carp_dest,estado,shape)
                    if shape == 'manzana':
                        shape = 'manzana_localidad'
                    tablaex = u'{}{}/cartografia/{}.dbf'.format(carp_dest,estado,shape)
                    if os.path.exists(db) and os.path.exists(tablaex):
                        tablanva = 'geometria'
                        crea_tabla_en_db(db, tablaex, tablanva)
                        escr(archlog, u'Tabla "{1}" creada en: "{0}"'.format(shape, tablanva))
                    else:
                        escr(archlog, u'La base de datos o la tabla dbf no existes')

                escr(archlog, u'Proceso de creación de tablas de geometría terminado para "{0}"'.format(shapes))

        def densidad(grupos):
            """
            Calcula la densidad poblacional en la tabla geometria de cada base de datos
            
            """
            tabla_pob = 'poblacion'
            campo_pob = 'POB1'
            tabla_geom = 'geometria'
            campo_area = 'area_has'
            campo_destino = 'dens_pob'
            campo_comun = 'CVEGEO'

            for grupo in grupos:
                db = u'{0}{1}/tablas/{2}.db'.format(carp_dest, estado, grupo)
                if os.path.exists(db) and edb2.existe_tabla(db,tabla_pob) and grupo == 'municipal':
                    escr(archlog, edb2.calcular_densidad_poblacional(db, tabla_pob, campo_pob, tabla_geom, campo_area, campo_comun, campo_destino))
                else:
                    escr(archlog, u'No se puede procesar "{0}"'.format(grupo))

        def borracopias(shp_dest):
            for archivo in ESU.listar_archivos(shp_dest):
                if '_copia' in archivo:
                    escr(archlog, u'archivo a borrar: "{}"'.format(archivo))
                    os.remove(shp_dest + '/' + archivo)
                    if not os.path.exists(archivo):
                        escr(archlog, u'Archivo eliminado satisfactoriamente de disco')
                    else:
                        escr(archlog, u'>>>>> ERROR: El archivo no ha podido ser eliminado de disco')

        #-------------------------------------------------------------------------------------------------------------
        # LAS SIGUIENTE FUNCIONES NO SON PARTE DEL PROCESO DE MIGRADO DE ARCHIVOS
        # contenido() # esta línea no forma parte del proceso regular, es sólo para listar el contenido de la carpeta
        # crea_db(grupos[0])
        # copiatablas()
        # copiapob(grupos)


        # PROCESOS DE MIGRADO DE ARCHIVOS
        proyecta(shapes)    # Proyecta los archivos shapefile de origen al NAS
        area()          # Calcula el área y la densidad de los polígonos en los shapefiles seleccionados
        crea_dbs(shapes, tablasdbf)    # Crea las bases de datos en el NAS
        borracampos(shapes) # borra los campos de población en los shapefiles del NAS
        geom(shapes) # crea tablas de geometria en las bases de datos correspondientes
        borracopias(shp_dest)

        escr(archlog, u'\n\n\nproceso de traslado y creación de bases de datos terminado en archivo: \n"{}"\n\n\n'.format(archlog))

if __name__ == '__main__':
    # impresiones()
    procesocopiashp()