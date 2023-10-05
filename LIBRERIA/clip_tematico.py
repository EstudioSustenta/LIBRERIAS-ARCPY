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

log.log(u"Librería 'clip_tematico' cargada con éxito")

def clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal):
    
    reload(exportma)

    log.log(u"Proceso clip_tematico iniciando para " + tit.upper() + "...")

    # log.log(u"rutas: " + rutas)
    # log.log(u"capas: " + capas)
    # log.log(u"tipo: " + tipo.upper())
    # log.log(u"ncampo: " + ncampo)
    # log.log(u"nummapa: " + nummapa)
    # log.log(u"ordinal: " + ordinal)

    rbase = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    numero_de_elementos = None

    if tipo == "nacional":
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
        campoRotulo = "NOM_ENT"

    # proceso de capa base
    log.log(u"Cargando capa base y aplicando formato: " + cbase)
    ccapas.carga_capas(rbase, cbase)
    filtro.fil_expr(cbase, filtr)
    ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + cbase + ".lyr"
    
    try:
        arcpy.ApplySymbologyFromLayer_management(cbase, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología
        log.log(u"Aplicando simbología a " + cbase)
    except:
        log.log(u"Falló aplicación de simbología en " + cbase)

    z_extent.zoom_extent(layout_name, cbase)   

    # proceso de bucle
    i = 0
    for ruta in rutas:
        capa = capas[i]
        log.log(u"Cargando capa complementaria y aplicando formato: " + capa)
        
        formato.formato_layout(tit.upper() + " A NIVEL " + tipo.upper())
        
        ccapas.carga_capas(ruta, capa)
        ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + capa + ".lyr"
        try:
            arcpy.ApplySymbologyFromLayer_management(capa, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología
            log.log(u"Aplicando simbología a " + capa)
        except:
            log.log(u"Falló aplicación de simbología en " + capa)

        arch = ruta + "/" + capa + ".shp"
        capasal = "Clip " + capa
        capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capasal + ".shp"
        log.log(u"rótulos en capa: " + capa + u", campo: " + ncampo[i])
        
        try:
            act_rot.activar_rotulos(capa, ncampo[i])
        except:
            log.log(u">>> ERROR: No se ha podido aplicar rótulos en capa: " + capa + u", campo: " + ncampo[i])

        
    
        if tipo == "nacional":
            gus = None
        else:
            arcpy.Clip_analysis(in_features=arch,
                clip_features=cbase,
                out_feature_class=capasalida,
                cluster_tolerance="")
            ccapas.remover_capas(capasalida)
            numero_de_elementos = int(arcpy.GetCount_management(capasal).getOutput(0))
            log.log("elementos en clip " + tit.upper() + ":" + str(numero_de_elementos))

        

        if numero_de_elementos == 0 and capasalida is None:
            print("CAPA VACÍA")
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
                    
                except:
                    print("Falló aplicación de simbología en " + capa)
    #             print("durmiendo")
    #             time.sleep(5)
    #             log.log(u"Datos para rótulos, capa: " + capa + u", campo: " + ncampo[i])
    #             act_rot.activar_rotulos("CURRENT", capa, ncampo[i])
    #             ccapas.remover_capas(capasal)
    #         
    #     mensaje = ("hora" + "CAMPO: " + capasalida + ", "  + ncampo[i])
    #     time.sleep(10)
    #     print("durmiendo...")
    #     act_rot.activar_rotulos("CURRENT", capasalida, ncampo[i])
            

    #     print("Ruta destino " + r_dest)
        i=i + 1

    if ordinal > 0:
        archivo = arcpy.env.carp_cliente + capa + " near.txt"
        log.log(u"Ordinal mayor que cero, se visualizarán " + str(ordinal) + " elementos para " + archivo)
        columna = 3
        reload(extraedato)
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
    log.log(u"Proceso clip temático finalizado para mapa " + str(nummapa) + " " + tit)

