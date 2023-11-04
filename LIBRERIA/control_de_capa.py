# -*- coding: utf-8 -*-

import arcpy
import importlib
import sys
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'control_de_capa.py' cargado con éxito")

mxd = arcpy.env.mxd         # Obtener acceso al documento actual
df = arcpy.env.df         # Obtener acceso al data frame activo

# --------------------FUNCIÓN PARA APAGAR UNA CAPA--------------------------
def apagacapa(capa_a_apagar):

    tiempo_apacacapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'apagacapa' iniciando para {}".format(capa_a_apagar))

    try:
        # Obtener acceso a la capa y apagarla
        capa = arcpy.mapping.ListLayers(mxd, capa_a_apagar, df)[0]
        capa.visible = False

        log.log(u"'apagacapa' finalizado para " + capa_a_apagar)

    except Exception as e:
        log.log(u">> ERROR, el proceso 'apagacapa' falló para " + capa_a_apagar)
        log.log(str(e))

    tiempo_apagacapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_apacacapa_ini,tiempo_apagacapa_fin])))

    log.log(u"'apagacapa' finalizado para {}".format(capa_a_apagar))

# --------------------FUNCIÓN PARA ENCENDER UNA CAPA--------------------------
def enciendecapa(capa_a_encender):

    tiempo_enciendeacapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'enciendecapa' iniciando para {}".format(capa_a_encender))
    
    try:
        # Obtener acceso a la capa y apagarla
        capa = arcpy.mapping.ListLayers(mxd, capa_a_encender, df)[0]
        capa.visible = True

        log.log(u"'enciendecapa' finalizado para " + capa_a_encender)

    except Exception as e:
    
        log.log(u">> ERROR, el proceso 'enciendecapa' falló para " + capa_a_encender)
        log.log(str(e))

    tiempo_enciendecapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería identity_sistema.py: {}".format(tiempo.tiempo([tiempo_enciendeacapa_ini,tiempo_enciendecapa_fin])))

    log.log(u"'apagacapa' finalizado para {}".format(capa_a_encender))
