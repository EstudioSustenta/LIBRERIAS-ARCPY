# -*- coding: utf-8 -*-

# SCRIPT PARA ANALIZAR LOS servicios IDENTIFICADOS POR EL INEGI EN EL SCINCE 2020.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import sys
import importlib
import datetime

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

layout_name = u"Layout"
mxd = arcpy.env.mxd
df = arcpy.env.df
carpeta_cliente = carpeta_proy

ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")
filtro = importlib.import_module(u"LIBRERIA.filtro")
z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")
exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")
formato = importlib.import_module(u"LIBRERIA.formato")
simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")
transp = importlib.import_module(u"LIBRERIA.aplica_transparencia")
act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")
renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet         #variable para incrementar el número consecutivo del mapa.


log.log(repet,u"Librería 'denue.py' cargado con éxito")
arcpy.env.overwriteOutput = True
ruta_arch = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia".format(arcpy.env.estado)

def denue(nummapa,distancia):

        arcpy.env.repet = arcpy.env.repet + 1
        repet = arcpy.env.repet

        tiempo_denue_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
        log.log(repet,u"'servicios' iniciando...")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa del municipio:

        # Carga capa de servicios correspondiente a la ciudad
        capadenue = u"Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/" + arcpy.env.estado + "conjunto_de_datos\wgs84z13_denue.shp"
        # capadenue = (u"{}/servicios_p.shp".format(ruta_arch))
        manz = "manzana_localidad"
        ccapas.carga_capas(ruta_arch,manz)
        simbologia.aplica_simb(manz)
        nuevomanz = (u"Manzanas urbanas")
        renombra.renomb(manz, nuevomanz)
        z_extent.zoom_extent(layout_name, "SISTEMA")
        df.scale = 7500

        # genera el clip a una distancia de cinco minutos caminando (417 metros de radio)
        # distancia = u"417"
        log.log(repet,u"Distancia de análisis: {} metros".format(distancia))
        
        clipsalida = u"{}Clip manz {}.shp".format(arcpy.env.carp_temp,distancia)

        try:
                log.log(repet,u"Generando buffer de sistema a {} metros".format(distancia))
                capasalida = u"{}Denue {}.shp".format(arcpy.env.carp_temp,distancia)
                log.log(repet,u"Generando buffer de sistema a {} metros".format(distancia))
                arcpy.Buffer_analysis(in_features="SISTEMA", 
                        out_feature_class=capasalida, 
                        buffer_distance_or_field= distancia + " Meters", 
                        line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                        dissolve_field="", method="PLANAR")
                log.log(repet,u"Buffer de sistema '{}' metros generado con éxito".format(capasalida))
                
        except Exception as e:
                log.log(repet,u">> ERROR, el proceso para generar el buffer de {} falló".format(distancia))
                log.log(repet,str(e))        
        
        # try:
        #         log.log(repet,u"Generando clip de '{}' a {} metros".format(capadenue,distancia))
        #         clipsalida = (u"{}Clip denue {}".format(arcpy.env.carp_temp,distancia))
        #         arcpy.Clip_analysis(in_features=capadenue,
        #                 clip_features=capasalida,
        #                 out_feature_class=clipsalida,
        #                 cluster_tolerance="")
        #         log.log(repet,u"Clip de sistema en '{}' generado con éxito".format(clipsalida))

        # except Exception as e:
        #         log.log(repet,u">> ERROR, el proceso para generar el Clip en {}".format(capasalida))
                
        print (nummapa)