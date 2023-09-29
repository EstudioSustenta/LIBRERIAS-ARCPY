# -*- coding: utf-8 -*-

# SCRIPT PARA ANALIZAR LOS SERVICIOS IDENTIFICADOS POR EL INEGI EN EL SCINCE 2020.
# FUNCION: A NIVEL NACIONAL.

def servicios():

        print("iniciando proceso de servicios")

        import arcpy
        import sys
        import importlib

        layout_name = "Layout"
        mxd = arcpy.env.mxd
        df = arcpy.env.df
        carpeta_cliente = arcpy.env.carp_cliente

        ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
        sys.path.append(ruta_libreria)

        ccapas = importlib.import_module("LIBRERIA.CARGAR CAPAS")
        filtro = importlib.import_module("LIBRERIA.FILTRO")
        z_extent = importlib.import_module("LIBRERIA.ZOOM EXTENT")
        exportma = importlib.import_module("LIBRERIA.EXPORTAR MAPAS")
        formato = importlib.import_module("LIBRERIA.FORMATO")
        simbologia = importlib.import_module("LIBRERIA.SIMBOLOGIA LYR")
        transp = importlib.import_module("LIBRERIA.APLICA TRANSPARENCIA")
        act_rot = importlib.import_module("LIBRERIA.ACTIVA ROTULOS")
        renombra = importlib.import_module("LIBRERIA.RENOMBRAR CAPA")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa del municipio:

        # Carga capa de servicios correspondiente a la ciudad
        ruta_arch = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        nombre_capa = "servicios_p"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        ccapas.carga_capas(ruta_arch, "manzana_localidad")
        simbologia.aplica_simb("manzana_localidad")
        renombra.renomb(nombre_capa, "Servicios")
        renombra.renomb("manzana_localidad", "Manzanas urbanas")
        z_extent.zoom_extent(layout_name, "SISTEMA")
        df.scale = 7500
        arcpy.RefreshActiveView()

        # genera el clip a una distancia de cinco minutos caminando (417 metros de radio)
        distancia = "417"
        print(distancia)
        capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/Buffer " + distancia + ".shp"
        clipsalida = "Y:/0_SIG_PROCESO/X TEMPORAL/Clip manz " + distancia + ".shp"
        arcpy.Buffer_analysis(in_features="SISTEMA", 
                              out_feature_class=capasalida, 
                              buffer_distance_or_field= distancia + " Meters", 
                              line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                              dissolve_field="", method="PLANAR")
        capasalida = "Buffer " + distancia
        arcpy.Clip_analysis(in_features="Servicios", 
                            clip_features=capasalida, 
                            out_feature_class=clipsalida, 
                            cluster_tolerance="")

        z_extent.zoom_extent(layout_name, "Buffer " + distancia)


        ccapas.remover_capas("Servicios")

        simbologia.aplica_simb("Clip manz 417")
        act_rot.activar_rotulos("CURRENT", "Clip manz 417", "NOMGEO")
        arcpy.RefreshActiveView()
        r_dest = carpeta_cliente + arcpy.env.proyecto + "_08_servicios"
        transp.transp("Manzanas urbanas",50)
        simbologia.aplica_simb("Clip manz 417")
        simbologia.aplica_simb("Buffer " + distancia)
        formato.formato_layout("Servicios a 5 minutos caminando (" + str(distancia) + " metros)")
        exportma.exportar(r_dest)

        arcpy.Near_analysis(in_features="Clip manz 417", 
                near_features="SISTEMA", 
                search_radius="", 
                location="NO_LOCATION", 
                angle="NO_ANGLE", method="PLANAR")

        arcpy.TableToExcel_conversion(Input_Table="Clip manz 417",
                Output_Excel_File=carpeta_cliente + " Near Servicios.xls",
                Use_field_alias_as_column_header="NAME",
                Use_domain_and_subtype_description="CODE")
        ccapas.remover_capas("Clip manz " + distancia)
        ccapas.remover_capas("Manzanas urbanas")
        ccapas.remover_capas("Buffer " + distancia)
        print("Proceso \"servicios\" terminado.")