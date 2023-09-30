# -*- coding: utf-8 -*-


# SCRIPT PARA renombrar_capaS.

import arcpy

def renomb(caparen, nuevonomb):
    mxd = arcpy.env.mxd          # Obtener acceso al documento actual
    capas = arcpy.mapping.ListLayers(mxd)
    for capa in capas:
        print capa.name
        if capa.name == caparen:
            capa.name = nuevonomb
            print(capa.name + " renombrada correctamente")
            arcpy.RefreshActiveView()
