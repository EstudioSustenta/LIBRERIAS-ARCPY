import arcpy

def leyenda(ancho, alto):
    # Obtén una referencia a la leyenda activa
    mxd = arcpy.mapping.MapDocument("CURRENT")
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]

    # Establece un ancho personalizado para el parche (patch) en la leyenda
    custom_width = ancho  # Ancho en pulgadas
    legend.defaultPatchWidth = custom_width

    # Establece una altura personalizada para el parche en la leyenda
    custom_height = alto  # Altura en pulgadas
    legend.defaultPatchHeight = custom_height

    # Actualiza la leyenda en el mapa
    arcpy.RefreshActiveView()
