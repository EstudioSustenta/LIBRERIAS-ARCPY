# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS TEMÁTICOS.

import arcpy
import importlib
import sys

def cliptema(rutas, capas, tipo, ncampo, nummapa, tit):
    print ("iniciando rutina de clip " + tipo + tit)

    # Agrega la ruta del paquete al path de Python
    ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON"
    sys.path.append(ruta_libreria)

    mxd = arcpy.env.mxd
    df = arcpy.env.df

    arcpy.env.overwriteOutput = True

    arcpy.env.overwriteOutput = True
    layout_name = "Layout"
    ccapas = importlib.import_module("LIBRERIA.CARGAR CAPAS 1_0_0")
    filtro = importlib.import_module("LIBRERIA.FILTRO 1_0_0")
    z_extent = importlib.import_module("LIBRERIA.ZOOM EXTENT 1_0_0")
    formato = importlib.import_module("LIBRERIA.FORMATO 1_0_0")
    exportma = importlib.import_module("LIBRERIA.EXPORTAR MAPAS 1_0_0")
    act_rot = importlib.import_module("LIBRERIA.ACTIVA ROTULOS 1_0_0")
    extraedato = importlib.import_module("LIBRERIA.EXTRAE DATO")

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

    ccapas.carga_capas(rbase, cbase)
    filtro.fil_expr(cbase, filtr)
    # act_rot.activar_rotulos("CURRENT", cbase, campoRotulo)

    i = 0
    for ruta in rutas:
        capa = capas[i]

        ccapas.carga_capas(ruta, capa)
        ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + capa + ".lyr"
        arcpy.ApplySymbologyFromLayer_management(capa, ruta_lyr) # esta línea ocasionalmente genera errores en la selección del archivo de simbología

        arch = ruta + u"/" + capa + ".shp"
        capasal = "Clip " + capa
        capasalida = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capasal + ".shp"
        ruta_lyr = "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/" + cbase + ".lyr"
        
        arcpy.ApplySymbologyFromLayer_management(cbase, ruta_lyr)
        act_rot.activar_rotulos("CURRENT", capa, ncampo)
        z_extent.zoom_extent(layout_name, cbase)
        if tipo == "nacional":
            gus = None
        else:
            arcpy.Clip_analysis(in_features=arch,
                clip_features=cbase,
                out_feature_class=capasalida,
                cluster_tolerance="")
            numero_de_elementos = int(arcpy.GetCount_management(capasal).getOutput(0))
            print("Número de elementos " + str(numero_de_elementos))

        formato.formato_layout(tit.upper() + " A NIVEL " + tipo.upper())

        if numero_de_elementos == 0 and capasalida is not None:
            print("CAPA VACÍA")
            ccapas.remover_capas(capasal)
        else:
            if tipo == "nacional":
                gus = None
            else:
                capa_diss = "Y:/0_SIG_PROCESO/X TEMPORAL/" + capa + ".shp"
                arcpy.Dissolve_management(in_features=capasal,
                    out_feature_class=capa_diss,
                    dissolve_field=ncampo,
                    statistics_fields="", 
                    multi_part="MULTI_PART", 
                    unsplit_lines="DISSOLVE_LINES")
                ccapas.remover_capas(capasal)
                ccapas.remover_capas(capa)

            nombre_leyenda = "Legend"  # Define el nombre de la leyenda
            leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", nombre_leyenda)[0]
            # Verificar si la leyenda fue encontrada
            if leyenda:
                # Obtener la lista de elementos de la leyenda
                elementos_leyenda = leyenda.listLegendItemLayers()
                # Buscar el elemento de leyenda por nombre y eliminarlo
                for elemento in elementos_leyenda:
                    if elemento.name == capa:
                        leyenda.removeItem(elemento)
            act_rot.activar_rotulos("CURRENT", capa, ncampo)
            i=i + 1
        r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + "_" + str(nummapa) + "_" + tit

        print("Ruta destino " + r_dest)
        
        reload(exportma)
        extraedato.extraedato(archivo, ordinal, columna)
        exportma.exportar(r_dest)

    i = 0
    for capa in capas:
       
       ccapas.remover_capas(capa)
       print("Removiendo capa " + capa)
       i = i + 1
   
    ccapas.remover_capas(cbase)


    print("Proceso clip temático finalizado  para mapa " + str(nummapa) + "\n\n\n\n")
