# -*- coding: utf-8 -*-

"""
Esta librería genera mapas con insumos de inegi
funciones:
marg_mun----> genera mapa de la marginación municipal del estado de ubicación
marg_loc----> genera mapa de la marginación de las localidades urbanas del estado de ubicación
marg_man----> genera mapa de la marginación por manzana del estado de ubicación
"""
# import json
# import arcpy
# import os
from UTILERIAS.ESUSTENTA_UTILERIAS import escribearch1 as ESCR
from arcpy.mapping import ListDataFrames
from arcpy.mapping import MapDocument
from UTILERIAS import Utilerias_shp as ushp


reload(ushp)

# mapa= "Y:/0_SIG_PROCESO/PLANTILLA.mxd"
mapa= "CURRENT"     # Usar esta variable cuando se ejecute el archivo con ArcMap abierto y el mapa de trabajo cargado.

mxd = MapDocument(mapa)
df = ListDataFrames(mxd)[0]
rutamapas = "Y:/0_SIG_PROCESO/MAPAS/"
estado="Aguascalientes"

valores = [{
    # estatal
    'mxd' : mxd,
    'df' : df,
    'shapefile' : 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/nombredelestado/cartografia/estatal.shp',
    'layer' : "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/ESTATAL.lyr",
    'nombreshape' : 'Estatal',
    'transparencia' : None,
    'campo_rotulos' : None,
    'titulo_mapa' : 'Mapa municipal',
},
{
    # municipal
    'mxd' : mxd,
    'df' : df,
    'shapefile' : 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/nombredelestado/cartografia/municipal.shp',
    'layer' : "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/municipal.lyr",
    'nombreshape' : 'Municipal',
    'transparencia' : 50,
    'campo_rotulos' : "NOMGEO"
}]

marg_mun = [
    {
        'mxd' : mxd,
        'df' : df,
        'shapefile' : 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/nombredelestado/cartografia/municipal.shp',
        'layer' : "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/marg_municipal.lyr",
        'nombreshape' : 'Municipal',
        'transparencia' : 50,
        'campo_rotulos' : "NOMGEO",
        'titulo_mapa' : 'Marginación a nivel municipio',
        'jpg' : True,
        'visualizacion' : None,
    }]

marg_manz = [
    {
        'mxd' : mxd,
        'df' : df,
        'shapefile' : 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/nombredelestado/cartografia/manzana_localidad.shp',
        'layer' : "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/marg_manzana.lyr",
        'nombreshape' : 'Manzanas',
        'transparencia' : 30,
        'campo_rotulos' : "marg_decil",
        'titulo_mapa' : 'Marginación a nivel manzana',
        'jpg' : True,
        'visualizacion' : 1000,
    }]

def proceso(valores):
    capa = valores[0]['nombreshape']
    titulomapa = valores[0]['titulo_mapa']
    jpgval=valores[0]['jpg']
    vis=valores[0]['visualizacion']

    # print (ushp.leyenda(mxd, nueva_altura=1.4))
    for valor in valores: # carga y da formato a las capas a visualizar en el mapa.
        cambio = valor['shapefile'].replace('nombredelestado', estado)
        valor['shapefile'] = cambio
        print (ushp.carga_capa_y_formatea(valor))
    if vis != None:     # Si el diámetro de visualización tiene algún valor (metros), ajusta la escala del dataframe
        print (ushp.zoom_extent(mxd, df, "SISTEMA"))
        ushp.escala_en_diametro(mxd, df, "SISTEMA", vis)
    else:
        print (ushp.zoom_extent(mxd, df, capa, over=3))
    print (ushp.leyenda(mxd))
    print (ushp.formato_layout(mxd, proyecto, titulomapa.upper()))
    print (ushp.refresca())
    tit_sin_acentos= ushp.acentos(titulomapa)
    print (ushp.exportar(mxd, rutamapas, tit_sin_acentos, jpg=jpgval))
    for valor in valores:
        capaaremover = valor['nombreshape']
        print (ushp.remueve_capa(mxd, df, capaaremover))
    print (ushp.leyenda(mxd, nueva_altura=1.4))
    print (ushp.formato_layout(mxd, proyecto, "título de mapa".upper()))
    print (ushp.refresca())
    


if __name__ == "__main__":
    
    proceso(marg_mun)   # Genera el mapa de marginación municipal
    proceso(marg_manz)   # Genera el mapa de marginación de manzanas
    # pass