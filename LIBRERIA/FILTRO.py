# -*- coding: utf-8 -*-


import arcpy
import importlib
import sys
import datetime

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")

log.log(u"Librería 'filtro.py' cargado con éxito")



mxd = arcpy.env.mxd

def fil_expr(capa_nombre, expr):     #Esta función acepta la cadena de expresión completa, ejemplo:---> "NOM_MUN = 'Jesús María' AND NOM_ENT = 'Aguascalientes'"

    tiempo_fil_expr_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    
    log.log(u"'filtro.fil_expr' iniciando para " + capa_nombre + u" con la expresión " + expr)
    
    try:
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        capa.definitionQuery = expr
        log.log(u"Filtro {} aplicado correctamente para la capa {}".format(expr, capa_nombre))
    except Exception as e:
        log.log(u">> ERROR, el proceso filtro '{}' falló para la capa '{}'".format(expr, capa_nombre))
        log.log(str(e))

    log.log(u"Se aplicó filtro con la expresión {} para la capa {}".format(expr, capa_nombre))

    tiempo_fil_expr_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'fil_expr': {}".format(tiempo.tiempo([tiempo_fil_expr_ini,tiempo_fil_expr_fin])))

    log.log(u"'filtro.fil_expr' finalizado para " + capa_nombre + u" con la expresión " + expr)


def aplicar_defq(capa_nombre, campo, texto_a_buscar):

    tiempo_aplicar_defq_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'filtro.plicar_defq' iniciando para " + capa_nombre + u" con la expresión " + campo)

    try:
        # Obtener el mapa actual
        mxd = arcpy.mapping.MapDocument(u"CURRENT")
        
        # Obtener la capa por su nombre
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        
        # Construir la expresión de consulta
        # expresion = u"{} LIKE '%{}%'".format(arcpy.AddFieldDelimiters(capa.dataSource, campo), texto_a_buscar) ------ expresión original sustituida por la línea siguiente
        expresion = campo + " = u" + texto_a_buscar
        
        # Aplicar el definition query a la capa
        capa.definitionQuery = expresion
        
        log.log(u"Definition query aplicado exitosamente.")
        
    except Exception as e:
        log.log(u">> ERROR, el proceso aplicar_defq falló")
        log.log(str(e))

    tiempo_aplicar_defq_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'aplicar_defq': {}".format(tiempo.tiempo([tiempo_aplicar_defq_ini,tiempo_aplicar_defq_fin])))

    log.log(u"'filtro.plicar_defq' finalizado para " + capa_nombre)

# Ejemplo de uso
# aplicar_defq(u"ESTATAL", u"NOMGEO", u"'Aguascalientes'")  <------ sintaxis correcta y verificada

def deshacer_defq(capa_nombre):

    tiempo_deshacer_defq_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    log.log(u"'filtro.plicar_defq' iniciando para " + capa_nombre + u" con la expresión " + campo)

    try:
        
        # Obtener la capa por su nombre
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        
        # Borrar el definition query
        capa.definitionQuery = u""
        
        log.log(u"Definition query eliminado, mostrando todos los objetos.")
        
    except Exception as e:
        log.log(u">> ERROR. Se ha producido un error aplicando 'filtro.plicar_defq' para: " + capa_nombre)
        log.log(str(e))
    
    tiempo_deshacer_defq_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(u"tiempo total de librería 'deshacer_defq': {}".format(tiempo.tiempo([tiempo_deshacer_defq_ini,tiempo_deshacer_defq_fin])))
    
    log.log(u"'filtro.plicar_defq' finalizado para " + capa_nombre)

# Ejemplo de uso
# deshacer_defq(u"ESTATAL") <------ sintaxis correcta y verificada
