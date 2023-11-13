# -*- coding: utf-8 -*-

import arcpy
import sys
import importlib
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

# Lista de capas a eliminar de la leyenda
# capas_a_eliminar = ["Nombre_Capa_1", "Nombre_Capa_2", "Nombre_Capa_3"]

mxd = arcpy.env.mxd


def capasleyenda(capas_a_eliminar):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_leyenda_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'elimina_capa_de_leyenda' iniciando...")

    # Obtenemos el objeto DataFrame
    data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

    # Obtenemos el objeto de la leyenda
    leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]

    try:

        # Iteramos sobre cada capa en la leyenda y la eliminamos si coincide con la lista capas_a_eliminar
        for lyr in leyenda.listLegendItemLayers():
            if lyr.name in capas_a_eliminar:
                leyenda.removeItem(lyr)
                log.log(repet,u"Se ha eliminado la capa '{}' de la leyenda con éxito.". format(lyr))

    except Exception as e:
        log.log(repet,u">> ERROR, el proceso de eliminación de capas de leyenda falló")
        log.log(repet,str(e))
    
    tiempo_leyenda_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'leyenda': {}".format(tiempo.tiempo([tiempo_leyenda_ini,tiempo_leyenda_fin])))

    log.log(repet,u"'elimina_capa_de_leyenda' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1