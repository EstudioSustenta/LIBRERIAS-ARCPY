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

    log.log(u"Proceso 'clip_tematico -carga_capas-' iniciando para " + nombre_capa.upper() + "...")

    # EJEMPLO: Lista de nombres de capas a agregar
    #nombres_capas = ["emas01", "emas02"]

    # EJEMPLO: Ruta de la carpeta donde se encuentran las capas
    #ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/0 UBICACION"

    
    # mxd = arcpy.mapping.MapDocument("CURRENT")

    # Obtener el data frame por su nombre
    df = arcpy.mapping.ListDataFrames(mxd, "layers")[0]

    # Verificar si la capa ya está agregada al mapa
    capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)
    if not capa_existente:
        # Construir la ruta completa a la capa
        ruta_capa = ruta_arch + "/" + nombre_capa + ".shp"
        # Agregar la capa al data frame
        capa = arcpy.mapping.Layer(ruta_capa)
        arcpy.mapping.AddLayer(df, capa)
    log.log(u"Proceso 'clip_tematico -carga_capas-' finalizado")




def remover_capas(capa_remover):

    log.log(u"Proceso 'clip_tematico -remover_capas-' iniciando para " + capa_remover + "...")

    try:
        capa = arcpy.mapping.ListLayers(mxd, capa_remover, df)[0]
        arcpy.mapping.RemoveLayer(df, capa)
        
        log.log(capa_remover + u" removida exitosamente.")
    except Exception as e:
        print("Error:", str(e))
    log.log(u"Proceso 'clip_tematico -remover_capas-' finalizado")