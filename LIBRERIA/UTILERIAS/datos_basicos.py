# -*- coding: utf-8 -*-

#RUTINA PARA GENERAR ARCHIVO DE datos_basicos DEL SISTEMA

# Agrega la ruta del paquete al path de Python
# import sys
# sys.path.append("Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS")
# sys.path.append('Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/UTILERIAS')

import arcpy
import datetime  # Importar módulo para obtener fecha y hora
import UTILERIAS.UTIL_JSON as UJ
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU


now = datetime.datetime.now()
fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
arcpy.env.fecha = fecha
# adbas = arcpy.env.adbas
# repet = arcpy.env.repet
# arch=arcpy.env.arch_log


def datosbasicos(arch_log,adbas):
    
    """
    Genera los datos básicos para el proyecto SIG
    genera variables de entorno tipo 'arcpy.env'
    y agrega información a un archivo .json
    """

    capa = u"Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"  # Ruta al archivo shapefile
    desc = arcpy.Describe(capa)         # Crear un objeto de descripción de capa
    proyeccion = desc.spatialReference      # Obtener la proyección

    # Imprimir la información de la proyección
    if proyeccion is not None:
        coordnombre = proyeccion.name
        coordtipo = proyeccion.type
        coordWKID = proyeccion.factoryCode
    else:
        coordnombre = u"Sin sistema de coordenadas definido"
        coordtipo = u"Sin tipo de sistema de coordenadas"
        coordWKID = u"Sin codigo WKID (ID de proyeccion)"
    
    # Leer el valor 'DESCRIP' del primer registro en el shapefile
    with arcpy.da.SearchCursor(capa, (u"DESCRIP")) as cursor:
        for row in cursor:
            proyecto = (row[0])
    with arcpy.da.SearchCursor(capa, (u"CLIENTE")) as cursor:
        for row in cursor:
            cliente = (row[0])
    with arcpy.da.SearchCursor(capa, (u"NOM_ENT")) as cursor:
        for row in cursor:
            estado = (row[0])
    with arcpy.da.SearchCursor(capa, (u"NOM_MUN")) as cursor:
        for row in cursor:
            municipio = (row[0])
    with arcpy.da.SearchCursor(capa, (u"NOM_LOC")) as cursor:
        for row in cursor:
            localidad = (row[0])
    with arcpy.da.SearchCursor(capa, (u"COLONIA")) as cursor:
        for row in cursor:
            colonia = (row[0])
    with arcpy.da.SearchCursor(capa, (u"ALTITUD")) as cursor:
        for row in cursor:
            altitud = (row[0])
    with arcpy.da.SearchCursor(capa, (u"AMBITO")) as cursor:
        for row in cursor:
            ambito = (row[0])
            if ambito == "U":
                ambito = u"Urbano"
            else:
                ambito = u"Rural"
    with arcpy.da.SearchCursor(capa, (u"CODIGOPOST")) as cursor:
        for row in cursor:
            cp = (row[0])     #código postal
    with arcpy.da.SearchCursor(capa, (u"CONTINENTA")) as cursor:
        for row in cursor:
            continentalidad = (row[0])    # continentalidad
    with arcpy.da.SearchCursor(capa, (u"CVE_SUN")) as cursor: # clave sistema urbano nacional
        for row in cursor:
            clavesun = (row[0])
    with arcpy.da.SearchCursor(capa, (u"CVELOC")) as cursor: # clave de localidad
        for row in cursor:
            claveloc = (row[0])
    with arcpy.da.SearchCursor(capa, (u"LAT")) as cursor: # latitud
        for row in cursor:
            latitud = (row[0])
    with arcpy.da.SearchCursor(capa, (u"LON")) as cursor: # longitud
        for row in cursor:
            longitud = (row[0])
    with arcpy.da.SearchCursor(capa, (u"POINT_X")) as cursor: # coordenada x
        for row in cursor:
            x = (row[0])
    with arcpy.da.SearchCursor(capa, (u"POINT_y")) as cursor: # coordenada y
        for row in cursor:
            y = (row[0])


    archivos = [
        # carp_cliente + "0 datos_basicos " + ".txt",
        arch_log,
        ]
    for archivo in archivos:
            ESU.log(("#" *60),archivo,postsalto=2,modo="w")
            ESU.log("",archivo,postsalto=2,modo="w",tabuladores=2,tiempo=True)
            ESU.log("DATOS GENERALES DEL PROYECTO",archivo,tabuladores=2)
            ESU.log("Fecha de creación: " + fecha,archivo,tabuladores=2)
            UJ.agdicson(adbas,"fecha", fecha)
            ESU.log("Autor: \t" + "Gustavo Martínez Velasco",archivo,postsalto=1,tabuladores=2)
            ESU.log("Proyecto: \t" + proyecto,archivo,tabuladores=2)
            UJ.agdicson(adbas,"proyecto", proyecto)
            ESU.log("Cliente: \t" + cliente,archivo,tabuladores=2)
            UJ.agdicson(adbas,"cliente", cliente)
            ESU.log("Estado: \t" + estado,archivo,tabuladores=2)
            UJ.agdicson(adbas,"estado", estado)
            ESU.log("Municipio: \t" + municipio,archivo,tabuladores=2)
            UJ.agdicson(adbas,"municipio", municipio)
            ESU.log("Localidad: \t" + localidad,archivo,tabuladores=2)
            UJ.agdicson(adbas,"localidad", localidad)
            ESU.log("Colonia: \t" + colonia,archivo,tabuladores=2)
            UJ.agdicson(adbas,"claveloc", claveloc)
            ESU.log("Localidad: \t" + claveloc,archivo,tabuladores=2)
            UJ.agdicson(adbas,"colonia", colonia)
            ESU.log("Codigo postal: \t" + cp,archivo,tabuladores=2)
            UJ.agdicson(adbas,"codigopostal", cp)
            ESU.log("Sistema urbano nacional: \t" + clavesun,archivo,tabuladores=2)
            UJ.agdicson(adbas,"clavesun", clavesun)
            ESU.log("Ambito urbano: \t" + ambito,archivo,postsalto=1,tabuladores=2)
            UJ.agdicson(adbas,"ambito", ambito)
            ESU.log("Sistema de coordenadas: \t" + coordnombre,archivo,tabuladores=2)
            UJ.agdicson(adbas,"coordnombre", coordnombre)
            ESU.log("Tipo de coordenadas: \t" + coordtipo,archivo,tabuladores=2)
            UJ.agdicson(adbas,"coordtipo", coordtipo)
            ESU.log("Clave WKID de coordenadas: \t" + str(coordWKID),archivo,tabuladores=2)
            UJ.agdicson(adbas,"coordWKID", coordWKID)
            ESU.log("Altitud (MSNMM): \t" + str(altitud),archivo,tabuladores=2)
            UJ.agdicson(adbas,"altitud", altitud)
            ESU.log("Latitud: \t" + str(latitud),archivo,tabuladores=2)
            UJ.agdicson(adbas,"latitud", latitud)
            ESU.log("Longitud: \t" + str(longitud),archivo,tabuladores=2)
            UJ.agdicson(adbas,"longitud", longitud)
            ESU.log("Coordenada X: \t" + str(x),archivo,tabuladores=2)
            UJ.agdicson(adbas,"x", x)
            ESU.log("Coordenada Y: \t" + str(y),archivo,tabuladores=2)
            UJ.agdicson(adbas,"y", y)
            ESU.log("Continentalidad (km): \t" + str(continentalidad),archivo,postsalto=1,tabuladores=2)
            UJ.agdicson(adbas,"continentalidad", continentalidad)

    ESU.log("Proceso de datos basicos realizado satisfactoriamente",archivo,presalto=1)

    return "dbas ejecutado correctamente"
