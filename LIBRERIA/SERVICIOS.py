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
carpeta_cliente = arcpy.env.carp_cliente

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

repet = arcpy.env.repet


log.log(repet,u"Librería 'servicios.py' cargado con éxito")

def servicios(nummapa):

        arcpy.env.repet = arcpy.env.repet + 1
        repet = arcpy.env.repet

        tiempo_servicios_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
        log.log(repet,u"'servicios' iniciando...")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa del municipio:

        # Carga capa de servicios correspondiente a la ciudad
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        capaservicios = (u"{}/servicios_p.shp".format(ruta_arch))
        manz = "manzana_localidad"
        ccapas.carga_capas(ruta_arch,manz)
        simbologia.aplica_simb(manz)
        nuevomanz = (u"Manzanas urbanas")
        renombra.renomb(manz, nuevomanz)
        z_extent.zoom_extent(layout_name, "SISTEMA")
        df.scale = 7500

        # genera el clip a una distancia de cinco minutos caminando (417 metros de radio)
        distancia = u"417"
        log.log(repet,u"Distancia de análisis: {} metros".format(distancia))
        
        clipsalida = u"{}Clip manz {}.shp".format(arcpy.env.carp_temp,distancia)

        try:
                log.log(repet,u"Generando buffer de sistema a {} metros".format(distancia))
                capasalida = u"{}Buffer {}.shp".format(arcpy.env.carp_temp,distancia)
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
        
        try:
                log.log(repet,u"Generando clip de '{}' a {} metros".format(capaservicios,distancia))
                clipsalida = (u"{}Clip servicios {}".format(arcpy.env.carp_temp,distancia))
                arcpy.Clip_analysis(in_features=capaservicios,
                        clip_features=capasalida,
                        out_feature_class=clipsalida,
                        cluster_tolerance="")
                log.log(repet,u"Clip de sistema en '{}' generado con éxito".format(clipsalida))

        except Exception as e:
                log.log(repet,u">> ERROR, el proceso para generar el Clip en {} falló".format(clipsalida))
                log.log(repet,str(e))

        capaclip = "Clip servicios {}".format(distancia)
        ccapas.carga_capas("Y:/0_SIG_PROCESO/X TEMPORAL",capaclip)
        simbologia.aplica_simb2(capaclip,"Clip servicios")
        act_rot.activar_rotulos(capaclip, u"NOMGEO")
        nuevocapaclip = "Servicios a {} metros".format(distancia)
        renombra.renomb(capaclip,nuevocapaclip)

        try:
                capamanz = ("{}/{}.shp".format(ruta_arch,manz))
                clip2 = "Clip Manzanas urbanas {}".format(distancia)
                clipsalida1 = (u"{}{}.shp".format(arcpy.env.carp_temp,clip2))
                log.log(repet,u"Generando clip de '{}' a {} metros".format(capamanz,distancia))
                arcpy.Clip_analysis(in_features=capamanz,
                        clip_features=capasalida,
                        out_feature_class=clipsalida1,
                        cluster_tolerance="")
                log.log(repet,u"Clip de sistema en '{}' generado con éxito".format(clipsalida1))

        except Exception as e:
                log.log(repet,u">> ERROR, el proceso para generar el Clip en {} falló".format(clipsalida1))
                log.log(repet,str(e))
        
        ccapas.carga_capas("Y:/0_SIG_PROCESO/X TEMPORAL",clip2)
        z_extent.zoom_extent(layout_name, clip2)
        simbologia.aplica_simb2(clip2,"Manzanas urbanas servicios")
        transp.transp(clip2,50)
        nuevobuff =("Buffer de {} metros".format(distancia))
        renombra.renomb(clip2, nuevobuff)

        # Proceso para agregar calles con nombres al mapa
        capa = "eje_vial"
        ccapas.carga_capas(ruta_arch,capa)
        act_rot.activar_rotulos(capa, u"NOMVIAL")
        simbologia.aplica_simb2(capa,"Calles")
        nuevocalles="Calles"
        renombra.renomb(capa,nuevocalles)

        formato.formato_layout(u"Servicios a 5 minutos caminando ({} metros)".format(str(distancia)))
        nombarch = u"{} {} servicios".format(arcpy.env.proyecto,str(nummapa))
        exportma.exportar(arcpy.env.carp_cliente,nombarch)

        arcpy.Near_analysis(in_features=nuevocapaclip, 
                near_features="SISTEMA", 
                search_radius="", 
                location="NO_LOCATION", 
                angle="NO_ANGLE", method="PLANAR")

        arcpy.TableToExcel_conversion(Input_Table=nuevocapaclip,
                Output_Excel_File=carpeta_cliente + " Near Servicios.xls",
                Use_field_alias_as_column_header="NAME",
                Use_domain_and_subtype_description="CODE")

        ccapas.remover_capas(nuevocapaclip)
        ccapas.remover_capas(nuevomanz)
        ccapas.remover_capas(nuevocalles)
        ccapas.remover_capas(nuevobuff)
        log.log(repet,u"'sercicios.servicios' finalizado!")

        arcpy.env.nummapa = arcpy.env.nummapa + 1

        tiempo_servicios_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
        log.log(repet,u"tiempo total de librería 'servicios': {}".format(tiempo.tiempo([tiempo_servicios_ini,tiempo_servicios_fin])))

        arcpy.env.repet = arcpy.env.repet - 1        