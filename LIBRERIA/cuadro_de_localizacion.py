# -*- coding: utf-8 -*-

import arcpy
import sys
import importlib
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'cuadro_de_localizacion.py' cargada con éxito")

arcpy.env.overwriteOutput = True

# ----RUTINA PARA GENERAR CUADRO DE LOCALIZACIÓN DEL PROYECTO 
def dxf():

    tiempo_cuad_loc_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    try:
        log.log(u"'cuadro_de_localizacion.dxf' iniciando ...")
        
        # -------------------------------------------------------------------------------
        # Proceso para generar cuadros de localización en zonas urbanas
        
        if arcpy.env.localidad != "Zona no urbanizada":
            log.log(u"tipo de zona: '{}'".format("Zona urbanizada"))
            ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
            origmanzanas = ("Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/manzana_localidad.shp".format(arcpy.env.estado))
            distancias = (["2000"])
            manz = []
            listamanz = u""

            # bucle para generar buffers y clips de manzanas
            for distancia in distancias:
                log.log(u"Iniciando bucle para buffer de '{}' metros".format(distancia))
                log.log(u"capa para clip '{}' ".format(origmanzanas))
                capasalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/buffer " + distancia + ".shp"
                clipsalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/clip manz " + distancia + ".shp"

                try:
                    log.log(u"Generando buffer de '{}' metros".format(distancia))
                    arcpy.Buffer_analysis(in_features="SISTEMA",
                        out_feature_class=capasalida, 
                        buffer_distance_or_field= distancia + " Meters",
                        line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                        dissolve_field="", method="PLANAR")
                    log.log(u"Buffer de '{}' metros generado con éxito en '{}'".format(distancia,capasalida))
                    
                except Exception as e:
                    log.log(u">> ERROR, la generación del buffer para '{}' metros falló".format(distancia))
                    log.log(str(e))

                try:
                    log.log(u"Generando clip para '{}' con '{}'".format(origmanzanas,capasalida))
                    arcpy.Clip_analysis(in_features=origmanzanas,
                        clip_features=capasalida,
                        out_feature_class=clipsalida,
                        cluster_tolerance="")
                    log.log(u"Clip generado con éxito en '{}'".format(clipsalida))
                    
                except Exception as e:
                    log.log(u">> ERROR, la generación del clip para '{}' falló".format(clipsalida))
                    log.log(str(e))

            # Operaciones para agregar nombres de archivos a la lista 'manz'
                listamanz = clipsalida

                manz.append(listamanz)

            # Agregar 'SISTEMA' al final de la lista 'manz'
            manz.append(u"SISTEMA")

            # Crear la cadena con los nombres de los archivos separados por punto y coma
            listaarch = u';'.join(manz)

            # Mostrar y registrar la lista de archivos a convertir a DWG
            log.log(u"Archivos a convertir a DWG: '{}'".format(listaarch))
            print(listaarch)

            try:
                dwgout = (arcpy.env.carp_cliente + "cuadro_de_localizacion.DWG")
                log.log(u"Exportando DWG para '{}' en '{}'".format(listaarch,dwgout))
                arcpy.ExportCAD_conversion(in_features=listaarch,
                    Output_Type="DWG_R2013",
                    Output_File=dwgout,
                    Ignore_FileNames="Ignore_Filenames_in_Tables",
                    Append_To_Existing="Overwrite_Existing_Files",
                    Seed_File="")
                log.log(u"Archivo '{}' creado con éxito".format(dwgout))
                
            except Exception as e:
                    log.log(u">> ERROR, exportando archivos para '{}'".format(dwgout))
                    log.log(str(e))
                    
        else:
            log.log(u"Zona rural")
            ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
            ccapas.carga_capas(ruta_arch, "red nacional de caminos")
            capaentrada = u"SISTEMA"
        
            distancias = ([u"2000"])    #colocar aquí la lista de distancia (en formato texto) a las que se desea generar los buffers y clips para los archivos dwg
            manz = []
            listamanz = u""
        
            # bucle para generar buffers y clips de caminos
            for distancia in distancias:
                log.log(u"Iniciando bucle para buffer " + distancia)
                capasalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/buffer " + distancia + ".shp"
                clipsalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/clip vial " + distancia + ".shp"
                arcpy.Buffer_analysis(in_features=capaentrada, 
                                    out_feature_class=capasalida, 
                                    buffer_distance_or_field= distancia + " Meters", 
                                    line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", 
                                    dissolve_field="", method="PLANAR")
                arcpy.Clip_analysis(in_features="red nacional de caminos", 
                                    clip_features=capasalida, 
                                    out_feature_class=clipsalida, 
                                    cluster_tolerance="")
                
                ccapas.remover_capas(u"buffer " + distancia)
                listamanz = u"Y:/0_SIG_PROCESO/X TEMPORAL/clip vial " + distancia + ".shp"
                manz.append(listamanz)
        
            manz.append(u"SISTEMA")
            listaarch = u""
            listaarch = u"';'".join(manz)
            listaarch = u"\"'" + listaarch + "'\""
        
            for archivolist in listaarch:
                log.log(u"archivos a convertir a dwg: {} ".format({[archivolist]}))
            log.log(u"carpeta de cliente: " + listaarch)
        
            arcpy.ExportCAD_conversion(in_features=listaarch,
                Output_Type="DWG_R2013",
                Output_File=arcpy.env.carp_cliente + "cuadro_de_localizacion.DWG",
                Ignore_FileNames="Ignore_Filenames_in_Tables",
                Append_To_Existing="Overwrite_Existing_Files",
                Seed_File="")
            
            ccapas.remover_capas(u"cuadro_de_localizacion")
            
            for arch in manz:
                if arch != "SISTEMA":
                    ccapas.remover_capas(arch)
            ccapas.remover_capas(u"red nacional de caminos")
            
            log.log(u"'cuadro_de_localizacion.dxf' finalizado!")

    except Exception as e:
        log.log(u">> ERROR, el proceso 'cuadro_de_localizacion.dxf' falló")
        log.log(str(e))

    log.log(u"'cuadro_de_localizacion' finalizado!")
    tiempo_cuad_loc_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'dxf': {}".format(tiempo.tiempo([tiempo_cuad_loc_ini,tiempo_cuad_loc_fin])))
