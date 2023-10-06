# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys

# Obtener acceso al documento actual
mxd = arcpy.env.mxd
df = arcpy.env.df

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"Librería 'cargar_capas' cargada con éxito")

def carga_capas(ruta_arch, nombre_capa):

    log.log(u"'carga_capas' iniciando ...")
    log.log(u"Ruta de archivo: " + ruta_arch)
    log.log(u"Capa: " + nombre_capa)

    # EJEMPLO: Lista de nombres de capas a agregar
    #nombres_capas = ["emas01", "emas02"]

    # EJEMPLO: Ruta de la carpeta donde se encuentran las capas
    #ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/0 UBICACION"

    try:
        # Verificar si la capa ya está agregada al mapa
        capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)
        if not capa_existente:
            log.log(nombre_capa.upper() + u" no existe previamente en el dataframe")
            # Construir la ruta completa a la capa
            ruta_capa = ruta_arch + "/" + nombre_capa + ".shp"
            log.log(u"Ruta de capa a agregar: " + ruta_capa)
            # Agregar la capa al data frame
            capa = arcpy.mapping.Layer(ruta_capa)
            arcpy.mapping.AddLayer(df, capa)
            log.log(capa.upper() + u" agregada correctamente al dataframe")
    except:
        log.log(u">> ERROR, no se pudo agregar la capa al dataframe")
        log.log(u">> ERROR, capa: " + nombre_capa)


    log.log(u"Proceso 'carga_capas' finalizado")




def remover_capas(capa_remover):

    log.log(u"'remover_capas' iniciando para " + capa_remover + "...")

    try:
        capa = arcpy.mapping.ListLayers(mxd, capa_remover, df)[0]
        arcpy.mapping.RemoveLayer(df, capa)
        
        log.log(capa_remover + u" removida exitosamente.")
    except Exception as e:
        print(">> ERROR: ", str(e))
    log.log(u"Proceso 'remover_capas' finalizado")