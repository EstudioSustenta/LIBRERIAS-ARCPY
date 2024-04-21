# -*- coding: utf-8 -*-

# RUTINA PARA ELIMINAR LOS REGISTROS DE UNA TABLA CON UN VALOR DETERMINADO EN EL CAMPO SELECCIONADO.
# para que funcione la capa debe estar cargada en el dataframe de arcmap
# --------------------------------------------------------------------------------------------------------------------------------


# cómo elimino los registros cuyo campo 'NEAR_DIST' es igual a 'valor' usando arcpy?
# ChatGPT
# Para eliminar los registros cuyo campo 'NEAR_DIST' es igual a 'valor' en una capa 
# utilizando ArcPy, puedes utilizar la función arcpy.DeleteRows_management. Aquí tienes un ejemplo de cómo hacerlo:

import arcpy
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

repet = arcpy.env.repet

log.log(repet,u"Librería 'elimina_registros.py' cargado con éxito")

# Ruta a la capa de interés
# capa = u"Cuerpoaguaintermitente"
# campo = u"NEAR_DIST"
# valor = -1

def eliminaregistros(capa, campo, valor):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_elireg_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(repet,u"'elimina_registros.eliminaregistros' iniciando para {}...".format(capa))

    try:

        log.log(repet,u"Eliminando registros con valor " + campo + u" de la capa " + capa + u" con valor = u" + str(valor))

        # Crear un objeto de tabla de atributos
        tabla_atributos = arcpy.da.TableToNumPyArray(capa, [campo])

        # Filtrar los registros donde 'NEAR_DIST' es igual a valor
        registros_eliminar = [row for row in tabla_atributos if row[campo] == valor]

        # Acceder a la tabla y eliminar los registros correspondientes
        with arcpy.da.UpdateCursor(capa, [campo]) as cursor:
            for row in cursor:
                if row[0] == valor:
                    cursor.deleteRow()

        # Limpiar la selección (esto es opcional, pero es buena práctica)
        arcpy.management.SelectLayerByAttribute(capa, "CLEAR_SELECTION")

    except Exception as e:
        log.log(repet,u">> ERROR, el proceso elimina registros falló")
        log.log(repet,str(e))
    
    tiempo_elireg_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'eliminaregistros': {}".format(tiempo.tiempo([tiempo_elireg_ini,tiempo_elireg_fin])))

    log.log(repet,u"'elimina_registros.eliminaregistros' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1
