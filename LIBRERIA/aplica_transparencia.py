# -*- coding: utf-8 -*-

#----> PROCESO PARA APLICAR TRANSPARENCIA A UNA capatr                       FUNCIONA

def transp(capa,transparencia):
    import arcpy
    #capatr = "manzana_localidad"
    mxd = arcpy.env.mxd
    df = arcpy.env.df
    for capatr in arcpy.mapping.ListLayers(mxd, "*", df):
        if capatr.name == capa:
            capatr.transparency = transparencia
            arcpy.RefreshActiveView()
    print("Proceso transparencia al " + str(transparencia) + "% para la capa '" + capa + "' terminado")
    
    