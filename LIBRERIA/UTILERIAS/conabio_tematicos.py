# -*- coding: utf-8 -*-

"""
Librería para generar mapas temáticos de la conabio
Usa la librería de mapas temáticos del inegi para relizar
los procesos
"""

from ESUSTENTA_UTILERIAS import log
from Utilerias_shp import identidadclip
from Utilerias_shp import nearbuff
import Crea_mapa_tematico
reload(Crea_mapa_tematico)
from Crea_mapa_tematico import proc_integra
import diccionarios_cargacapas as dicci
reload(dicci)



def area_nat_protegida(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        "NOMBRE"        :   u"NOMBRE",
        "TIPO"          :   u"TIPO",
        "CATEGORIA"     :   u"CATEGORIA",
        "F_DEC"         :   u"FECHA DE DECRETO",
        "FUENTE"        :   u"FUENTE",
        "HECTARES"      :   u"SUPERFICIE (has)",
        "ESTADO"        :   u"UBICACION EN ENTIDAD FEDERATIVA",
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
        'archivonear'   :   dbasicos['rutaconabio'] + "Areas naturales protegidas.shp",
        'layer'         :   dbasicos['rutasimbologia'] + "Areas naturales protegidas.lyr",
        'campo'         :   "NOMBRE", # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   "Areas naturales protegidas",   # Para el dataframe
        'titulocapa'    :   "A.N.P",    # Nombre de la capa, para la simbología.
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
        'nombreshape'   :   valoresbasicos['titulocapa'],
        'layer'         :   valoresbasicos['layer'],
        'transparencia' :   valoresbasicos['transparencia'],
        'campo_rotulos' :   valoresbasicos['campo'],
    }

    # =========Capas complementarias a cargar en el layout=========
    # carga diccionaro para capa de estados decreto 185
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
            valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def clima_koppen(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'CLIMA_TIPO'    :   u'CLAVE KOPPEN',
        'AREA'          :   u'AREA DEL POLIGONO DE CLIMA',
        'DES_TEM'       :   u'DESCRIPCION DE TEMPERATURAS',
        'DES_PREC'      :   u'DESCRIPCION DE LAS PRECIPITACIONES',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Climas.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Climas.lyr',
        'campo'         :   'CLIMA_TIPO', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Climas Koppen',   # Para el dataframe
        'titulocapa'    :   "Climas Koppen",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida
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

    # =========Capas complementarias a cargar en el layout=========
    # carga diccionaro para capa de estados decreto 185
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def clima_olgyay(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'CLIMA'         :   u'CLIMA',
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

        'elementos'     :   2, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutadatosgis'] + '/00 PROPIOS/CLIMA/MEXICO_OLGYAY.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'MEXICO_OLGYAY.lyr',
        'campo'         :   'CLIMA', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Climas Olgyay',   # Para el dataframe
        'titulocapa'    :   "Climas Olgyay",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   15000000,   # Definir valor si se desea que se haga una zoom a una escala definida
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def cuenca(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'CUENCA'         :   u'CUENCA HIDROLOGICA',
        'REGION'         :   u'REGION HIDROLOGICA',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Cuenca hidrologica.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Cuenca hidrologica cuenca.lyr',
        'campo'         :   'CUENCA', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Cuencas hidrologicas',   # Para el dataframe
        'titulocapa'    :   "Cuencas Hidro.",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def edafologia(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'SUE1'          :   u'CLAVE EDAFOLOGICA',
        'TEX'           :   u'TEXTURA',
        'FASFIS'        :   u'FASE FISICA',
        'FASQUIM'       :   u'FASE QUIMICA',
        'OBSERVACIO'    :   u'OBSERVACIONES',
        'DESCRIPCIO'    :   u'DESCRIPCION',
        'DESC_TEX'      :   u'DESCRIPCION DE TEXTURA',
        'DESC_FASFI'    :   u'DESCRIPCION DE FASE FISICA',
        'DESC_FAQUI'    :   u'DESCRIPCION DE FASE QUIMICA',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Edafologia.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Edafologia.lyr',
        'campo'         :   'DESCRIPCIO', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Edafologia',   # Para el dataframe
        'titulocapa'    :   "Edafologia",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def humedad(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'TIPO'          :   u'TIPO',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Humedad del suelo.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Humedad del suelo.lyr',
        'campo'         :   'TIPO', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Humedad del suelo',   # Para el dataframe
        'titulocapa'    :   "Zona de humedad",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def precip(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'PRECI_RANG'          :   u'RANGO DE PRECIPITACION',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Precipitacion.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Precipitacion.lyr',
        'campo'         :   'PRECI_RANG', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Precipitacion',   # Para el dataframe
        'titulocapa'    :   "Z. precipitacion",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
        'escala'        :   None,   # Definir valor si se desea que se haga una zoom a una escala definida, escala automática = None
        'transparencia' :   30, # transparencia para capa base
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def subcuenca(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'NOMBRE'        :   u'NOMBRE DE LA SUBCUENCA',
        'DESCRIPCI'     :   u'DESCRIPCION',
        'TIPO'          :   u'TIPO',
        'AREA'          :   u'AREA (has)',
        'PERIMETRO'     :   u'PERIMETRO (km)',
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

        'elementos'     :   7, #cantidad de elementos más cercanos a regresar
        'archivonear'   :   dbasicos['rutaconabio'] + 'Subcuencas hidrologicas.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Subcuencas hidrologicas.lyr',
        'campo'         :   'NOMBRE', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Subcuencas hidrológicas',   # Para el dataframe
        'titulocapa'    :   "Subcuenca",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '70 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def subregion(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'NOMBRE'        :   u'NOMBRE DE LA REGION',
        'CLAVE_SH'      :   u'CLAVE',
        'PERIMETRO'     :   u'PERIMETRO (km)',
        'AREA'          :   u'AREA (has)',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Subregiones hidrologicas.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Subregiones hidrologicas.lyr',
        'campo'         :   'NOMBRE', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Subregiones hidrológicas',   # Para el dataframe
        'titulocapa'    :   "Subregiones",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e

def zonaecol(dbasicos,creajson=True):
    """
    Función para crear mapa y registro de identidad de in punto
    con respecto al shp de áreas naturales protegidas

    returns: mensaje con los resultados del proceso.
    """
    

    archlog=dbasicos['archivo_log']
    log("reporte de 'area_nat_protegida'...",archlog)

    # CAMPOS A OBTENER EN EL ANÁLISIS DE IDENTIDAD
    camposidenti={
        'NOMZONECOL'    :   u'NOMBRE DE LA ZONA',
        'TIPO_ZONA'     :   u'TIPO',
        'NUM_ZONA'      :   u'NÚMERO DE ZONA',
        'AREA'          :   u'AREA (has)',
        'PERIMETRO'     :   u'PERIMETRO (km)',
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
        'archivonear'   :   dbasicos['rutaconabio'] + 'Zonas ecologicas.shp',
        'layer'         :   dbasicos['rutasimbologia'] + 'Zonas ecologicas.lyr',
        'campo'         :   'NOMZONECOL', # CAMPO PARA 'archivonear' y para rótulos de capa base
        'subtitulomapa' :   'Zonas ecologicas',   # Para el dataframe
        'titulocapa'    :   "Z. ecoloogica",    # Nombre de la capa, para la simbología.
        'radiobuffer'   :   '100 kilometers', #RADIO DEL BUFFER PARA CLIP PARA NEAR
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
    valestados=dicci.estataldecreto(dbasicos)
    
    # Definición de diccionarios
    diccionariosnear=[  # Define los diccionarios a los que se aplicará análisis near
        valoresnear,
        ]
    
    diccionariosidenti=[    # Define los diccionarios a los que se aplicará análisis identidad
        valoresidenti,
    ]
    
    capas_a_cargar=[    # Define las capas que se van a cargar en layout para visualizar en el mapa
        valestados,
        capabase,
    ]

    try:
        resultado = proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson)
        return resultado
    except Exception as e:
        return e


