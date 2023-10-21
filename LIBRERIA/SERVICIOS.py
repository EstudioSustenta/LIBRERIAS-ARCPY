# -*- coding: utf-8 -*-

# SCRIPT PARA ANALIZAR LOS servicios IDENTIFICADOS POR EL INEGI EN EL SCINCE 2020.
# FUNCION: A NIVEL NACIONAL.

def servicios(nummapa):

        print(u"iniciando proceso de servicios")

        import arcpy
        import sys
        import importlib

        layout_name = u"Layout"
        mxd = arcpy.env.mxd
        df = arcpy.env.df
        carpeta_cliente = arcpy.env.carp_cliente

        ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
        sys.path.append(ruta_libreria)

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

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa del municipio:

        # Carga capa de servicios correspondiente a la ciudad
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
        nombre_capa = u"servicios_p"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        ccapas.carga_capas(ruta_arch, "manzana_localidad")
        simbologia.aplica_simb(u"manzana_localidad")
        renombra.renomb(nombre_capa, "Servicios")
        renombra.renomb(u"manzana_localidad", u"Manzanas urbanas")
        z_extent.zoom_extent(layout_name, "SISTEMA")
        df.scale = 7500
        arcpy.RefreshActiveView()

        # genera el clip a una distancia de cinco minutos caminando (417 metros de radio)
        distancia = u"417"
        print(distancia)
        capasalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/Buffer " + distancia + ".shp"
        clipsalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/Clip manz " + distancia + ".shp"
        arcpy.Buffer_analysis(in_features="SISTEMA", 
                              out_feature_class=capasalida, 
                              buffer_distance_or_field= distancia + " Meters", 
                              line_side="FULL", line_end_type="ROUND", dissolve_option="NONE",
                              dissolve_field="", method="PLANAR")
        capasalida = u"Buffer " + distancia
        arcpy.Clip_analysis(in_features="Servicios", 
                            clip_features=capasalida, 
                            out_feature_class=clipsalida, 
                            cluster_tolerance="")

        z_extent.zoom_extent(layout_name, "Buffer " + distancia)


        ccapas.remover_capas(u"Servicios")

        simbologia.aplica_simb(u"Clip manz 417")
        act_rot.activar_rotulos(u"Clip manz 417", u"NOMGEO")
        arcpy.RefreshActiveView()
        r_dest = carpeta_cliente + arcpy.env.proyecto + " " + str(nummapa) + " servicios"
        transp.transp(u"Manzanas urbanas",50)
        simbologia.aplica_simb(u"Clip manz 417")
        simbologia.aplica_simb(u"Buffer " + distancia)
        formato.formato_layout(u"Servicios a 5 minutos caminando (u" + str(distancia) + " metros)")
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
        ccapas.remover_capas(u"Clip manz " + distancia)
        ccapas.remover_capas(u"Manzanas urbanas")
        ccapas.remover_capas(u"Buffer " + distancia)
        print(u"Proceso \"servicios\" terminado.")

        arcpy.env.nummapa = nummapa