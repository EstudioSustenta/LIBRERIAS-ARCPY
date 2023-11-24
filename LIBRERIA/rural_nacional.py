# -*- coding: utf-8 -*-


# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS RURALES.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import sys
import importlib
import datetime

mxd = arcpy.env.mxd
df = arcpy.env.df
    
# Agrega la ruta del paquete al path de Python
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
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'rural_nacional' se ha cargado con éxito")

def prural(nummapa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_prural_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"Iniciando 'prural'...")
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del municipio:    
    
    log.log(repet,u"Proceso de creación de mapa municipal iniciado")
    
    ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    rutarednc = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia"
    nombre_capa = u"MUNICIPAL CENSO 2020 DECRETO 185"
    ccapas.carga_capas(ruta_arch , nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    transp.transp(nombre_capa,50)
    ccapas.carga_capas(rutarednc, "red nacional de caminos")
    simbologia.aplica_simb2(u"red nacional de caminos","red nacional de caminos")
    filtr = u"\"NOM_ENT\" = '{}' AND \"NOM_MUN\" = '{}'".format(arcpy.env.estado, arcpy.env.municipio)
    filtro.fil_expr(nombre_capa, filtr)
    z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
    nombarch = u"{} {} municipio".format(arcpy.env.proyecto,str(nummapa))
    formato.formato_layout(u"UBICACIÓN A NIVEL MUNICIPIO")
    nnomb = u"Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)
    exportma.exportar(arcpy.env.carp_cliente,nombarch)
    ccapas.remover_capas(nnomb)

    log.log(repet,u"Proceso mapa Municipio finalizado!")
    nummapa = nummapa + 1

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la región:

    log.log(repet,u"Proceso de creación de mapa de región iniciado")

    escala = 50000
    ruta2 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    capa2 = u"loc_rur"
    z_extent.zoom_extent(arcpy.env.layout, u"SISTEMA")
    df.scale = escala
    ccapas.carga_capas(ruta2 , capa2)
    filtro.fil_expr(capa2, filtr)
    simbologia.aplica_simb(capa2)
    act_rot.activar_rotulos(u"loc_rur", u"NOMGEO")
    formato.formato_layout(u"UBICACIÓN A NIVEL REGIÓN")
    renombra.renomb(capa2, u"Localidades rurales")
    nombarch = u"{} {} región".format(arcpy.env.proyecto,str(nummapa))
    exportma.exportar(arcpy.env.carp_cliente,nombarch)
    nummapa = nummapa + 1
    log.log(repet,u"Proceso región finalizado!")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa de la zona:

    log.log(repet,u"Proceso de creación de mapa de zona iniciado")

    escala = 25000
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
    df.scale = escala
    formato.formato_layout(u"UBICACIÓN A NIVEL ZONA")
    act_rot.activar_rotulos(u"red nacional de caminos","NOMBRE")
    nombarch = u"{} {} zona".format(arcpy.env.proyecto,str(nummapa))
    exportma.exportar(arcpy.env.carp_cliente,nombarch)
    nummapa = nummapa + 1
    log.log(repet,u"Proceso zona finalizado!")
    
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa del sitio:

    log.log(repet,u"Proceso de creación de mapa de sitio iniciado")

    escala = 7500
    ccapas.remover_capas(u"Localidades rurales")
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")
    df.scale = escala
    formato.formato_layout(u"UBICACIÓN A NIVEL SITIO")
    nombarch = u"{} {} sitio".format(arcpy.env.proyecto,str(nummapa))
    exportma.exportar(arcpy.env.carp_cliente,nombarch)
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    ccapas.remover_capas(u"red nacional de caminos")
    ccapas.remover_capas(nnomb)
    ccapas.remover_capas(u"Manzanas urbanas")
    log.log(repet,u"Proceso Sitio finalizado!")
    nummapa = nummapa + 1
    arcpy.env.nummapa = nummapa

    tiempo_prural_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'prural': {}".format(tiempo.tiempo([tiempo_prural_ini,tiempo_prural_fin])))
    
    log.log(repet,u"'prural' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1