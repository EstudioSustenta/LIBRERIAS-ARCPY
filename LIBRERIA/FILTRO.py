# -*- coding: utf-8 -*-


import arcpy
import importlib
import sys

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module("LIBRERIA.archivo_log")

mxd = arcpy.env.mxd

log.log(u"filtro.py cargado con éxito")

def fil_expr(capa_nombre, expr):     #Esta función acepta la cadena de expresión completa, ejemplo:---> "NOM_MUN = 'Jesús María' AND NOM_ENT = 'Aguascalientes'"
    
    log.log(u"'filtro.fil_expr' iniciando para " + capa_nombre + u" con la expresión " + expr)
    
    try:
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        capa.definitionQuery = expr
        log.log(u"Filtro aplicado correctamente para la capa " + capa_nombre)
    except:
        log.log(u">> ERROR, el proceso filtro falló para la capa " + capa_nombre)

    log.log(u"'filtro.fil_expr' finalizado para " + capa_nombre)



def aplicar_defq(capa_nombre, campo, texto_a_buscar):
    try:
        # Obtener el mapa actual
        mxd = arcpy.mapping.MapDocument("CURRENT")
        
        # Obtener la capa por su nombre
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        
        # Construir la expresión de consulta
        # expresion = "{} LIKE '%{}%'".format(arcpy.AddFieldDelimiters(capa.dataSource, campo), texto_a_buscar) ------ expresión original sustituida por la línea siguiente
        expresion = campo + " = " + texto_a_buscar
        
        # Aplicar el definition query a la capa
        capa.definitionQuery = expresion
        
        print("Definition query aplicado exitosamente.")
        
    except Exception as e:
        print("Error:", str(e))

# Ejemplo de uso
# aplicar_defq("ESTATAL", "NOMGEO", "'Aguascalientes'")  <------ sintaxis correcta y verificada

import arcpy

def deshacer_defq(capa_nombre):
    try:
        # Obtener el mapa actual
        mxd = arcpy.mapping.MapDocument("CURRENT")
        
        # Obtener la capa por su nombre
        capa = arcpy.mapping.ListLayers(mxd, capa_nombre)[0]
        
        # Borrar el definition query
        capa.definitionQuery = ""
        
        print("Definition query eliminado, mostrando todos los objetos.")
        
    except Exception as e:
        print("Error:", str(e))

# Ejemplo de uso
# deshacer_defq("ESTATAL") <------ sintaxis correcta y verificada
