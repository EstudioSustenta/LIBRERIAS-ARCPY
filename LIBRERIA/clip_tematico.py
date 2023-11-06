# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS TEMÁTICOS.

import arcpy
import importlib
import sys
import time
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

mxd = arcpy.env.mxd
df = arcpy.env.df

arcpy.env.overwriteOutput = True
layout_name = u"Layout"

ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")
filtro = importlib.import_module(u"LIBRERIA.filtro")
z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")
formato = importlib.import_module(u"LIBRERIA.formato")
exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")
act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")
extraedato = importlib.import_module(u"LIBRERIA.extrae_dato")
log = importlib.import_module(u"LIBRERIA.archivo_log")
leyenda = importlib.import_module(u"LIBRERIA.leyenda_ajuste")
transp = importlib.import_module(u"LIBRERIA.aplica_transparencia")
acentos = importlib.import_module(u"LIBRERIA.quitar_acentos")
simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")
renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")


# reload(ccapas)
# reload(filtro)
# reload(z_extent)
# reload(formato)
# reload(exportma)
# reload(act_rot)
# reload(extraedato)
# reload(log)
# reload(leyenda)
# reload(tiempo)

repet = arcpy.env.repet


log.log(repet,u"Librería 'clip_tematico' cargada con éxito")

def clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_clip_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(repet,u"'clip_tematico' iniciando para {}...".format(tit))

    rbase = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    numero_de_elementos = None

    if tipo == "nacional":          # decisión: asigna valores para la capa base del marco geográfico y el campo para los rótulos
        cbase = u"ESTATAL decr185"
        campoRotulo = u"NOM_ENT"
        filtr= ""
    elif tipo == "estatal":
        cbase = u"MUNICIPAL CENSO 2020 DECRETO 185"
        filtr= "\"NOM_ENT\" = '{}'".format(arcpy.env.estado)
        campoRotulo = u"NOM_MUN"
    else:
        cbase = u"MUNICIPAL CENSO 2020 DECRETO 185"
        filtr = "\"NOM_ENT\" = '{}' AND \"NOM_MUN\" = '{}'".format(arcpy.env.estado, arcpy.env.municipio)

        campoRotulo = u"NOM_MUN"

    # proceso de capa base
    log.log(repet,u"Cargando capa base y aplicando formato: " + cbase)
    ccapas.carga_capas(rbase, cbase)
    filtro.fil_expr(cbase, filtr)
    act_rot.activar_rotulos(cbase, campoRotulo)
    simbologia.aplica_simb(cbase)
    z_extent.zoom_extent(layout_name, cbase)
    subtitulo1 = (tit + " A NIVEL " + tipo).upper()
    formato.formato_layout(subtitulo1)

    # proceso de bucle para capas de interés
    i = 0
    for ruta in rutas:
        capa = capas[i]

        log.log(repet,u"Bucle para proceso de capa " + capa)
        
        arch = ruta + "/" + capa + ".shp"
        capasal = u"Clip " + capa
        capasalida = u"Y:/0_SIG_PROCESO/X TEMPORAL/{}.shp".format(capasal)
        
        if tipo == "nacional":
            log.log(repet,u"Proceso 'nacional', no se realiza clip del archivo para la capa " + capa)
            # aquí debo poner la carga de archivo capa y darle formato.
            ccapas.carga_capas(ruta,capa)
            simbologia.aplica_simb2(capa,capa)

            
        else:           # si la visualización no es nacional, hace un recorte (clip) del área de interés (estatal o municipal)
            log.log(repet,u"Proceso {}, no se realiza clip del archivo para la capa {}".format(tipo, capa))
            arcpy.Clip_analysis(in_features=arch,
                clip_features=cbase,
                out_feature_class=capasalida,
                cluster_tolerance="")

            numero_de_elementos = int(arcpy.GetCount_management(capasalida).getOutput(0))
            log.log(repet,u"elementos en clip " + capasalida.upper() + ":" + str(numero_de_elementos))

            if numero_de_elementos == 0 and capasalida is None:     # Se evalúa si la capa producto del clip tiene algún contenido y si el archivo existe en la carpeta de temporales
                log.log(repet,u"La capa " + capasal + " no contiene elementos")
            else:
                log.log(repet,u"Capa de trabajo no nacional:\t" + capasalida)
                desc = arcpy.Describe(capasalida)
                tipo_geometria = desc.shapeType

                if not tipo_geometria == "Point": # evalúa si la capa es de puntos, si no lo es, aplica un 'dissolve' a la capa, esto puede reducir la simbología en el mapa
                    capa_diss = u"Y:/0_SIG_PROCESO/X TEMPORAL/" + capa + ".shp"
                    arcpy.Dissolve_management(in_features=capasalida,
                        out_feature_class=capa_diss,
                        dissolve_field=ncampo[i],
                        statistics_fields="", 
                        multi_part="MULTI_PART", 
                        unsplit_lines="DISSOLVE_LINES")
                    ccapas.cargar(capa_diss)
                else:
                    ccapas.cargar(capasalida)
                    renombra.renomb(capasal, capa)

                simbologia.aplica_simb2(capa,capa)
                log.log(repet,u"SE APLICÓ ESTA SIMBOLOGIA")
                    
    #    evalúa si el tipo de geometría de la capa es tipo polígono, si es así, aplica una transparencia
        desc = arcpy.Describe(capa)
        tipo_geometria = desc.shapeType
        log.log(repet,u"geometría tipo " + tipo_geometria)

        if tipo_geometria == "Polygon":
                transp.transp(capa, 50)

        act_rot.activar_rotulos(capa, ncampo[i])

        i=i + 1
    # fin de bucle para capas

    # Proceso para hacer zoom apara que quepan un número (ordinal) de elementos en la vista del mapa
    if ordinal > 0 and tipo != "nacional":      #evalúa si ordinal es mayor que cero y la cobertura no es nacional.
        archivo = "{}{} near {}.txt".format(arcpy.env.carp_cliente, capa, arcpy.env.fechahora)
        log.log(repet,u"Ordinal mayor que cero, se visualizarán " + str(ordinal) + " elementos para " + archivo)
        columna = 3
        extraedato.extraedato(archivo, ordinal, columna)
    
    # Proceso para exportación de archivo
    r_dest = arcpy.env.carp_cliente
    nombarch = arcpy.env.proyecto + " " + str(nummapa) + " " + tit
    # reload (exportma)
    exportma.exportar(r_dest,nombarch)

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

    tiempo_clip_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'clipt': {}".format(tiempo.tiempo([tiempo_clip_ini,tiempo_clip_fin])))

    log.log(repet,u"'clip temático' finalizado!")

    arcpy.env.repet = arcpy.env.repet - 1

arcpy.env.repet = arcpy.env.repet - 1
