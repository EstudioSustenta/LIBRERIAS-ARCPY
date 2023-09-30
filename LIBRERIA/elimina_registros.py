# -*- coding: utf-8 -*-

# RUTINA PARA ELIMINAR LOS REGISTROS DE UNA TABLA CON UN VALOR DETERMINADO EN EL CAMPO SELECCIONADO.
# para que funcione la capa debe estar cargada en el dataframe de arcmap
# --------------------------------------------------------------------------------------------------------------------------------


# cómo elimino los registros cuyo campo 'NEAR_DIST' es igual a 'valor' usando arcpy?
# ChatGPT
# Para eliminar los registros cuyo campo 'NEAR_DIST' es igual a 'valor' en una capa 
# utilizando ArcPy, puedes utilizar la función arcpy.DeleteRows_management. Aquí tienes un ejemplo de cómo hacerlo:

import arcpy

# Ruta a la capa de interés
# capa = "Cuerpoaguaintermitente"
# campo = "NEAR_DIST"
# valor = -1

def eliminaregistros(capa, campo, valor):
    print("Eliminando registros con valor" + campo + " de la capa " + capa + "con valor = " + str(valor))

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
