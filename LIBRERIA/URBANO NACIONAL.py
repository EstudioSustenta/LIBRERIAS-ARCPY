# -*- coding: utf-8 -*-

# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS URBANAS.
# FUNCION: A NIVEL NACIONAL.
print("-------------------> PROCESO URBANO INICIADO")

import arcpy
import sys
import importlib

mxd = arcpy.env.mxd          # Obtener acceso al documento actual
df = arcpy.env.df

def purbano():

    layout_name = "Layout"
    # Agrega la ruta del paquete al path de Python
    ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON"
    sys.path.append(ruta_libreria)
    
    ccapas = importlib.import_module("LIBRERIA.CARGAR CAPAS 1_0_0")         #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
    filtro = importlib.import_module("LIBRERIA.FILTRO 1_0_0")
    z_extent = importlib.import_module("LIBRERIA.ZOOM EXTENT 1_0_0")        #carga el script para aplicar zoom extent a una capa 
    exportma = importlib.import_module("LIBRERIA.EXPORTAR MAPAS 1_0_0")     #carga el script para exportar mapas a pdf y jpg
    formato = importlib.import_module("LIBRERIA.FORMATO 1_0_0")             #carga el script para aplicar formato a layout
    simbologia = importlib.import_module("LIBRERIA.SIMBOLOGIA_LYR 1_0_0")   #carga el script para aplicar simbología a capas
    transp = importlib.import_module("LIBRERIA.APLICA TRANSPARENCIA 1_0_0")   #carga el script para aplicar transparencia a capas
    act_rot = importlib.import_module("LIBRERIA.ACTIVA ROTULOS 1_0_0")
    renombra = importlib.import_module("LIBRERIA.RENOMBRAR_CAPA_1_0_0")       #carga el script para cambiar el nombre a capas
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del municipio:    
    
    ruta_arch1 = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    nombre_capa1 = "manzana_localidad"
    ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"
    nombre_capa = "MUNICIPAL CENSO 2020 DECRETO 185"
    ccapas.carga_capas(ruta_arch , nombre_capa)
    ccapas.carga_capas(ruta_arch1, nombre_capa1)        # carga las manzanas del estado correspondiente.
    filtro.fil_expr("MUNICIPAL CENSO 2020 DECRETO 185", "NOM_MUN = '" + arcpy.env.municipio + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    z_extent.zoom_extent(layout_name, nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    simbologia.aplica_simb("manzana_localidad")
    transp.transp(nombre_capa,50)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_03_municipio"
    formato.formato_layout("UBICACIÓN A NIVEL MUNICIPIO")
    nnomb = "Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)
    renombra.renomb("manzana_localidad", "Manzanas urbanas")
    exportma.exportar(r_dest)
    ccapas.remover_capas(nnomb)
    print("Proceso Municipio terminado")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la ciudad:    

    filtro.fil_expr("Manzanas urbanas", "NOMGEO = '" + arcpy.env.localidad + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    z_extent.zoom_extent(layout_name, "Manzanas urbanas")
    transp.transp("Manzanas urbanas",50)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_04_ciudad"
    formato.formato_layout("UBICACIÓN A NIVEL CIUDAD")
    exportma.exportar(r_dest)
    print("Proceso Ciudad terminado")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la región:
    escala = 50000
    z_extent.zoom_extent(layout_name, arcpy.env.proyecto)
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_05_region"
    formato.formato_layout("UBICACIÓN A NIVEL REGIÓN")
    simbologia.aplica_simb2("red nacional de caminos","red nacional de caminos2")
    exportma.exportar(r_dest)
    print("Proceso Región terminado")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la zona:
    escala = 25000
    z_extent.zoom_extent(layout_name, arcpy.env.proyecto)
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_06_zona"
    formato.formato_layout("UBICACIÓN A NIVEL ZONA")
    # ccapas.carga_capas(ruta_arch1, nombre_capa1)
    exportma.exportar(r_dest)
    print("Proceso zona terminado")
    

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la sitio:
    escala = 7500
    rutacoloniasTmp = "Y:/0_SIG_PROCESO/X TEMPORAL/BORRACONTENIDO/Colonias.shp"
    rutacolonias = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/NUMEROSLOCOS/COLONIAS CON MPIO.shp"
    capaclip = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia/estado decr185.shp"
    arcpy.Clip_analysis(in_features=rutacolonias, clip_features=capaclip, out_feature_class=rutacoloniasTmp, cluster_tolerance="")
    simbologia.aplica_simb("Colonias")
    act_rot.activar_rotulos("CURRENT", "Colonias","COLONIA")
    z_extent.zoom_extent(layout_name, arcpy.env.proyecto)
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_07_sitio"
    formato.formato_layout("UBICACIÓN A NIVEL SITIO")
    act_rot.activar_rotulos("CURRENT", "red nacional de caminos", "NOMBRE")
    exportma.exportar(r_dest)
    ccapas.remover_capas("red nacional de caminos")
    ccapas.remover_capas("Manzanas urbanas")
    ccapas.remover_capas("Colonias")
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    arcpy.RefreshActiveView()
    print("Proceso sitio terminado")