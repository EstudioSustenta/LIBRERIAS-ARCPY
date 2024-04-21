# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys
import os
import datetime



# Obtener acceso al documento actual
mxd = arcpy.env.mxd
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'cargar_capas' cargada con éxito")

def carga_capas(ruta_arch, nombre_capa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_ccapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'carga_capas' iniciando ...")
    log.log(repet,u"Ruta de archivo: " + ruta_arch)
    log.log(repet,u"Capa: " + nombre_capa)

    # EJEMPLO: Lista de nombres de capas a agregar
    #nombres_capas = [u"emas01", u"emas02"]

    # EJEMPLO: Ruta de la carpeta donde se encuentran las capas
    #ruta_arch = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/0 UBICACION"

    try:
        # Verificar si la capa ya está agregada al mapa
        capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)
        if not capa_existente:
            log.log(repet,nombre_capa + u" no existe previamente en el dataframe, agregándolo")
            # Construir la ruta completa a la capa
            ruta_capa = ruta_arch + "/" + nombre_capa + ".shp"
            log.log(repet,u"Ruta de capa a agregar: " + ruta_capa)
            # Agregar la capa al data frame
            capa = arcpy.mapping.Layer(ruta_capa)
            arcpy.mapping.AddLayer(df, capa)
            log.log(repet,capa.name + u" agregada correctamente al dataframe")
    except Exception as e:
        log.log(repet,u">> ERROR, proceso de agregado de capa con inconsistencias")
        log.log(repet,u">> ERROR, capa: " + nombre_capa)
        log.log(repet,str(e))
    tiempo_ccapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'carga_capas': {}".format(tiempo.tiempo([tiempo_ccapa_ini,tiempo_ccapa_fin])))

    log.log(repet,u"'carga_capas' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1

def cargar(ruta_capa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_cargar_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"'cargar' iniciando para {}...".format(ruta_capa))

    try:
        # Obtener el nombre de la capa sin extensión
        nombre_capa = os.path.basename(ruta_capa)
        nombre_capa = os.path.splitext(nombre_capa)[0]

        # Verificar si la capa ya está agregada al mapa
        capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)

        if not capa_existente:
            log.log(repet,u"{} no existe previamente en el dataframe, agregándolo".format(nombre_capa))
            # Construir la ruta completa a la capa
            log.log(repet,u"Archivo a agregar: " + ruta_capa)
            # Agregar la capa al data frame
            capa = arcpy.mapping.Layer(ruta_capa)
            arcpy.mapping.AddLayer(df, capa)
            log.log(repet,u"{} agregada correctamente al dataframe".format(nombre_capa))
        else:
            log.log(repet,u"{} ya existe en el dataframe, no se agregó nuevamente".format(nombre_capa))

    except Exception as e:
        log.log(repet,u">> ERROR, proceso de agregado de capa con inconsistencias")
        log.log(repet,str(e))

    tiempo_cargar_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'cargar': {}".format(tiempo.tiempo([tiempo_cargar_ini,tiempo_cargar_fin])))

    log.log(repet,u"'cargar' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1



def remover_capas(capa_remover):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_remcapas_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"'remover_capas' iniciando para " + capa_remover + "...")

    try:
        capa = arcpy.mapping.ListLayers(mxd, capa_remover, df)[0]
        arcpy.mapping.RemoveLayer(df, capa)
        
        log.log(repet,capa_remover + u" removida exitosamente.")
    except Exception as e:
        log.log(repet,str(e))

    tiempo_remcapas_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'remover_capas': {}".format(tiempo.tiempo([tiempo_remcapas_ini,tiempo_remcapas_fin])))

    log.log(repet,u"'remover_capas' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
