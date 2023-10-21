# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR CUADRO DE LOCALIZACIÓN DEL PROYECTO 
def dxf(aaa):
    print(u"Iniciando proceso de cuadro de datos")
    print(aaa)

    import arcpy
    import sys
    import importlib
    
    arcpy.env.overwriteOutput = True
    carpeta_cliente = arcpy.env.carp_cliente
    
    # Agrega la ruta del paquete al path de Python
    ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
    sys.path.append(ruta_libreria)
    
    arcpy.env.mxd = arcpy.mapping.MapDocument(u"CURRENT")                    # Obtener acceso al documento actual
    mxd = arcpy.env.mxd
    arcpy.env.df = arcpy.mapping.ListDataFrames(mxd)[0]
    df = arcpy.env.df
    
    # Importar el módulo desde el paquete LIBRERIA utilizando importlib
    ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
    
    
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de localización en zonas urbanas
    
    if arcpy.env.localidad != "Zona no urbanizada":
        print(u"Zona urbana")
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        ccapas.carga_capas(ruta_arch, "manzana_localidad")
        capaentrada = u"SISTEMA"
        distancias = ([u"2000", u"1000", u"500", u"250"])
        manz = []
        listamanz = u""

          # bucle para generar buffers y clips de manzanas
        for distancia in distancias:
            print(distancia)
            capasalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/buffer " + distancia + ".shp"
            clipsalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/clip manz " + distancia + ".shp"
            arcpy.Buffer_analysis(in_features=capaentrada, 
                out_feature_class=capasalida, 
                buffer_distance_or_field= distancia + " Meters", 
                line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                dissolve_field="", method="PLANAR")
            arcpy.Clip_analysis(in_features="manzana_localidad", 
                clip_features=capasalida, 
                out_feature_class=clipsalida, 
                cluster_tolerance="")
           
            ccapas.remover_capas(u"buffer " + distancia)
            listamanz = u"clip manz " + distancia
            manz.append(listamanz)
    
        manz.append(u"SISTEMA")
        listaarch = u""
        listaarch = u"';'".join(manz)
        listaarch = u"\"'" + listaarch + "'\""
    
        print(u"archivos a convertir a dwg " + listaarch)
    
        arcpy.ExportCAD_conversion(in_features=listaarch,
            Output_Type="DWG_R2013",
            Output_File=carpeta_cliente + "cuadro_de_localizacion.DWG",
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File="")
        
        ccapas.remover_capas(u"cuadro_de_localizacion")
        
        for arch in manz:
            if arch != "SISTEMA":
                ccapas.remover_capas(arch)
        ccapas.remover_capas(u"manzana_localidad")
    
    else:
        print(u"Zona rural")
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        ccapas.carga_capas(ruta_arch, "red nacional de caminos")
        capaentrada = u"SISTEMA"
    
        distancias = ([u"2000", u"1000", u"500", u"250"])
        manz = []
        listamanz = u""
    
        # bucle para generar buffers y clips de caminos
        for distancia in distancias:
            print(distancia)
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
    
        print(u"archivos a convertir a dwg " + listaarch)
        print(u"carpeta de cliente: " + carpeta_cliente)
    
        arcpy.ExportCAD_conversion(in_features=listaarch,
            Output_Type="DWG_R2013",
            Output_File=carpeta_cliente + "cuadro_de_localizacion.DWG",
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File="")
        
        ccapas.remover_capas(u"cuadro_de_localizacion")
        
        for arch in manz:
            if arch != "SISTEMA":
                ccapas.remover_capas(arch)
        ccapas.remover_capas(u"red nacional de caminos")