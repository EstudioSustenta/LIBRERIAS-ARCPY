# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS CON DATOS COMPLEMENTARIOS DEL INEGI
# RUTA DE LOS MAPAS:    Y:/GIS/MEXICO/VARIOS/INEGI

import arcpy
import importlib
import sys
import datetime
import os


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

mxd = arcpy.env.mxd
df = arcpy.env.df

arcpy.env.overwriteOutput = True

global act_rot
global borrainn
global ccapas
global cliptema
global escribe_archivo
global exportma
global formato
global idproy
global log
global nearexp
global renombra
global simbologia
global tiempo
global z_extent

#------------------------------> CARGA DE LIBRERÍAS <------------------------------------------

act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")
borrainn = importlib.import_module(u"LIBRERIA.borrainn")
ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")
cliptema = importlib.import_module(u"LIBRERIA.clip_tematico")
escribe_archivo = importlib.import_module(u"LIBRERIA.escribe_archivo")
exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")
formato = importlib.import_module(u"LIBRERIA.formato")
idproy = importlib.import_module(u"LIBRERIA.identity_sistema")
log = importlib.import_module(u"LIBRERIA.archivo_log")
nearexp = importlib.import_module(u"LIBRERIA.near_a_sistema")
renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")
simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")
z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")


reload(borrainn)
reload(ccapas)
reload(cliptema)
reload(escribe_archivo)
reload(idproy)
reload(log)
reload(nearexp)
reload(renombra)
reload(simbologia)
reload(tiempo)
reload(z_extent)

layout_name = u"Layout"

global repet

repet = arcpy.env.repet

#-----------------------------------------------------------------------------------------------
#------------------------------------> INICIO DE PROCESOS <-------------------------------------
#-----------------------------------------------------------------------------------------------
def borra_arch(ruta_archivo):
    try:
        log.log(repet,u"Borrando '{}'".format(ruta_archivo))
        arcpy.Delete_management(ruta_archivo)
        log.log(repet,u"'{}' borrado con éxito".format(ruta_archivo))
    except Exception as e:
        log.log(repet,u">> ERROR, No se pudo borrar {}".format(capasalida)) 

def denue(nummapa,distancia):

        arcpy.env.repet = arcpy.env.repet + 1
        repet = arcpy.env.repet

        tiempo_denue_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
        log.log(repet,u"'denue' iniciando...")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa del municipio:

        # Carga capa de servicios correspondiente a la ciudad
        capadenue = u"Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/{}/conjunto_de_datos\denue_wgs84z13.shp".format(arcpy.env.estado)
        manzanas = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/manzana_localidad.shp".format(arcpy.env.estado)
        manz = "manzana_localidad"
        ccapas.cargar(manzanas)
        simbologia.aplica_simb(manz)
        nuevomanz = (u"Manzanas urbanas")
        renombra.renomb(manz, nuevomanz)
        z_extent.zoom_extent(layout_name, "SISTEMA")
        df.scale = 2000

        # genera el clip a una distancia de cinco minutos caminando (417 metros de radio)
        log.log(repet,u"Distancia de análisis: {} metros".format(distancia))
        
        clipsalida = u"{}Clip manz {}.shp".format(arcpy.env.carp_temp,distancia)


        try:
            log.log(repet,u"Generando buffer de sistema a {} metros".format(distancia))
            capasalida = u"{}buffer_denue_{}.shp".format(arcpy.env.carp_temp,distancia)

            arcpy.Buffer_analysis(in_features="SISTEMA",
                    out_feature_class=capasalida, 
                    buffer_distance_or_field= str(distancia) + " Meters", 
                    line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                    dissolve_field="", method="PLANAR")

            log.log(repet,u"Buffer de sistema '{}' metros generado con éxito".format(capasalida))
                
        except Exception as e:
            log.log(repet,u">> ERROR, el proceso para generar el buffer de {} falló".format(distancia))
            log.log(repet,str(e))
        
        try:
            clipsalida = (u"{}Clip_denue_{}.shp".format(arcpy.env.carp_temp,distancia))
            log.log(repet,u"Generando clip de '{}-{}' a {} metros".format(arcpy.env.estado, os.path.splitext(os.path.basename(capadenue))[0],distancia))
            log.log(repet,u"Capas para clip: {}\n   capa de recorte: {}\n   Capa de salida: {}".format(capadenue, capasalida, clipsalida))
            
            arcpy.Clip_analysis(in_features=capadenue,
                    clip_features=capasalida,
                    out_feature_class=clipsalida,
                    cluster_tolerance="")

            arcpy.Near_analysis(in_features=clipsalida,
                                near_features="SISTEMA",
                                search_radius="{} Meters".format(distancia),
                                location="NO_LOCATION",
                                angle="ANGLE",
                                method="PLANAR")

            
            print("Iniciando proceso de creación de matriz, espere por favor...")
            with arcpy.da.SearchCursor(clipsalida,['NEAR_DIST',
                                                   'NEAR_ANGLE',
                                                   'nomb_scian',
                                                   'tipoUniEco',
                                                   'nom_estab',
                                                   'raz_social',
                                                   'nombre_act',
                                                   'per_ocu',
                                                   'manzana',
                                                   'telefono',
                                                   'correoelec',
                                                   'www',
                                                   'fecha_alta']) as cursor:
                archivo = "{}/Near_DENUE.txt".format(arcpy.env.carp_cliente)
                titulo = "Archivo de datos DENUE".encode('utf-8')
                campos = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    "Distancia al sistema",
                    "Ángulo",
                    "Clave y nombre SCIAN",
                    "Tipo de unidad económica",
                    "Nombre del establecimiento",
                    "Razón social",
                    "Nombre de la actividad económica",
                    "Personal ocupado",
                    "Clave de manzana",
                    "Teléfono",
                    "Correoelec",
                    "Página web",
                    "Fecha de alta")
                
                for campo in cursor:
                    lista_unid = ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                        campo[0],
                        campo[1],
                        campo[2].encode('utf-8'),
                        campo[3].encode('utf-8'),
                        campo[4].encode('utf-8'),
                        campo[5].encode('utf-8'),
                        campo[6].encode('utf-8'),
                        campo[7].encode('utf-8'),
                        campo[8].encode('utf-8'),
                        campo[9].encode('utf-8'),
                        ((campo[10]).encode('utf-8')).lower(),
                        (campo[11].encode('utf-8')).lower(),
                        campo[12].encode('utf-8')
                        ))

                    
                    escribe_archivo.texto(archivo,titulo,campos,lista_unid)

            log.log(repet,u"Clip de sistema en '{}' generado con éxito".format(clipsalida))
            borra_arch(capasalida)
            ccapas.cargar(capadenue)
            den = os.path.splitext(os.path.basename(capadenue))[0]
            simbologia.aplica_simb(den)
            act_rot.activar_rotulos(den, "scian")
            tit = u"DENUE"
            nombarch = u"{} {} {}".format(arcpy.env.proyecto,str(nummapa),tit)
            formato.formato_layout(u"UNIDADES ECONÓMICAS DENUE 2023")
            exportma.exportar(arcpy.env.carp_cliente,nombarch)
            borra_arch(clipsalida)

        except Exception as e:
            log.log(repet,u">> ERROR en el proceso para generar el Clip en {}".format(capasalida))
            log.log(repet,str(e))
