# -*- coding: utf-8 -*-

# SCRIPT PARA DAR FORMATO AL MAPA
# DEBE EXISTIR UN FRAMEWORK LLAMADO 'Layers', TRES OBJETOS LLAMADOS 'TITULO', 'SUBTITULO' Y 'FECHA' PARA QUE FUNCIONE ADECUADAMENTE
# DEBE TEMBIÉN CONTENER UNA LEYENDA.
# ÉSTOS DEBERÁN ESTAR EN EL LAYOUT DE ARCMAP.
import arcpy

print("RUTINA DE ASIGNACIÓN DE FORMATO CARGADA EXITOSAMENTE")

def formato_layout(subtitulo1):

    mxd = arcpy.mapping.MapDocument("current")  # Acceder al documento actual
    #df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # Obtener el primer data frame llamado "Layers"
    
    print (subtitulo1)
    
    # Acceder a elementos de diseño por su nombre
    titulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TITULO")[0]             #debe de existir el elemento de texto en layout llamado "TITULO"
    subtitulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SUBTITULO")[0]       #debe de existir el elemento de texto en layout llamado "SUBTITULO"
    tfecha = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "FECHA")[0]              #debe de existir el elemento de texto en layout llamado "FECHA"
    leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]          #debe de existir el elemento de leyenda en layout llamado "Legend"
    
    import datetime  # Importar módulo para obtener fecha y hora
    from datetime import datetime
    now = datetime.now()
    fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
    print (fecha)
    arcpy.env.fecha = fecha

    titulo.text = arcpy.env.proyecto # Actualiza el título
    subtitulo.text = subtitulo1 # Actualiza el subtítulo
    tfecha.text = fecha         # Actualiza la fecha
    leyenda.title = "SIMBOLOGÍA" # Asigna el rótulo a la simbología