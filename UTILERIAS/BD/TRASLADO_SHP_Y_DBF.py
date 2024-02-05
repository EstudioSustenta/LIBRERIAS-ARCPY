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
from estados import estadosact as estados_activos
from estados import estorigdest as eod
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



# VARIABLES
estados = estados_activos()
Eods = eod()
carp_orig = 'C:/SCINCE 2020/'
carp_dest = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/'
archlog = carp_dest + '0_log_copia_origen.txt'
tablasdbf = [
    'caracteristicas_economicas.dbf',
    'discapacidad.dbf',
    'educacion.dbf',
    'etnicidad.dbf',
    'fecundidad.dbf',
    'hogares_censales.dbf',
    'migracion.dbf',
    'mortalidad.dbf',
    'poblacion.dbf',
    'religion.dbf',
    'servicios_de_salud.dbf',
    'situacion_conyugal.dbf',
    'vivienda.dbf'
               ]
grupos = [
    'ageb_urb',
    'estatal',
    'loc_rur',
    'loc_urb',
    'manzana',
    'municipal'
          ]
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
shapes = [
    'ageb_urb.shp',
    'eje_vial.shp',
    'estatal.shp',
    'loc_rur.shp',
    'loc_urb.shp',
    'manzana.shp',
    'municipal.shp',
    'servicios_a.shp',
    'servicios_l.shp',
    'servicios_p.shp',
          ]
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

# inicio de proceso para los estados seleccionados en 'estados'
for estado in estados:
    escr (archlog, u'\nEstado >>>>>>>>> {}'.format(estado))
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
    
    def crea_db(grupo):
        # Crea la(s) base(s) de datos integrando los archivos dbf, borrando de disco los archivos dfb origen
        db = u'{}{}/tablas/{}.db'.format(carp_dest,estado,grupo)
        escr(archlog, u'Proceso de creación de base de datos iniciando para {}'.format(db.upper()))
        dbdir = os.path.dirname(db)
        if not os.path.exists(dbdir):
            os.makedirs(dbdir)
            escr(archlog, u'La carpeta de la base de datos no existe, se ha creado')
        # return
        if not os.path.exists(db): # crea la base de datos si no existe
            new_db(db)
            escr(archlog, u'Se ha creado la base de datos\n{}'.format(db))
        for tabla in tablasdbf:
            if tabla == 'poblacion.dbf':
                arch_dbf = u'{}{}/cartografia/{}.dbf'.format(carp_orig, Eods[estado],grupo)
            else:
                arch_dbf = u'{}{}/tablas/cpv2020_{}_{}'.format(carp_orig, Eods[estado], grupo, tabla)
            escr(archlog, u'agregando tabla "{}" a base de datos "{}" en la tabla "{}"'.format(arch_dbf,os.path.basename(db),nicks[tabla]))
            # continue
            tablaex = edb2.existe_tabla(db, nicks[tabla])
            tabladb = (nicks['caracteristicas_economicas.dbf'])
            if not tablaex:
                add_table(arch_dbf, db, nicks[tabla])
                escr(archlog, u'La tabla {} existe en la base de datos, se ha agregado'.format(nicks[tabla]))
                registros = edb2.contar_reg_tabla(db, nicks[tabla])
                escr(archlog, u'Se han agregado {} registros a la tabla {}'.format(registros, nicks[tabla]))
            else:
                registros = edb2.contar_reg_tabla(db, tabladb)
                escr(archlog, u'La tabla {} ya existe en la base de datos con {} registros'.format(nicks[tabla], registros))
                
            reg_eco = edb2.contar_reg_tabla(db, tabladb)
            if reg_eco == registros and reg_eco > 0 and os.path.exists(arch_dbf):
                # os.remove(arch_dbf)  # esta linea elimina la tabla DBF de disco si se ha agregado correctamente a la base de datos
                escr(archlog, u'Se ha agregado la tabla "{}" a la base de datos "{}"'.format(arch_dbf,db))
            else:
                escr(archlog, u'No se ha agregado correctamente la tabla "{}" a la base de datos'.format(arch_dbf))
        escr(archlog, u'Proceso de creación de base de datos terminada para "{}"'.format(os.path.basename(db).upper()))
        
    def crea_dbs(grupos):
        escr(archlog, u'Proceso de creación de bases de datos iniciando para el estado de {}'.format(estado.upper()))
        for grupo in grupos:
            crea_db(grupo)
        escr(archlog, u'Proceso de creación de bases de datos terminada para el estado de {}'.format(estado.upper()))

    def proyecta():
        escr(archlog,u'iniciando proyección de shapefiles para {}'.format(estado))
        for shapeo in shapes:
            shaped = shape_nick[shapeo]
            shpfile_orig = u'{}/{}'.format(shp_orig,shapeo)
            shpfile_dest = u'{}/{}'.format(shp_dest,shaped)
            # escr(archlog,u'iniciando proyección de {}'.format(shpfile_dest))
            if not os.path.exists(shp_dest):
                os.makedirs(shp_dest)
                escr(archlog,u'la carpeta {} no existe, se ha creado'.format(shp_dest))
            escr(archlog, u'Proyectando {} >>> {}'.format(shpfile_orig,shpfile_dest)) 
            # continue
            escr(archlog, Utilerias_shp.proyectar(shpfile_orig, shpfile_dest, sobreescribir=True))
            if os.path.exists(shpfile_dest):
                escr(archlog,u'El archivo {} existe en disco'.format(shpfile_dest))
            else:
                escr(archlog,u'Error, el archivo {} no existe en disco'.format(shpfile_dest))
        escr(archlog,u'Proceso de proyección concluido para {}'.format(estado.upper()))

    def borracampos():
        """
        Función para borrar los campos de población del archivo manzanas
        una vez que fueron respaldados en las bases de datos correspondientes
        """
        tablasaborr = [
            # 'ageb_urb.dbf',
            # 'eje_vial.dbf',
            'estatal.dbf',
            'loc_rur.dbf',
            'loc_urb.dbf',
            'manzana_localidad.dbf',
            'municipal.dbf',
            # 'servicios_a.dbf',
            # 'servicios_l.dbf',
            # 'servicios_p.dbf',
            ]

        escr(archlog, n'Iniciando proceso de borrado de archivos para "{}"'.format(tablasaborr))

        for shape in shapes:
            shape_dbf = shape_nick[shape]
            shape_dbf = shape_dbf.split(".")[0] + '.dbf'
            # print(shape_dbf)
            if shape_dbf in tablasaborr:
                escr(archlog, n'Eliminando campos de "{}"'.format(shape_dbf))
                arch_dbf = u'{}/{}'.format(shp_dest, shape_dbf)
                # escr(archlog, u'{} >>> {} campos'.format(shape_dbf, esDBF.contar_campos_dbf(arch_dbf)))
                import campos_pob
                campos = campos_pob.campospob()
                escr(archlog, shape_dbf)
                # campos = ['POB1','POB2']
                resultado = (Utilerias_shp.elimina_campos(arch_dbf, campos))
                if resultado:
                    escr(archlog, u'Se han eliminado los campos de la tabla "{}"'.format(arch_dbf))
                else:
                    escr(archlog, u'No se han eliminado los campos de la tabla "{}"'.format(arch_dbf))
        escr(archlog,u'Proceso de borrado de campos concluido para "{}"'.format(estado.upper()))

    #-------------------------------------------------------------------------------------------------------------
    # LAS SIGUIENTE FUNCIONES NO SON PARTE DEL PROCESO DE MIGRADO DE ARCHIVOS
    # contenido() # esta línea no forma parte del proceso regular, es sólo para listar el contenido de la carpeta
    # crea_db(grupos[0])
    # copiatablas()
    # copiapob(grupos)
        

    # PROCESOS DE MIGRADO DE ARCHIVOS
    crea_dbs(grupos)    # Crea las bases de datos en el NAS
    proyecta()    # Proyecta los archivos shapefile de origen al NAS
    borracampos() # borra los campos de población en los shapefiles del NAS
    
    

