# -*- coding: utf-8 -*-

#RUTINA PARA GENERAR ARCHIVO DE datos_basicos DEL SISTEMA

import arcpy
import sys
import codecs
import datetime  # Importar módulo para obtener fecha y hora
import importlib

# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)
log = importlib.import_module(u"LIBRERIA.archivo_log")

reload (log)

# from datetime import datetime
now = datetime.datetime.now()
fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
arcpy.env.fecha = fecha

repet = arcpy.env.repet
log.log(repet,u"datos básicos cargado con éxito")

def datosbasicos():

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    log.log(repet,u"'datos_basicos.datosbasicos' iniciando...")

    capa = u"Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"  # Ruta al archivo shapefile

    # Crear un objeto de descripción de capa
    desc = arcpy.Describe(capa)

    # Obtener la proyección
    proyeccion = desc.spatialReference

    # Imprimir la información de la proyección
    if proyeccion is not None:
        arcpy.env.coordnombre = proyeccion.name
        arcpy.env.coordtipo = proyeccion.type
        arcpy.env.coordWKID = proyeccion.factoryCode
        log.log(repet,u"Sistema de coordenadas: " + arcpy.env.coordnombre)
        log.log(repet,u"Tipo de coordenadas: " + arcpy.env.coordtipo)
        log.log(repet,u"Código WKID de coordenadas" + str(arcpy.env.coordWKID))
    else:
        log.log(repet,u"La capa no tiene una proyección definida.")
        arcpy.env.coordnombre = u"Sin sistema de coordenadas definido"
        arcpy.env.coordtipo = u"Sin tipo de sistema de coordenadas"
        arcpy.env.coordWKID = u"Sin codigo WKID (ID de proyeccion)"
    

    
    # Leer el valor 'DESCRIP' del primer registro en el shapefile
    with arcpy.da.SearchCursor(capa, (u"DESCRIP")) as cursor:
        for row in cursor:
            arcpy.env.proyecto = (row[0])
            log.log(repet,arcpy.env.proyecto)
    
    with arcpy.da.SearchCursor(capa, (u"CLIENTE")) as cursor:
        for row in cursor:
            arcpy.env.cliente = (row[0])
            log.log(repet,arcpy.env.cliente)
    
    with arcpy.da.SearchCursor(capa, (u"NOM_ENT")) as cursor:
        for row in cursor:
            arcpy.env.estado = (row[0])
            log.log(repet,arcpy.env.estado)

    with arcpy.da.SearchCursor(capa, (u"NOM_MUN")) as cursor:
        for row in cursor:
            arcpy.env.municipio = (row[0])
            log.log(repet,arcpy.env.municipio)

    with arcpy.da.SearchCursor(capa, (u"NOM_LOC")) as cursor:
        for row in cursor:
            arcpy.env.localidad = (row[0])
            log.log(repet,arcpy.env.localidad)

    with arcpy.da.SearchCursor(capa, (u"COLONIA")) as cursor:
        for row in cursor:
            arcpy.env.colonia = (row[0])
            log.log(repet,arcpy.env.colonia)

    with arcpy.da.SearchCursor(capa, (u"ALTITUD")) as cursor:
        for row in cursor:
            arcpy.env.altitud = (row[0])
            log.log(repet,str(arcpy.env.altitud))

    with arcpy.da.SearchCursor(capa, (u"AMBITO")) as cursor:
        for row in cursor:
            ambito = (row[0])
            if ambito == "U":
                ambito = u"Urbano"
            else:
                ambito = u"Rural"
    arcpy.env.ambito = ambito
    log.log(repet,arcpy.env.ambito)

    with arcpy.da.SearchCursor(capa, (u"CODIGOPOST")) as cursor:
        for row in cursor:
            arcpy.env.cp = (row[0])     #código postal
            log.log(repet,str(arcpy.env.cp))

    with arcpy.da.SearchCursor(capa, (u"CONTINENTA")) as cursor:
        for row in cursor:
            arcpy.env.continentalidad = (row[0])    # continentalidad
            log.log(repet,str(arcpy.env.continentalidad))
    
    with arcpy.da.SearchCursor(capa, (u"CVE_SUN")) as cursor: # clave sistema urbano nacional
        for row in cursor:
            arcpy.env.clavesun = (row[0])
            # log.log(repet,arcpy.env.clavesun)

    with arcpy.da.SearchCursor(capa, (u"CVELOC")) as cursor: # clave de localidad
        for row in cursor:
            arcpy.env.claveloc = (row[0])
            # log.log(repet,arcpy.env.claveloc)

    with arcpy.da.SearchCursor(capa, (u"LAT")) as cursor: # latitud
        for row in cursor:
            arcpy.env.latitud = (row[0])
            # log.log(repet,arcpy.env.latitud)

    with arcpy.da.SearchCursor(capa, (u"LON")) as cursor: # longitud
        for row in cursor:
            arcpy.env.longitud = (row[0])
            # log.log(repet,arcpy.env.longitud)

    with arcpy.da.SearchCursor(capa, (u"POINT_X")) as cursor: # coordenada x
        for row in cursor:
            arcpy.env.x = (row[0])
            # log.log(repet,arcpy.env.x)

    with arcpy.da.SearchCursor(capa, (u"POINT_y")) as cursor: # coordenada y
        for row in cursor:
            arcpy.env.y = (row[0])
            # log.log(repet,arcpy.env.y)

    fechahora = (now.strftime(u"%Y-%m-%d %H:%M:%S")).replace(":", "-")
    log.log(repet,str(arcpy.env.fechahora))

    archivo1 = arcpy.env.carp_cliente + "0 datos_basicos " + fechahora + ".txt"
    archivo2 = arcpy.env.archivolog

    log.log(repet,archivo1)
    log.log(repet,archivo2)
    

    archivos = [archivo1, archivo2]

    for archivo in archivos:
        with codecs.open(archivo, 'w', encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
            archivo.write(u"DATOS GENERALES DEL PROYECTO" + '\n')
            archivo.write(u"Fecha de creación: " + arcpy.env.fecha + '\n')
            archivo.write(u"Autor: \t" + "Gustavo Martinez Velasco" + '\n\n')
            archivo.write(u"Proyecto: \t" + arcpy.env.proyecto + '\n')
            archivo.write(u"Cliente: \t" + arcpy.env.cliente + '\n')
            archivo.write(u"Estado: \t" + arcpy.env.estado + '\n')
            archivo.write(u"Municipio: \t" + arcpy.env.municipio + '\n')
            archivo.write(u"Localidad: \t" + arcpy.env.localidad + '\n')
            archivo.write(u"Colonia: \t" + arcpy.env.colonia + '\n')
            archivo.write(u"Codigo postal: \t" + arcpy.env.cp + '\n')
            archivo.write(u"Sistema urbano nacional: \t" + arcpy.env.clavesun + '\n')
            archivo.write(u"Ambito urbano: \t" + arcpy.env.ambito + '\n\n')
            archivo.write(u"Sistema de coordenadas: \t" + arcpy.env.coordnombre + '\n')
            archivo.write(u"Tipo de coordenadas: \t" + arcpy.env.coordtipo + '\n')
            archivo.write(u"Clave WKID de coordenadas: \t" + str(arcpy.env.coordWKID) + '\n')
            archivo.write(u"Altitud (MSNMM): \t" + str(arcpy.env.altitud) + '\n')
            archivo.write(u"Latitud: \t" + str(arcpy.env.latitud) + '\n')
            archivo.write(u"Longitud: \t" + str(arcpy.env.longitud) + '\n')
            archivo.write(u"Coordenada X: \t" + str(arcpy.env.x) + '\n')
            archivo.write(u"Coordenada Y: \t" + str(arcpy.env.y) + '\n')
            archivo.write(u"Continentalidad (km): \t" + str(arcpy.env.continentalidad) + '\n\n')
            archivo.write(u"Ruta de carpeta de proyecto: \t" + arcpy.env.carp_cliente)

    print(u"Proceso de datos basicos realizado satisfactoriamente")

    arcpy.env.repet = arcpy.env.repet - 1
