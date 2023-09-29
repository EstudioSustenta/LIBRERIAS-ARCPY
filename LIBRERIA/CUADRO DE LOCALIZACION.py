# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR CUADRO DE LOCALIZACIÓN DEL PROYECTO 
def dxf(aaa):
    print("Iniciando proceso de cuadro de datos")
    print(aaa)

    import arcpy
    import sys
    import importlib
    
    arcpy.env.overwriteOutput = True
    carpeta_cliente = arcpy.env.carp_cliente
    
    # Agrega la ruta del paquete al path de Python
    ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON"
    sys.path.append(ruta_libreria)
    
    arcpy.env.mxd = arcpy.mapping.MapDocument("CURRENT")                    # Obtener acceso al documento actual
    mxd = arcpy.env.mxd
    arcpy.env.df = arcpy.mapping.ListDataFrames(mxd)[0]
    df = arcpy.env.df
    
    # Importar el módulo desde el paquete LIBRERIA utilizando importlib
    ccapas = importlib.import_module("LIBRERIA.CARGAR CAPAS 1_0_0")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
    
    
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de localización en zonas urbanas
    
    if arcpy.env.localidad != "Zona no urbanizada":
        print("Zona urbana")
        ruta_arch = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        ccapas.carga_capas(ruta_arch, "manzana_localidad")
        capaentrada = "SISTEMA"
        distancias = (["2000", "1000", "500", "250"])
        manz = []
        listamanz = ""

          # bucle para generar buffers y clips de manzanas
        for distancia in distancias:
            print(distancia)
            capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/buffer " + distancia + ".shp"
            clipsalida = "Y:/0_SIG_PROCESO/X TEMPORAL/clip manz " + distancia + ".shp"
            arcpy.Buffer_analysis(in_features=capaentrada, 
                out_feature_class=capasalida, 
                buffer_distance_or_field= distancia + " Meters", 
                line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                dissolve_field="", method="PLANAR")
            arcpy.Clip_analysis(in_features="manzana_localidad", 
                clip_features=capasalida, 
                out_feature_class=clipsalida, 
                cluster_tolerance="")
           
            ccapas.remover_capas("buffer " + distancia)
            listamanz = "clip manz " + distancia
            manz.append(listamanz)
    
        manz.append("SISTEMA")
        listaarch = ""
        listaarch = "';'".join(manz)
        listaarch = "\"'" + listaarch + "'\""
    
        print("archivos a convertir a dwg " + listaarch)
    
        arcpy.ExportCAD_conversion(in_features=listaarch,
            Output_Type="DWG_R2013",
            Output_File=carpeta_cliente + "CUADRO DE LOCALIZACION.DWG",
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File="")
        
        ccapas.remover_capas("CUADRO DE LOCALIZACION")
        
        for arch in manz:
            if arch != "SISTEMA":
                ccapas.remover_capas(arch)
        ccapas.remover_capas("manzana_localidad")
    
    else:
        print("Zona rural")
        ruta_arch = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        ccapas.carga_capas(ruta_arch, "red nacional de caminos")
        capaentrada = "SISTEMA"
    
        distancias = (["2000", "1000", "500", "250"])
        manz = []
        listamanz = ""
    
        # bucle para generar buffers y clips de caminos
        for distancia in distancias:
            print(distancia)
            capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/buffer " + distancia + ".shp"
            clipsalida = "Y:/0_SIG_PROCESO/X TEMPORAL/clip vial " + distancia + ".shp"
            arcpy.Buffer_analysis(in_features=capaentrada, 
                                  out_feature_class=capasalida, 
                                  buffer_distance_or_field= distancia + " Meters", 
                                  line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", 
                                  dissolve_field="", method="PLANAR")
            arcpy.Clip_analysis(in_features="red nacional de caminos", 
                                clip_features=capasalida, 
                                out_feature_class=clipsalida, 
                                cluster_tolerance="")
            
            ccapas.remover_capas("buffer " + distancia)
            listamanz = "clip vial " + distancia
            manz.append(listamanz)
    
        manz.append("SISTEMA")
        listaarch = ""
        listaarch = "';'".join(manz)
        listaarch = "\"'" + listaarch + "'\""
    
        print("archivos a convertir a dwg " + listaarch)
    
        arcpy.ExportCAD_conversion(in_features=listaarch,
            Output_Type="DWG_R2013",
            Output_File=carpeta_cliente + "CUADRO DE LOCALIZACION.DWG",
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File="")
        
        ccapas.remover_capas("CUADRO DE LOCALIZACION")
        
        for arch in manz:
            if arch != "SISTEMA":
                ccapas.remover_capas(arch)
        ccapas.remover_capas("red nacional de caminos")