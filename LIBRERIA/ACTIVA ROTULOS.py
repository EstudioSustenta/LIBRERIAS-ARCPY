# -*- coding: utf-8 -*-

import arcpy

def activar_rotulos(mapa, capa, campo_rotulo):
    # Obtiene el mapa actual
    mxd = arcpy.mapping.MapDocument(mapa)

    # Obtiene la capa activa del mapa
    capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica

    # Habilita los rótulos para la capa
    capa.showLabels = True

    # Configura la expresión de rótulo
    labelClass = capa.labelClasses[0]
    labelClass.expression = "[{}]".format(campo_rotulo)

    # Refresca la vista de datos para aplicar los cambios de rótulos

# Ejemplo de uso:
# activar_rotulos("CURRENT", "MUNICIPAL CENSO 2020 DECRETO 185","NOM_MUN")

def desactivar_rotulos(capa):
    # Obtiene el mapa actual
    mxd = arcpy.mapping.MapDocument("CURRENT")

    # Obtiene la capa activa del mapa
    capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica

    # Habilita los rótulos para la capa
    capa.showLabels = False

    # Refresca la vista de datos para aplicar los cambios de rótulos

# Ejemplo de uso:
# desactivar_rotulos("MUNICIPAL CENSO 2020 DECRETO 185")
