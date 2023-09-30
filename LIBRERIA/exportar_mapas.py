# -*- coding: utf-8 -*-

# SCRIPT PARA exportar_mapas A LA CARPETA POR DEFAULT
# TOMA COMO REFERENCIA LA r_dest DEFINIDA COMO VARIABLE EN LA FUNCIÓN
# GENERA DOS MAPAS CON EL NOMBRE DEL PROYECTO Y LA ESPECIALIDAD.


def exportar(r_dest):
    print(u"Iniciando proceso de exportación de mapa " + r_dest)
    import arcpy
    import importlib
    import sys

    ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
    sys.path.append(ruta_libreria)
    renombra = importlib.import_module("LIBRERIA.renombrar_capa")


    mxd = arcpy.env.mxd
    arcpy.env.overwriteOutput = True  # Permitir sobrescribir archivos de salida
    renombra.renomb("SISTEMA", arcpy.env.proyecto)
    arcpy.RefreshActiveView()  # Actualizar la vista
    # arcpy.mapping.ExportToJPEG(mxd, r_dest + ".jpg", "page_layout", 1024, 768, 250)  # Exportar a JPEG
    arcpy.mapping.ExportToPDF(mxd, r_dest + ".pdf", "page_layout", 1024, 768, 350)  # Exportar a PDF
    renombra.renomb(arcpy.env.proyecto, "SISTEMA")
    print("Mapa " + r_dest + " exportado correctamente")
