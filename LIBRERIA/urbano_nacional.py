# -*- coding: utf-8 -*-

# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS URBANAS.
# FUNCION: A NIVEL NACIONAL.
print(u"-------------------> PROCESO URBANO INICIADO")

import arcpy
import sys
import importlib

mxd = arcpy.env.mxd          # Obtener acceso al documento actual
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")           #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
filtro = importlib.import_module(u"LIBRERIA.filtro")
z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")          #carga el script para aplicar zoom extent a una capa 
exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")       #carga el script para exportar mapas a pdf y jpg
formato = importlib.import_module(u"LIBRERIA.formato")               #carga el script para aplicar formato a layout
simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")     #carga el script para aplicar simbología a capas
transp = importlib.import_module(u"LIBRERIA.aplica_transparencia")   #carga el script para aplicar transparencia a capas
act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")
renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")       #carga el script para cambiar el nombre a capas
log = importlib.import_module(u"LIBRERIA.archivo_log")

def purbano(nummapa):

    layout_name = u"Layout"
    log.log(u"'urbano_nacional' iniciando...")
    
    
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del municipio:    
    
    log.log(u"Iniciando proceso para municipio...")
    ruta_arch1 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    nombre_capa1 = u"manzana_localidad"
    ruta_arch = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"
    nombre_capa = u"MUNICIPAL CENSO 2020 DECRETO 185"
    ccapas.carga_capas(ruta_arch , nombre_capa)
    ccapas.carga_capas(ruta_arch1, nombre_capa1)        # carga las manzanas del estado correspondiente.
    filtro.fil_expr(u"MUNICIPAL CENSO 2020 DECRETO 185", u"NOM_MUN = '" + arcpy.env.municipio + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    z_extent.zoom_extent(layout_name, nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    simbologia.aplica_simb(u"manzana_localidad")
    transp.transp(nombre_capa,50)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + str(nummapa) + " municipio"
    formato.formato_layout(u"UBICACIÓN A NIVEL MUNICIPIO")
    nnomb = u"Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)
    renombra.renomb(u"manzana_localidad", u"Manzanas urbanas")
    exportma.exportar(r_dest)
    ccapas.remover_capas(nnomb)
    nummapa = nummapa + 1
    log.log(u"Terminando proceso para municipio")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la ciudad:    

    log.log(u"Iniciando proceso para mapa de ciudad...")
    filtro.fil_expr(u"Manzanas urbanas", u"NOMGEO = '" + arcpy.env.localidad + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    z_extent.zoom_extent(layout_name, "Manzanas urbanas")
    transp.transp(u"Manzanas urbanas",50)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " ciudad"
    formato.formato_layout(u"UBICACIÓN A NIVEL CIUDAD")
    exportma.exportar(r_dest)
    log.log(u"Terminando proceso para mapa de ciudad")
    nummapa = nummapa + 1

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la región:

    log.log(u"Iniciando proceso para región...")
    escala = 50000
    z_extent.zoom_extent(layout_name, "SISTEMA")
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " region"
    formato.formato_layout(u"UBICACIÓN A NIVEL REGIÓN")
    simbologia.aplica_simb2(u"red nacional de caminos","red nacional de caminos2")
    exportma.exportar(r_dest)
    print(u"Proceso Región terminado")
    nummapa = nummapa + 1

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la zona:

    log.log(u"Iniciando proceso para zona...")
    escala = 25000
    z_extent.zoom_extent(layout_name, "SISTEMA")
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " zona"
    formato.formato_layout(u"UBICACIÓN A NIVEL ZONA")
    # ccapas.carga_capas(ruta_arch1, nombre_capa1)
    exportma.exportar(r_dest)
    nummapa = nummapa + 1
    log.log(u"Terminando proceso para zona...")


    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la sitio:

    log.log(u"Iniciando proceso para sitio...")
    escala = 7500
    rutacoloniasTmp = u"Y:/0_SIG_PROCESO/X TEMPORAL/BORRACONTENIDO/Colonias.shp"
    rutacolonias = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/NUMEROSLOCOS/COLONIAS CON MPIO.shp"
    capaclip = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia/estado decr185.shp"
    arcpy.Clip_analysis(in_features=rutacolonias, clip_features=capaclip, out_feature_class=rutacoloniasTmp, cluster_tolerance="")
    simbologia.aplica_simb(u"Colonias")
    act_rot.activar_rotulos(u"Colonias","COLONIA")
    z_extent.zoom_extent(layout_name, "SISTEMA")
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " sitio"
    formato.formato_layout(u"UBICACIÓN A NIVEL SITIO")
    act_rot.activar_rotulos(u"red nacional de caminos", u"NOMBRE")
    exportma.exportar(r_dest)
    ccapas.remover_capas(u"red nacional de caminos")
    ccapas.remover_capas(u"Manzanas urbanas")
    ccapas.remover_capas(u"Colonias")
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    arcpy.RefreshActiveView()
    print(u"Proceso sitio terminado")
    nummapa = nummapa + 1
    arcpy.env.nummapa = nummapa
    log.log(u"Terminando proceso para sitio")

    log.log(u"'urbano_nacional' terminado")