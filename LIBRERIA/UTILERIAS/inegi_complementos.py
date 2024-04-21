# -*- coding: utf-8 -*-
"""
librería de funciones para mapas complementarios a los del medio físico natural del INEGI
"""

from ESUSTENTA_UTILERIAS import log
from Utilerias_shp import identidadclip
from Utilerias_shp import nearbuff
import Crea_mapa_tematico
reload(Crea_mapa_tematico)
from Crea_mapa_tematico import proc_integra
import diccionarios_cargacapas as dicci
reload(dicci)

import Utilerias_shp as USHP

def denue(dbasicos,creajson=True):
    """
    Genera mapa para el denue
    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)
    
    archivo="{}INEGI/DENUE/2023/{}/conjunto_de_datos/denue_wgs84z13.shp".format(dbasicos['rutadatosgis'],dbasicos['estado'])
    
    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        # 'NOMZONECOL'    :   u'NOMBRE DE LA ZONA',
        # 'TIPO_ZONA'     :   u'TIPO',
        # 'NUM_ZONA'      :   u'NÚMERO DE ZONA',
        # 'AREA'          :   u'AREA (has)',
        # 'PERIMETRO'     :   u'PERIMETRO (km)',
            }
    
    # VALORES GENERALES
    valoresbasicos={
        'archivobase'   :   dbasicos['sistema'],
        'archlog'       :   dbasicos['archivo_log'],
        'camposidenti'  :   camposidenti,
        'carpeta_proy'  :   dbasicos['carpeta_proy'],
        'proyecto'      :   dbasicos['proyecto'],
        'archlog'       :   dbasicos['archivo_log'],
        'mxd'           :   dbasicos['mxd'],
        'df'            :   dbasicos['df'],

        'elementos'     :   50, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   archivo,
        'layer'         :   dbasicos['rutasimbologia'] + 'denue_wgs84z13-1.lyr',
        'campo'         :   'nom_estab', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Establecimientos denue',   # Para el dataframe
        'titulocapa'    :   "DENUE",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '2 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida, escala automática = None
        'transparencia' :   50, # transparencia para capa base
    }

    valoresnear={
        'elementos'     :   valoresbasicos['elementos'],
        'archivobase'   :   valoresbasicos['archivobase'],
        'archivonear'   :   valoresbasicos['archivonear'],
        'campo'         :   valoresbasicos['campo'],
        'carpeta_proy'  :   valoresbasicos['carpeta_proy'],
        'radiobuffer'   :   valoresbasicos['radiobuffer'],
        'archlog'       :   valoresbasicos['archlog'],
    }

    valoresidenti={
        'capapunto'     :   valoresbasicos['archivobase'],
        'capaident'     :   valoresbasicos['archivonear'],
        'camposidenti'  :   valoresbasicos['camposidenti'],
        'carpeta_proy'  :   valoresbasicos['carpeta_proy'],
        'proyecto'      :   valoresbasicos['proyecto'],
        'archlog'       :   valoresbasicos['archlog'],
    }

    valprocesofin={
        'mxd'           :   valoresbasicos['mxd'],
        'df'            :   valoresbasicos['df'],
        'titulomapa'    :   valoresbasicos['proyecto'],
        'subtitulomapa' :   valoresbasicos['subtitulomapa'],
        'capazoom'      :   valoresbasicos['archivonear'],
        'sistema'       :   valoresbasicos['archivobase'],
        'escala'        :   valoresbasicos['escala'],
        'carpeta_proy'  :   valoresbasicos['carpeta_proy'],
        'archsalida'    :   valoresbasicos['subtitulomapa'].replace(" ", "_"),
        'archlog'       :   valoresbasicos['archlog'],
        }
    
    capabase={
        'mxd'           :   valoresbasicos['mxd'],
        'df'            :   valoresbasicos['df'],
        'shapefile'     :   valoresbasicos['archivonear'],
        'nombreshape'   :   valoresbasicos['titulocapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

    # =========Capas complementarias a cargar en el layout=========
    # carga diccionaro para capa de estados decreto 185
    manzanas=dicci.manzanas(dbasicos)
    manzanas['shapefile']=dbasicos['rutascince2020'] + "manzana_localidad.shp"
    manzanas['campo_rotulos']=None
    caminos=dicci.rnc(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        # valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        manzanas,
        caminos,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        valores={
            "capabase"  :   dbasicos['archsistema'],
            "capanear"  :   valoresbasicos['archivobase'],
            "radio"     :   1000,
            "carp_tmp"  :   dbasicos['carpeta_proy'] + "/temp/",
            "archlog"   :   dbasicos['archivo_log']
        }
        lista_cercanos=USHP.listacercanos(valores)
        print (lista_cercanos)
        
        return resultado
    except Exception as e:
        return e



    print(valores)
    print(distancia)

    USHP.clipparamapa()



