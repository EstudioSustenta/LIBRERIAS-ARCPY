# -*- coding: utf-8 -*-

import arcpy
import sys
import importlib
import datetime


ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'buffer_clip.py' cargado con éxito")

#RUTINA PARA GENERAR BUFFER, CLIP Y DWG DEL SISTEMA

def clipbuff(ruta, radios):
    try:
        tiempo_buf_clip_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
        log.log(u"'filtro.fil_expr' iniciando para " + ruta)
        es_sistema = u"Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA_SIMPLIFICADO.shp"
        
        mxd = arcpy.env.mxd
        df = arcpy.env.df
        manzanas = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.localidad + "/cartografia/manzana_localidad.shp"
        
        for radio in radios:
            
            radio1 = radio.replace(u"'", u"")
            clipin = ruta + "Buffer" + radio + ".shp"
            clipout = ruta + "Clip" + radio + ".shp"
            log.log(u"iniciando proceso de buffer y clips " + radio)
            arcpy.Buffer_analysis(in_features=es_sistema, out_feature_class=ruta + "Buffer" + radio1 + ".shp",
                buffer_distance_or_field=radio1 + " Meters", line_side="FULL", line_end_type="ROUND",
                dissolve_option="NONE", dissolve_field="", method="PLANAR")
            arcpy.Clip_analysis(in_features=manzanas, clip_features=clipin, out_feature_class=clipout, cluster_tolerance="")
            capa_nombre = u"Buffer" + radio1
            capa = arcpy.mapping.ListLayers(mxd, capa_nombre, df)[0]
            arcpy.mapping.RemoveLayer(df, capa)
    except Exception as e:
        log.log(u">> ERROR. Se ha producido un error aplicando 'buffer_clip.clipbuff' para: " + ruta)
        log.log(str(e))
    
    tiempo_buf_clip_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería buffer_clip.py: {}".format(tiempo.tiempo([tiempo_buf_clip_ini,tiempo_buf_clip_fin])))
    
    log.log(u"'filtro.plicar_defq' finalizado para " + ruta)

