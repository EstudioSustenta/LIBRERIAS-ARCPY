# -*- coding: utf-8 -*-

# ----HACER IDENTITY DEL SISTEMA CON CAPAS DEFINIDAS

import arcpy
import os
import importlib
import sys
import codecs

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
ccapas = importlib.import_module("LIBRERIA.cargar_capas")
log = importlib.import_module("LIBRERIA.archivo_log")

mxd = arcpy.env.mxd
df = arcpy.env.df
log.log(u"'identity_sistema.py' cargado con éxito")
def idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter):
    
    log.log(u"'idproy.idproy' iniciando...")
    
    try:
        arch = rutaCl + "/" + capaCl
        archtxt = arcpy.env.carp_cliente + capa_salida + "-identity.txt"
        ruta_archivo = archtxt

        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo) # Elimina el archivo si existe
            log.log(u"El archivo " + ruta_archivo + u" ha sido eliminado.")
        else:
            log.log(u"El archivo " + ruta_archivo + u" no existe.")

        with codecs.open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write('Archivo de datos.\n')
            archivo.write('Archivo fuente: ' + rutaCl + capaCl + chr(10))
            archivo.write(chr(10))
            log.log(u"El archivo " + ruta_archivo + u" ha sido creado.")

        arcpy.env.overwriteOutput = True
        arcpy.Identity_analysis(in_features="SISTEMA", 
            identity_features=arch, 
            out_feature_class="Y:/0_SIG_PROCESO/X TEMPORAL/" + capa_salida + ".shp", 
            join_attributes="ALL", 
            cluster_tolerance="", 
            relationship="NO_RELATIONSHIPS")

        campos = arcpy.ListFields(capa_salida)
        nombres_de_campos = [campo.name for campo in campos]
        i = 0

        for nombre in nombres_de_campos:
            for cons in camposCons:
                if cons == nombre:
                    capatr = arcpy.mapping.Layer(capa_salida) # Obtén una referencia a la capa "uso de suelo" en el mapa actual
                    with arcpy.da.SearchCursor(capatr, nombre) as cursor: # Lee el primer registro
                        registro = next(cursor)
                    valor_del_campo = registro[0] # El valor del campo "DESCRIP" del primer registro se encuentra en registro[0]
                    if isinstance(valor_del_campo, int) or isinstance(valor_del_campo, float):
                        valor_del_campo = str(valor_del_campo)
                        if valor_del_campo == None:
                            valor_del_campo = "Sistema fuera de área de " + capa_salida
                    
                    with codecs.open(ruta_archivo, 'a', encoding='utf-8') as archivo:
                        archivo.write(nombre + chr(9) + dAlter[i] + chr(9) + valor_del_campo + chr(10))
                        i = i + 1
        ccapas.remover_capas(capa_salida)
        log.log(u"'idproy.idproy' Se ha ejecutado satisfactoriamente")
    except Exception as e:
        log.log(u">> ERROR, no se ha podido ejecutar identity_sistema.py adecuadamente")
        log.log(str(e))

    log.log(u"'idproy.idproy' finalizado")
