# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys
import datetime

mxd = arcpy.env.mxd

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'activa_rotulos' se ha cargado con éxito")

def activar_rotulos(capa, campo_rotulo):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_act_rot_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"Iniciando 'activar_rotulos' para '{}' con el campo '{}'...".format(capa, campo_rotulo))

    try:
        capa = arcpy.mapping.Layer(capa)
        # Habilita los rótulos para la capa
        capa.showLabels = True
        # Configura la expresión de rótulo
        labelClass = capa.labelClasses[0]
        labelClass.expression = u"[{}]".format(campo_rotulo)
        # log.log(repet,u"Rótulos activados satisfactoriamente para capa " + capa.name)
        log.log(repet,u"Rótulos activados satisfactoriamente para capa " + capa)
    except Exception as e:
        # log.log(repet,u">> ERROR, los rótulos no se han activado para capa " + capa.name)
        log.log(repet,u">> ERROR, los rótulos no se han activado para capa " + capa)
        log.log(repet,str(e))

    tiempo_act_rot_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_act_rot_ini,tiempo_act_rot_fin])))

    log.log(repet,u"'activar_rotulos' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1

def activar_rot_exp(capa, expresion):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_act_rot_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"Iniciando 'activar_rotulos' para '{}' con el campo '{}'...".format(capa, expresion))

    try:
        capa = arcpy.mapping.Layer(capa)
        # Habilita los rótulos para la capa
        capa.showLabels = True
        # Configura la expresión de rótulo
        labelClass = capa.labelClasses[0]
        labelClass.expression = u"{}".format(expresion)
        log.log(repet,u"Rótulos activados satisfactoriamente para capa " + capa.name)
    except Exception as e:
        log.log(repet,u">> ERROR, los rótulos no se han activado para capa " + capa.name)
        log.log(repet,str(e))

    tiempo_act_rot_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_act_rot_ini,tiempo_act_rot_fin])))

    log.log(repet,u"'activar_rotulos' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1


def desactivar_rotulos(capa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet
    
    tiempo_dact_rot_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"Iniciando 'desactiva_rotulos'...")

    try:
        # Obtiene la capa activa del mapa
        capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica
        # Habilita los rótulos para la capa
        capa.showLabels = False
        log.log(repet,u"Rótulos desactivados satisfactoriamente para capa " + capa.name)
    except Exception as e:
        log.log(repet,u">> ERROR, los rótulos no se han desactivado para capa " + capa.name)
        log.log(repet,str(e))

    tiempo_dact_rot_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería activa_rotulos.py: {}".format(tiempo.tiempo([tiempo_dact_rot_ini,tiempo_dact_rot_fin])))

    log.log(repet,u"'desactivar_rotulos' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1


# Ejemplo de uso:
# desactivar_rotulos(u"MUNICIPAL CENSO 2020 DECRETO 185")
