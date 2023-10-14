# -*- coding: utf-8 -*-


# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS RURALES.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import sys
import importlib

mxd = arcpy.env.mxd
df = arcpy.env.df
    
# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
    
ccapas = importlib.import_module("LIBRERIA.cargar_capas")
filtro = importlib.import_module("LIBRERIA.filtro")
z_extent = importlib.import_module("LIBRERIA.zoom_extent")
exportma = importlib.import_module("LIBRERIA.exportar_mapas")
formato = importlib.import_module("LIBRERIA.formato")
simbologia = importlib.import_module("LIBRERIA.simbologia_lyr")
transp = importlib.import_module("LIBRERIA.aplica_transparencia")
act_rot = importlib.import_module("LIBRERIA.activa_rotulos")
renombra = importlib.import_module("LIBRERIA.renombrar_capa")
log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"Librería 'rural_nacional' se ha cargado con éxito")

def prural(nummapa):

    log.log(u"Iniciando 'prural'...")
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del municipio:    
    
    log.log(u"Proceso de creación de mapa municipal iniciado")
    
    ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"
    nombre_capa = "MUNICIPAL CENSO 2020 DECRETO 185"
    ccapas.carga_capas(ruta_arch , nombre_capa)
    filtro.fil_expr("MUNICIPAL CENSO 2020 DECRETO 185", "NOM_MUN = '" + arcpy.env.municipio + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    transp.transp(nombre_capa,50)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " municipio"
    formato.formato_layout("UBICACIÓN A NIVEL MUNICIPIO")
    nnomb = "Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)
    exportma.exportar(r_dest)
    ccapas.remover_capas(nnomb)

    log.log(u"Proceso Municipio terminado")
    nummapa = nummapa + 1

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la región:

    log.log(u"Proceso de creación de mapa de región iniciado")

    escala = 50000
    ruta2 = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    capa2 = "loc_rur"
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
    df.scale = escala
    ccapas.carga_capas(ruta2 , capa2)
    filtro.fil_expr(capa2, "NOM_MUN = '" + arcpy.env.municipio + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
    simbologia.aplica_simb(capa2)
    act_rot.activar_rotulos("loc_rur", "NOMGEO")
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " region"
    formato.formato_layout("UBICACIÓN A NIVEL REGIÓN")
    simbologia.aplica_simb2("red nacional de caminos","red nacional de caminos1")
    renombra.renomb(capa2, "Localidades rurales")
    exportma.exportar(r_dest)
    nummapa = nummapa + 1
    log.log(u"Proceso región terminado")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la zona:

    log.log(u"Proceso de creación de mapa de zona iniciado")

    escala = 25000
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " zona"
    formato.formato_layout("UBICACIÓN A NIVEL ZONA")
    act_rot.activar_rotulos("red nacional de caminos","NOMBRE")
    exportma.exportar(r_dest)
    nummapa = nummapa + 1
    log.log(u"Proceso zona terminado")
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del sitio:

    log.log(u"Proceso de creación de mapa de sitio iniciado")

    escala = 7500
    ccapas.remover_capas("Localidades rurales")
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
    df.scale = escala
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " sitio"
    formato.formato_layout("UBICACIÓN A NIVEL SITIO")
    exportma.exportar(r_dest)
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    ccapas.remover_capas("red nacional de caminos")
    ccapas.remover_capas(nnomb)
    ccapas.remover_capas("Manzanas urbanas")
    print("Proceso Sitio terminado")
    nummapa = nummapa + 1
    arcpy.env.nummapa = nummapa

    log.log(u"Proceso sitio terminado")

    
    log.log(u"'prural' terminado...")