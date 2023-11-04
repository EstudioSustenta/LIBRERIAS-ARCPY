# -*- coding: utf-8 -*-

# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS URBANAS.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import sys
import importlib
import datetime

global nummapa

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
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'urbano_nacional' cargada con éxito...")

def purbano(nummapa):

    tiempo_purbano_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    layout_name = u"Layout"
    log.log(u"'urbano_nacional' iniciando...")


    # proceso para cargar y dar formato a capas comunes
    ruta_manzanas = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    manzanas = u"manzana_localidad"


    ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    nombre_capa = u"MUNICIPAL CENSO 2020 DECRETO 185"
    rutarednc = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia"
    ccapas.carga_capas(ruta_arch , nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    

    filtr = "\"NOM_ENT\" = '{}' AND \"NOM_MUN\" = '{}'".format(arcpy.env.estado, arcpy.env.municipio)
    filtro.fil_expr(nombre_capa, filtr)
    z_extent.zoom_extent(layout_name, nombre_capa)
    transp.transp(nombre_capa,50)
    nnomb = u"Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)

    ccapas.carga_capas(ruta_manzanas, manzanas)
    simbologia.aplica_simb(manzanas)
    renombra.renomb(manzanas, u"Manzanas urbanas")

    ccapas.carga_capas(rutarednc, "red nacional de caminos")
    simbologia.aplica_simb2(u"red nacional de caminos","red nacional de caminos")


    def municipio(nummapa):

        log.log(u"Iniciando proceso para mapa municipal...")

        # try:
            
            # Proceso para generar mapa del municipio:    
            
        r_dest = arcpy.env.carp_cliente
        nombarch = u"{} {} municipio".format(arcpy.env.proyecto,nummapa)
        formato.formato_layout(u"UBICACIÓN A NIVEL MUNICIPIO")
        exportma.exportar(r_dest,nombarch)
        arcpy.env.nummapa = arcpy.env.nummapa + 1

    def ciudad(nummapa):

        # Proceso para generar mapa de la ciudad: 
        
        log.log(u"Iniciando proceso para mapa de ciudad...")

        try:   
            
            filtr = "\"NOM_ENT\" = '{}' AND \"NOMGEO\" = '{}'".format(arcpy.env.estado, arcpy.env.localidad)
            # filtro.fil_expr(u"Manzanas urbanas", u"NOMGEO = '" + arcpy.env.localidad + "' AND NOM_ENT = '" + arcpy.env.estado + "'")
            filtro.fil_expr(u"Manzanas urbanas", filtr)
            z_extent.zoom_extent(layout_name, "Manzanas urbanas")
            transp.transp(u"Manzanas urbanas",50)
            r_dest = arcpy.env.carp_cliente
            simbologia.aplica_simb2(u"red nacional de caminos","red nacional de caminos1")
            nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" ciudad"
            formato.formato_layout(u"UBICACIÓN A NIVEL CIUDAD")
            exportma.exportar(r_dest,nombarch)
            log.log(u"Proceso para mapa de ciudad realizado con éxito.\n")
            arcpy.env.nummapa = arcpy.env.nummapa + 1

        except Exception as e:
            log.log(u">> ERROR, el proceso para generar mapa de ciudad falló")
            log.log(str(e))

        log.log(u"Terminando proceso para ciudad\n")

    def maparegion(nummapa):

        # Proceso para generar mapa de la región:

        log.log(u"Iniciando proceso para región...")

        try:

            escala = 50000
            z_extent.zoom_extent(layout_name, "SISTEMA")
            df.scale = escala
            r_dest = arcpy.env.carp_cliente
            nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" region"
            formato.formato_layout(u"UBICACIÓN A NIVEL REGIÓN")
            exportma.exportar(r_dest,nombarch)
            log.log(u"Proceso Región finalizado!")
            arcpy.env.nummapa = arcpy.env.nummapa + 1

        except Exception as e:
            log.log(u">> ERROR, el proceso para generar mapa de región falló")
            log.log(str(e))

        log.log(u"Terminando proceso para región\n")

    def zona(nummapa):

        log.log(u"Iniciando proceso para zona...")

        # Proceso para generar mapa de la zona:

        try:

            
            escala = 25000
            z_extent.zoom_extent(layout_name, "SISTEMA")
            df.scale = escala
            r_dest = arcpy.env.carp_cliente
            nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" zona"
            formato.formato_layout(u"UBICACIÓN A NIVEL ZONA")
            exportma.exportar(r_dest,nombarch)
            arcpy.env.nummapa = arcpy.env.nummapa + 1
            log.log(u"Proceso para zona finalizado!")

        except Exception as e:
            log.log(u">> ERROR, el proceso para generar mapa de zona falló")
            log.log(str(e))
        
        log.log(u"Terminando proceso para zona\n")

    def sitio(nummapa):

        # Proceso para generar mapa de la sitio:

        log.log(u"Iniciando proceso para sitio...")

        try:

            escala = 7500
            rutacoloniasTmp = u"Y:/0_SIG_PROCESO/X TEMPORAL"
            coloniasTmp = u"Colonias"
            
            rutaccoloniasTmp = "{}/{}".format(rutacoloniasTmp,coloniasTmp)
            rutacolonias = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/NUMEROSLOCOS/COLONIAS.shp"
            capaclip = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia/estado decr185.shp"
            arcpy.Clip_analysis(in_features=rutacolonias, clip_features=capaclip, out_feature_class=rutaccoloniasTmp, cluster_tolerance="")
            ccapas.carga_capas(rutacoloniasTmp,coloniasTmp)
            simbologia.aplica_simb2(u"Colonias","Colonias")
            simbologia.aplica_simb2(u"red nacional de caminos","red nacional de caminos2")
            act_rot.activar_rotulos(u"Colonias","COLONIA")
            z_extent.zoom_extent(layout_name, "SISTEMA")
            df.scale = escala
            r_dest = arcpy.env.carp_cliente
            nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" sitio"
            formato.formato_layout(u"UBICACIÓN A NIVEL SITIO")
            act_rot.activar_rotulos(u"red nacional de caminos", u"NOMBRE")
            exportma.exportar(r_dest,nombarch)
            renombra.renomb(arcpy.env.proyecto, "SISTEMA")
            log.log(u"Proceso sitio finalizado!")
            arcpy.env.nummapa = arcpy.env.nummapa + 1
            
        except Exception as e:
            log.log(u">> ERROR, el proceso para generar mapa de sitio falló")
            log.log(str(e))

        log.log(u"Terminando proceso para sitio\n")

     # -------------------------------------------------------------------------------

    municipio(arcpy.env.nummapa)
    ciudad(arcpy.env.nummapa)
    maparegion(arcpy.env.nummapa)
    zona(arcpy.env.nummapa)
    sitio(arcpy.env.nummapa)

    ccapas.remover_capas(u"red nacional de caminos")
    ccapas.remover_capas(u"Manzanas urbanas")
    ccapas.remover_capas(u"Colonias")
    ccapas.remover_capas(nnomb)

    tiempo_purbano_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'purbano': {}".format(tiempo.tiempo([tiempo_purbano_ini,tiempo_purbano_fin])))

    log.log(u"'urbano_nacional' finalizado!")