# -*- coding: utf-8 -*-


# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS RURALES.
# FUNCION: A NIVEL NACIONAL.

import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
import UTILERIAS.Utilerias_shp as USH
reload(USH)

es=USH

def proyrural(dbasicos):
    """
    Proceso para crear mapa municipal cuando el ámbito es rural
    
    """
    arch_log=dbasicos['archivo_log'] 
    ESU.log("Iniciando 'prural'...",arch_log,imprimir=True)
    proyecto=dbasicos['proyecto']
    
    rutasimbologia=dbasicos['rutasimbologia']
    municipio=dbasicos['municipio']
    mxd=dbasicos['mxd']
    df=dbasicos['df']
    sistema=u"SISTEMA"

    # -----municipio-----
    valores = {
            'mxd': dbasicos['mxd'],
            'df': dbasicos['df'],
            'shapefile': "{}municipal.shp".format(dbasicos['rutascince2020']),
            'nombreshape': "Municipio",
            'layer': rutasimbologia + "Municipios.lyr",
            'transparencia': 50,
            'campo_rotulos': "NOMGEO",
        }
    ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
    filtro= u""" ("NOMGEO" =  '{}') """.format(municipio)
    ESU.log(USH.fil_expr(mxd,valores['nombreshape'],filtro),arch_log)
    ESU.log(USH.zoom_extent(mxd,df,valores['nombreshape'],over=5),arch_log)


    # -----caminos-----
    valores['shapefile']=dbasicos['rednalcaminos']
    valores['nombreshape']="Caminos"
    valores['layer']=rutasimbologia + "carretera250_l.lyr"
    valores['campo_rotulos']=None
    ESU.log(USH.carga_capa_y_formatea(valores),arch_log)

    # -----localidades urbanas-----
    valores['shapefile']=dbasicos['rutascince2020'] + "loc_urb.shp"
    valores['nombreshape']="Loc. Urbanas"
    valores['layer']=rutasimbologia + "Localidades.lyr"
    valores['campo_rotulos']="NOMGEO"
    valores['transparencia']=30
    ESU.log(USH.carga_capa_y_formatea(valores),arch_log)

    # -----localidades rurales-----
    valores['shapefile']=dbasicos['rutascince2020'] + "loc_rur.shp"
    valores['nombreshape']="Loc. Rurales"
    valores['layer']=rutasimbologia + "loc_rur.lyr"
    valores['campo_rotulos']="NOMGEO"
    valores['transparencia']=10
    ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
    expr="""("POB1" >=200)"""
    USH.fil_expr(mxd,valores['nombreshape'],expr)

    #-----formato e impresión municipio------

    ESU.log(USH.formato_layout(mxd, proyecto, u"Mapa municipal"),arch_log)
    ESU.log(USH.exportar(mxd,dbasicos['carpeta_proy'],"Municipal",serial=True),arch_log)

    #-----formato e impresión region------
    
    ESU.log(USH.zoom_extent(mxd,df,sistema),arch_log)
    df.scale = 50000
    ESU.log(USH.formato_layout(mxd, proyecto, u"Ubicación a nivel región"),arch_log)
    expr='[TIPO_VIAL] + " " + [NOMBRE] '
    ESU.log(USH.activar_rot_exp(mxd,df,"Caminos",expr),arch_log)
    ESU.log(USH.exportar(mxd,dbasicos['carpeta_proy'],"Region",serial=True),arch_log)

    #-----formato e impresión zona------

    ESU.log(USH.zoom_extent(mxd,df,sistema),arch_log)
    df.scale = 25000
    ESU.log(USH.formato_layout(mxd, proyecto, u"Ubicación a nivel zona"),arch_log)
    ESU.log(USH.exportar(mxd,dbasicos['carpeta_proy'],"zona",serial=True),arch_log)

    

    #-----finalizando-----
    ESU.log(USH.borrainn(mxd,df),arch_log)
