# -*- coding: utf-8 -*-

import arcpy

#RUTINA PARA GENERAR BUFFER, CLIP Y DWG DEL SISTEMA

def clipbuff(ruta, radios):
    es_sistema = "Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA_SIMPLIFICADO.shp"
    
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    manzanas = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.localidad + "/cartografia/manzana_localidad.shp"

    for radio in radios:
        
        radio1 = radio.replace("'", "")
        clipin = ruta + "Buffer" + radio + ".shp"
        clipout = ruta + "Clip" + radio + ".shp"
        print("iniciando proceso de buffer y clips " + radio)
        arcpy.Buffer_analysis(in_features=es_sistema, out_feature_class=ruta + "Buffer" + radio1 + ".shp", 
            buffer_distance_or_field=radio1 + " Meters", line_side="FULL", line_end_type="ROUND",
            dissolve_option="NONE", dissolve_field="", method="PLANAR")
        arcpy.Clip_analysis(in_features=manzanas, clip_features=clipin, out_feature_class=clipout, cluster_tolerance="")
        capa_nombre = "Buffer" + radio1
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre, df)[0]
        arcpy.mapping.RemoveLayer(df, capa)
    



