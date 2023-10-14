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
# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module("LIBRERIA.archivo_log")

log.log(u"elimina_registros.py cargado con éxito")

# Ruta a la capa de interés
# capa = "Cuerpoaguaintermitente"
# campo = "NEAR_DIST"
# valor = -1

def eliminaregistros(capa, campo, valor):

    log.log(u"'elimina_registros.eliminaregistros' iniciando...")

    try:

        log.log(u"Eliminando registros con valor " + campo + u" de la capa " + capa + u"con valor = " + str(valor))

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
        log.log(u">> ERROR, el proceso elimina registros falló")
        log.log(str(e))
    
    log.log(u"'elimina_registros.eliminaregistros' terminado")