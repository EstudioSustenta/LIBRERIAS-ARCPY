# -*- coding: utf-8 -*-

"""
Librería para generar mapas temáticos de la conabio
Usa la librería de mapas temáticos del inegi para relizar
los procesos.
importante:
En la lista de capas a cargar, capabase debe ser la última de la lista para
que el proceso de recorte se ejecute en esa capa.
El proceso de recorte en Crea_mapa_tematico.py se ejecuta en la última capa de la lista.
"""

from ESUSTENTA_UTILERIAS import log
from Utilerias_shp import identidadclip
from Utilerias_shp import nearbuff
import Crea_mapa_tematico
reload(Crea_mapa_tematico)
from Crea_mapa_tematico import proc_integra
import diccionarios_cargacapas as dicci
reload(dicci)


def usodesuelo(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        "ECOS_VEGE"     :   u"VEGETACION",
        "INFYS_0409"    :   u"INFORMACION COMPLEMENTARIA",
        "VEG_FORES"     :   u"USO DE SUELO",
        "CVE_UNION"     :   u"CLAVE",
        "FORMACION"     :   u"FORMACION",
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "USO DE SUELO INEGI SERIE IVCopy.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Uso de suelo.lyr",
        'campo'         :   "VEG_FORES", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Uso de suelo",   # Para el dataframe
        'radiobuffer'   :   "100 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   50, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    valcaminos=dicci.caminos(dbasicos)
    valcaminos['campo_rotulos']=None    # cambia el valor del campo caminos para que no se muestre en el mapa
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
            valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        valcaminos,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def hidrologia(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'hidrologia'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'NOMBRE'        :   'NOMBRE',
        'GEOGRAFICO'    :   'GEOGRAFICO',
        'CONDICION'     :   'CONDICION',
        'IDENTIFICA'    :   'IDENTIFICADOR INEGI',
        'AREAhas'       :   'SUPERFICIE (has)',
        'PERIM_km'      :   'PERIMETRO (km)',
        'CVE_EDO'       :   'CLAVE DE ESTADO DE UBICACION',
    }
    
    # VALORES GENERALES
    valoresbasicos={
        'archivobase'   :   dbasicos['archsistema'],
        'archlog'       :   dbasicos['archivo_log'],
        'camposidenti'  :   camposidenti,
        'carpeta_proy'  :   dbasicos['carpeta_proy'],
        'proyecto'      :   dbasicos['proyecto'],
        'archlog'       :   dbasicos['archivo_log'],
        'mxd'           :   dbasicos['mxd'],
        'df'            :   dbasicos['df'],

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Cuerpos de agua.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Cuerpos de agua1.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Hidrologia",   # Para el dataframe
        'titulocapa'    :   "Cuerpos de agua",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "100 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   50, # transparencia para capa base
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

    valoresnear1={
        'elementos'     :   valoresbasicos['elementos'],
        'archivobase'   :   valoresbasicos['archivobase'],
        'archivonear'   :   dbasicos['rutamapadigital'] + "Corrientes de agua.shp",
        'campo'         :   "NOMBRE",
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
        'capazoom'      :   valoresbasicos['archivobase'],
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

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionarios para carga de capas.
    valcaminos=dicci.caminos(dbasicos)
    valcaminos['campo_rotulos']=None    # cambia el valor del campo caminos para que no se muestre en el mapa
    estataldecreto=dicci.estataldecreto(dbasicos)
    valcorrientes=dicci.corrientesdeagua(dbasicos)
    valcorrientes['transparencia']=20

    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        valoresnear1,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad
    diccionariosidenti=[
            valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        valcaminos,
        valcorrientes,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def lineasElectricas(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'lineasElectricas'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={} # se pasa un campo vacío porque en este mapa no hay shapefiles tipo polígono
    
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Linea de transmision electrica.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Linea de transmision electrica.lyr",
        'campo'         :   "TIPO", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Infraestructura electrica",   # Para el dataframe
        'titulocapa'    :   "Linea de transmision",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "100 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   50, # transparencia para capa base
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

    valoresnear1={
        'elementos'     :   valoresbasicos['elementos'],
        'archivobase'   :   valoresbasicos['archivobase'],
        'archivonear'   :   dbasicos['rutamapadigital'] + "Subestacion electrica.shp",
        'campo'         :   "NOMBRE",
        'carpeta_proy'  :   valoresbasicos['carpeta_proy'],
        'radiobuffer'   :   valoresbasicos['radiobuffer'],
        'archlog'       :   valoresbasicos['archlog'],
    }

    # no se usa porque no hay capas de polígonos para el proceso identity
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
        'capazoom'      :   valoresbasicos['archivobase'],
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

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionarios para carga de capas.
    valcaminos=dicci.caminos(dbasicos)
    valcaminos['campo_rotulos']=None    # cambia el valor del campo caminos para que no se muestre en el mapa
    estataldecreto=dicci.estataldecreto(dbasicos)
    valcorrientes=dicci.corrientesdeagua(dbasicos)
    valcorrientes['transparencia']=20
    subestaciones=dicci.subestacioneselec(dbasicos)

    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        valoresnear1,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad
    diccionariosidenti=[
            # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        valcaminos,
        subestaciones,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def malpais(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        "GEOGRAFICO"    :   u"GEOGRAFICO",
        "IDENTIFICA"    :   u"IDENTIFICADOR",
        "AREA_has"      :   u"SUPERFICIE (has)",
        "CVE_EDO"       :   u"CLAVE DEL ESTADO DE UBICACION",
        "CALI_REPR"     :   u"CALIDAD DE REPRESENTACION",
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Malpais.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Malpais.lyr",
        'campo'         :   "GEOGRAFICO", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Malpais",   # Para el dataframe
        'titulocapa'    :   "Malpais",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "3000 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   20, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
            valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def curvasdenivel(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={}
    
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Curvas de nivel.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Curvas de nivel.lyr",
        'campo'         :   "ALTURA", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Curvas de nivel",   # Para el dataframe
        'titulocapa'    :   "Curva",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "50 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   250000,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   20, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def pantano(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'GEOGRAFICO'    :   'ELEMENTO',
        'IDENTIFICA'    :   'IDENTIFICADOR',
        'AREA_has'      :   'SUPERFICIE (has)',
        'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Pantano.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Pantano.lyr",
        'campo'         :   "GEOGRAFICO", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Pantanos",   # Para el dataframe
        'titulocapa'    :   "Pantano",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "1000 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   20, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def pistadeAviacion(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        # 'GEOGRAFICO'    :   'ELEMENTO',
        # 'IDENTIFICA'    :   'IDENTIFICADOR',
        # 'AREA_has'      :   'SUPERFICIE (has)',
        # 'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   5, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Pista de aviacion.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Pista de aviacion.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Pistas de aviación",   # Para el dataframe
        'titulocapa'    :   "Pista",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "200 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def presa(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        # 'GEOGRAFICO'    :   'ELEMENTO',
        # 'IDENTIFICA'    :   'IDENTIFICADOR',
        # 'AREA_has'      :   'SUPERFICIE (has)',
        # 'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Presa.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Presa.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Presas",   # Para el dataframe
        'titulocapa'    :   "Presa",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "200 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def rasgoarqueologico(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        # 'GEOGRAFICO'    :   'ELEMENTO',
        # 'IDENTIFICA'    :   'IDENTIFICADOR',
        # 'AREA_has'      :   'SUPERFICIE (has)',
        # 'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Rasgo arqueologico.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Rasgo arqueologico.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Rasgo arqueológico",   # Para el dataframe
        'titulocapa'    :   "Rasgo",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "1000 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def salina(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'NOMBRE'        :   'ELEMENTO',
        'TIPO'          :   'ELEMENTO',
        'IDENTIFICA'    :   'IDENTIFICADOR',
        'AREA_ha'       :   'SUPERFICIE (has)',
        'CVE_EDO'       :   'CLAVE DE ESTADO',
        'PERIM_km'      :   'ELEMENTO',
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

        'elementos'     :   5, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Salina.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Salina.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Salinas",   # Para el dataframe
        'titulocapa'    :   "Salina",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "2000 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def viaferrea(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        # 'GEOGRAFICO'    :   'ELEMENTO',
        # 'IDENTIFICA'    :   'IDENTIFICADOR',
        # 'AREA_has'      :   'SUPERFICIE (has)',
        # 'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Via ferrea.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Via ferrea.lyr",
        'campo'         :   "TIPO", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Vías férreas",   # Para el dataframe
        'titulocapa'    :   "Via ferrea",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "1000 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        # valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def zonaarenosa(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'TIPO'          :   'TIPO',
        'GEOGRAFICO'    :   'ELEMENTO',
        'IDENTIFICA'    :   'IDENTIFICADOR',
        'AREA_has'      :   'SUPERFICIE (has)',
        'PERIM_km'      :   'PERIMETRO (km)',
        'CVE_EDO'       :   'CLAVE DE ESTADO',
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

        'elementos'     :   10, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutamapadigital'] + "Zona arenosa.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Zona arenosa.lyr",
        'campo'         :   "TIPO", # CAMPO PARA 'archivonear'
        'subtitulomapa' :   "Zona arenosa",   # Para el dataframe
        'titulocapa'    :   "Zona arenosa",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   "1500 kilometers", #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
        "transparencia" :   30, # transparencia para capa base
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
        'capazoom'      :   valoresbasicos['archivobase'],
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
        'nombreshape'   :   valoresbasicos['subtitulomapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

#==========DEFINICIÓN DE CAPAS COMPLEMENTARIAS===============
    #Diccionario de caminos
    estataldecreto=dicci.estataldecreto(dbasicos)
    
    # Define los diccionarios a los que se aplicará análisis near
    diccionariosnear=[
        valoresnear,
        ]
    
    # Define los diccionarios a los que se aplicará análisis identidad    
    diccionariosidenti=[
        valoresidenti,
    ]
    
    # Define las capas que se van a cargar en layout para visualizar en el mapa
    capas_a_cargar=[
        estataldecreto,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e





