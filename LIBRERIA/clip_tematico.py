# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS TEMÁTICOS.

import arcpy
import importlib
import sys
import time
import datetime
import codecs

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

mxd = arcpy.env.mxd
df = arcpy.env.df

arcpy.env.overwriteOutput = True
layout_name = "Layout"

ccapas = importlib.import_module("LIBRERIA.cargar_capas")
filtro = importlib.import_module("LIBRERIA.filtro")
z_extent = importlib.import_module("LIBRERIA.zoom_extent")
formato = importlib.import_module("LIBRERIA.formato")
exportma = importlib.import_module("LIBRERIA.exportar_mapas")
act_rot = importlib.import_module("LIBRERIA.activa_rotulos")
extraedato = importlib.import_module("LIBRERIA.extrae_dato")
log = importlib.import_module("LIBRERIA.archivo_log")
leyenda = importlib.import_module("LIBRERIA.leyenda_ajuste")
transp = importlib.import_module("LIBRERIA.aplica_transparencia")

reload(ccapas)
reload(filtro)
reload(z_extent)
reload(formato)
reload(exportma)
reload(act_rot)
reload(extraedato)
reload(log)
reload(leyenda)



log.log(u"Librería 'clip_tematico' cargada con éxito")

def clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal):
    
    log.log(u"'clip_tematico' iniciando para " + tit.upper() + "...")

    rbase = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    numero_de_elementos = None

    if tipo == "nacional":          # decisión: asigna valores para la capa base del marco geográfico y el campo para los rótulos
        cbase = "ESTATAL decr185"
        campoRotulo = "NOM_ENT"
        filtr= ""
    elif tipo == "estatal":
        cbase = "MUNICIPAL CENSO 2020 DECRETO 185"
        filtr= "NOM_ENT = '" + arcpy.env.estado + "'"
        campoRotulo = "NOM_MUN"
    else:
        cbase = "MUNICIPAL CENSO 2020 DECRETO 185"
        filtr= "NOM_MUN = '" + arcpy.env.municipio + "' AND NOM_ENT = '" + arcpy.env.estado + "'"
        campoRotulo = "NOM_MUN" # CAMBIÉ EL CAMPO DE RÓTULO, ESPERO NO DÉ PROBLEMAS, EL ANTERIOR ERA "NOM_ENT"

    # proceso de capa base
    log.log(u"Cargando capa base y aplicando formato: " + cbase)
    ccapas.carga_capas(rbase, cbase)
    filtro.fil_expr(cbase, filtr)
    ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + cbase + ".lyr"
    act_rot.activar_rotulos(cbase, campoRotulo)
    
    try:
        arcpy.ApplySymbologyFromLayer_management(cbase, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología
        log.log(u"Aplicando simbología a " + cbase)
    except Exception as e:
        log.log(u"Falló aplicación de simbología en " + cbase)
        log.log(str(e))

    z_extent.zoom_extent(layout_name, cbase)   
    formato.formato_layout(tit.upper() + " A NIVEL " + tipo.upper())

    # proceso de bucle para capas de interés
    i = 0
    for ruta in rutas:
        capa = capas[i]

        log.log(u"Bucle para proceso de capa " + capa)
        
        ccapas.carga_capas(ruta, capa)
        ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + capa + ".lyr"
        try:
            arcpy.ApplySymbologyFromLayer_management(capa, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología
            log.log(u"Aplicando simbología a " + capa)
        except Exception as e:
            log.log(u"Falló aplicación de simbología en " + capa)
            log.log(str(e))

        arch = ruta + "/" + capa + ".shp"
        capasal = "Clip " + capa
        capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capasal + ".shp"
        log.log(u"rótulos en capa: " + capa + u", campo: " + ncampo[i])
        
        try:
            act_rot.activar_rotulos(capa, ncampo[i])
        except Exception as e:
            log.log(u">> ERROR: No se ha podido iniciar el proceso para rótulos en capa: " + capa + u", campo: " + ncampo[i])
            log.log(str(e))

        if tipo == "nacional":
            log.log(u"Proceso 'nacional', no se realiza clip del archivo para la capa " + capa)
        else:           # si la visualización no es nacional, hace un recorte (clip) del área de interés (estatal o municipal)
            arcpy.Clip_analysis(in_features=arch,
                clip_features=cbase,
                out_feature_class=capasalida,
                cluster_tolerance="")
            # ccapas.remover_capas(capasalida)
            numero_de_elementos = int(arcpy.GetCount_management(capasal).getOutput(0))
            log.log("elementos en clip " + tit.upper() + ":" + str(numero_de_elementos))

            if numero_de_elementos == 0 and capasalida is None:     # Se evalúa si la capa producto del clip tiene algún contenido y si el archivo existe en la carpeta de temporales
                log.log(u"La capa " + capasal + " no tiene elementos, se eliminará del dataset")
                ccapas.remover_capas(capasal)
            else:
                ccapas.remover_capas(capa)
                if tipo == "nacional":
                    gus = None
                else:
                    
                    temp1 = ruta + "/" + capa + ".shp"
                    log.log("Capa de trabajo no nacional:\t" + temp1)
                    desc = arcpy.Describe(temp1)
                    tipo_geometria = desc.shapeType
                    if not tipo_geometria == "Point":
                        capa_diss = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capa + ".shp"
                        arcpy.Dissolve_management(in_features=capasalida,
                            out_feature_class=capa_diss,
                            dissolve_field=ncampo[i],
                            statistics_fields="", 
                            multi_part="MULTI_PART", 
                            unsplit_lines="DISSOLVE_LINES")
                        ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + capa + ".lyr"
                        ccapas.remover_capas(capasal)
                    else:
                        ccapas.carga_capas(ruta, capa)
                        # print("\n\n\n capa a SIMBOLOGIZAR: " + capa)
                        # print("archivo de simbología: " + ruta_lyr)
                
                    try:
                        arcpy.ApplySymbologyFromLayer_management(capa, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología
                        
                    except Exception as e:
                        print("Falló aplicación de simbología en " + capa)
                        log.log(str(e))

        #evalúa si el tipo de geometría de la capa es tipo polígono, si es así, aplica una transparencia
        desc = arcpy.Describe(capa)
        tipo_geometria = desc.shapeType
        log.log(u"geometría tipo " + tipo_geometria)
        print(tipo_geometria)
        if tipo_geometria == "Polygon":
                transp.transp(capa, 50)

        act_rot.activar_rotulos(capa, ncampo[i])
                        
        i=i + 1

    if ordinal > 0:
        archivo = arcpy.env.carp_cliente + capa + " near.txt"
        log.log(u"Ordinal mayor que cero, se visualizarán " + str(ordinal) + " elementos para " + archivo)
        columna = 3
        extraedato.extraedato(archivo, ordinal, columna)
        
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " " + tit

    exportma.exportar(r_dest)

    # elimina todas las capas, excepto "SISTEMA"
    capas_a_mantener = []

        # Iterar a través de todas las capas en el DataFrame
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        # Verificar si el nombre de la capa es "SISTEMA"
        if lyr.name == "SISTEMA":
            capas_a_mantener.append(lyr)  # Agregar la capa a la lista de capas a mantener

        # Eliminar todas las capas del DataFrame
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        if lyr not in capas_a_mantener:
            arcpy.mapping.RemoveLayer(df, lyr)

        # Actualizar el contenido del DataFrame
    arcpy.RefreshTOC()
    
    nummapa = nummapa + 1
    arcpy.env.nummapa = nummapa 
    log.log(u"'clip temático' finalizado")

