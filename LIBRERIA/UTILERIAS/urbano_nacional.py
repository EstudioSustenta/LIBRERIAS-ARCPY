# -*- coding: utf-8 -*-

# SCRIPT PARA GENERAR PRODUCTOS CARTOGRÁFICOS DE ZONAS URBANAS.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import UTILERIAS.Utilerias_shp as USH
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
import estados as sustit
# reload(ESU)
# reload(USH)
# reload(sustit)




def proyurbano(dbasicos):

    """
    Ejecuta el proceso para generar mapas en el ámbito urbano
    parámetro: dbasicos (diccionario con los valores necesarios para su funcionamiento)
    returns: reporte de actividades
    """
    
    mxd = dbasicos['mxd']                   # Obtener acceso al documento actual
    df = dbasicos['df']
    arch = dbasicos['archivo_log']
    ESU.log("Librería 'urbano_nacional' cargada con éxito...",arch,imprimir=False)
    ESU.log("Iniciando proceso para proyecto urbano...",arch, presalto=2)
    try:
        estado = dbasicos['estado']
        municipio = dbasicos['municipio']
        carp_cliente = dbasicos['carpeta_proy']
        localidad = dbasicos['localidad']
        carpeta_proy=dbasicos['carpeta_proy']
        rednalcaminos=dbasicos['rednalcaminos']
        rutascince2020=dbasicos['rutascince2020']
        proyecto=dbasicos['proyecto']

        ESU.log("'urbano_nacional' iniciando...",arch)

        # Proceso para extraer los nombres de las entidades federativas del campo "ENTIDAD"
        estadossust = sustit.sustedo()
        if estado in estadossust:
            edo=estadossust[estado]
        
        # proceso para cargar y dar formato a capas comunes
        # Carga los municipios del pais
        valoresmun = {
            'mxd': mxd,
            'df': df,
            'shapefile': "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS/MUNICIPAL CENSO 2020 DECRETO 185.shp",
            'nombreshape': "Municipios",
            'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/MUNICIPAL CENSO 2020 DECRETO 185.lyr",
            'transparencia': 50,
            'campo_rotulos': 'NOM_MUN',
        }
        ESU.log(USH.carga_capa_y_formatea(valoresmun), arch)
        filtr = """ "NOM_ENT" = '{}' AND "NOM_MUN" = '{}' """.format(estado, municipio)
        ESU.log(USH.fil_expr(mxd,valoresmun["nombreshape"],filtr), arch)
        ESU.log(USH.zoom_extent(mxd,df,valoresmun['nombreshape'],over=10),arch)

        # Carga las manzanas del estado
        valoreslocu = {
            'mxd': mxd,
            'df': df,
            'shapefile': u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/loc_urb.shp",
            'nombreshape': "Loc. urbanas",
            'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/loc_urb.lyr",
            'transparencia': 30,
            'campo_rotulos': None,
        }
        ESU.log(USH.carga_capa_y_formatea(valoreslocu),arch)

        # Carga los caminos del pais
        valorescarr = {
            'mxd': mxd,
            'df': df,
            'shapefile': rednalcaminos,
            'nombreshape': "R.N.C",
            'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/carretera250_l.lyr",
            'transparencia': 50,
            'campo_rotulos': None,
        }
        ESU.log( USH.carga_capa_y_formatea(valorescarr),arch)
        

        def municipio():
            filtr = """("TIPO_VIAL" = 'Carretera' OR "TIPO_VIAL" = 'Boulevard')"""
            ESU.log(USH.fil_expr(mxd,valorescarr["nombreshape"],filtr), arch)
            ESU.log("Iniciando proceso para mapa municipal...",arch, presalto=1)
            ESU.log(USH.formato_layout(mxd, proyecto,"UBICACIÓN A NIVEL MUNICIPIO"),arch)
            ESU.log(USH.exportar(mxd, carp_cliente,"Municipio",serial=True),arch)
            ESU.log("Proceso para mapa municipal terminado",arch)

        def ciudad():
            # Proceso para generar mapa de la ciudad: 
            ESU.log("Iniciando proceso para mapa de ciudad...",arch)
            localidades=valoreslocu["nombreshape"]
            try:   
                filtr = """ "NOM_ENT" = '{}' AND \"NOMGEO\" = '{}' """.format(estado,localidad)
                ESU.log(USH.fil_expr(mxd,localidades,filtr), arch)
                ESU.log(USH.zoom_extent(mxd,df,localidades), arch)
                filtr = """("TIPO_VIAL" = 'Carretera' OR "TIPO_VIAL" = 'Boulevard' OR "TIPO_VIAL" = 'Avenida')"""
                ESU.log(USH.fil_expr(mxd,valorescarr["nombreshape"],filtr), arch)
                ESU.log(USH.formato_layout(mxd, proyecto,'Mapa de la ciudad de {}'.format(localidad)), arch)
                ESU.log(USH.exportar(mxd, carpeta_proy,'Ciudad',serial=True), arch)
                ESU.log("Proceso para mapa de ciudad realizado con éxito", arch)
            except Exception as e:
                ESU.log('>>>>>ERROR en ciudad: {}'.format(e), arch,imprimir=True)

        def maparegion():

            try:
                # ESU.log(USH, arch)
                ESU.log("Proceso Región iniciando", arch)
                valoresmanz = {
                    'mxd': mxd,
                    'df': df,
                    'shapefile': "{}manzana_localidad.shp".format(rutascince2020),
                    'nombreshape': "Manzanas",
                    'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/manzana_localidad.lyr",
                    'transparencia': 30,
                    'campo_rotulos': None,
                    }
                ESU.log(USH.carga_capa_y_formatea(valoresmanz), arch)
                escala = 50000
                ESU.log(USH.zoom_extent(mxd,df,"SISTEMA"), arch)
                df.scale = escala
                ESU.log(USH.formato_layout(mxd, proyecto,u"UBICACIÓN A NIVEL REGIÓN"), arch)
                ESU.log(USH.exportar(mxd, carp_cliente,'Region',serial=True), arch)
                ESU.log("Proceso Región finalizado", arch)
            except Exception as e:
                ESU.log(">>>>>ERROR en maparegion: {}".format(e), arch,imprimir=True)

        def zona():
            # Proceso para generar mapa de la zona:
            try:
                ESU.log("Proceso zona iniciando", arch)
                
                valorescol = {
                    'mxd': mxd,
                    'df': df,
                    'shapefile': "Y:/GIS/MEXICO/VARIOS/www.numeroslocos.com/{0}/Colonias_{0}.shp".format(edo),
                    'nombreshape': "Colonias",
                    'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/Colonias.lyr",
                    'transparencia': 10,
                    'campo_rotulos': 'COLONIA',
                    }
                escala = 25000
                ESU.log(USH.zoom_extent(mxd,df,"SISTEMA"), arch)
                df.scale = escala
                ESU.log(USH.carga_capa_y_formatea(valorescol), arch)
                ESU.log(USH.formato_layout(mxd, proyecto,u"UBICACIÓN A NIVEL ZONA"), arch)
                ESU.log(USH.exportar(mxd, carpeta_proy,'Zona',serial=True), arch)
                ESU.log("Proceso zona finalizado", arch)

            except Exception as e:
                ESU.log(">>>>>ERROR en zona: {}".format(e), arch,imprimir=True)

        def sitio():
            # Proceso para generar mapa de la sitio:
            try:
                capa_a_apagar=valorescarr['nombreshape']
                (arcpy.mapping.ListLayers(mxd, capa_a_apagar, df)[0]).visible = False
                valorescall = {
                    'mxd': mxd,
                    'df': df,
                    'shapefile': "{}eje_vial.shp".format(rutascince2020),
                    'nombreshape': "Vialidades",
                    'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/carretera250_l.lyr",
                    'transparencia': 50,
                    'campo_rotulos': "NOMVIAL",
                    }
                ESU.log(USH.carga_capa_y_formatea(valorescall), arch)
                escala = 7500
                df.scale = escala
                ESU.log(USH.formato_layout(mxd, proyecto,u"UBICACIÓN A NIVEL SITIO"), arch)
                ESU.log(USH.exportar(mxd, carp_cliente,'Sitio',serial=True), arch)
                escala = 3500
                df.scale = escala
                ESU.log(USH.formato_layout(mxd, proyecto,u"UBICACIÓN A NIVEL LUGAR"), arch)
                ESU.log(USH.exportar(mxd, carp_cliente,'Lugar',serial=True), arch)
                
            except Exception as e:
                ESU.log(">>>>>ERROR en sitio: {}".format(e), arch,imprimir=True)

        # -------------------------------------------------------------------------------
        municipio()
        ciudad()
        maparegion()
        zona()
        sitio()
        
    except Exception as e:
        ESU.log('>>>>>ERROR en purbano:\n {}'.format(e),arch,imprimir=True)
    finally:
        ESU.log(USH.borrainn(mxd,df),arch)
