# -*- coding: utf-8 -*-

#RUTINA PARA GENERAR ARCHIVO DE datos_basicos DEL SISTEMA

import arcpy
import sys
import codecs

def datosbasicos():
    capa = "Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"  # Ruta al archivo shapefile

    # Crear un objeto de descripción de capa
    desc = arcpy.Describe(capa)

    # Obtener la proyección
    proyeccion = desc.spatialReference

    # Imprimir la información de la proyección
    if proyeccion is not None:
        arcpy.env.coordnombre = proyeccion.name
        arcpy.env.coordtipo = proyeccion.type
        arcpy.env.coordWKID = proyeccion.factoryCode
    else:
        print(u"La capa no tiene una proyección definida.")
        arcpy.env.coordnombre = u"Sin sistema de coordenadas definido"
        arcpy.env.coordtipo = u"Sin tipo de sistema de coordenadas"
        arcpy.env.coordWKID = u"Sin codigo WKID (ID de proyeccion)"
    

    
    # Leer el valor 'DESCRIP' del primer registro en el shapefile
    with arcpy.da.SearchCursor(capa, ("DESCRIP")) as cursor:
        for row in cursor:
            arcpy.env.proyecto = (row[0])
    
    with arcpy.da.SearchCursor(capa, ("CLIENTE")) as cursor:
        for row in cursor:
            arcpy.env.cliente = (row[0])
    
    with arcpy.da.SearchCursor(capa, ("NOM_ENT")) as cursor:
        for row in cursor:
            arcpy.env.estado = (row[0])

    with arcpy.da.SearchCursor(capa, ("NOM_MUN")) as cursor:
        for row in cursor:
            arcpy.env.municipio = (row[0])

    with arcpy.da.SearchCursor(capa, ("NOM_LOC")) as cursor:
        for row in cursor:
            arcpy.env.localidad = (row[0])

    with arcpy.da.SearchCursor(capa, ("COLONIA")) as cursor:
        for row in cursor:
            arcpy.env.colonia = (row[0])

    import datetime  # Importar módulo para obtener fecha y hora
    from datetime import datetime
    now = datetime.now()
    fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
    arcpy.env.fecha = fecha

    with arcpy.da.SearchCursor(capa, ("ALTITUD")) as cursor:
        for row in cursor:
            arcpy.env.altitud = (row[0])

    with arcpy.da.SearchCursor(capa, ("AMBITO")) as cursor:
        for row in cursor:
            ambito = (row[0])
            if ambito == "U":
                ambito = "Urbano"
            else:
                ambito = "Rural"
    arcpy.env.ambito = ambito

    with arcpy.da.SearchCursor(capa, ("CODIGOPOST")) as cursor:
        for row in cursor:
            arcpy.env.cp = (row[0])     #código postal

    with arcpy.da.SearchCursor(capa, ("CONTINENTA")) as cursor:
        for row in cursor:
            arcpy.env.continentalidad = (row[0])    # continentalidad
    
    with arcpy.da.SearchCursor(capa, ("CVE_SUN")) as cursor: # clave sistema urbano nacional
        for row in cursor:
            arcpy.env.clavesun = (row[0])

    with arcpy.da.SearchCursor(capa, ("CVELOC")) as cursor: # clave de localidad
        for row in cursor:
            arcpy.env.claveloc = (row[0])

    with arcpy.da.SearchCursor(capa, ("LAT")) as cursor: # latitud
        for row in cursor:
            arcpy.env.latitud = (row[0])

    with arcpy.da.SearchCursor(capa, ("LON")) as cursor: # longitud
        for row in cursor:
            arcpy.env.longitud = (row[0])

    with arcpy.da.SearchCursor(capa, ("POINT_X")) as cursor: # coordenada x
        for row in cursor:
            arcpy.env.x = (row[0])

    with arcpy.da.SearchCursor(capa, ("POINT_y")) as cursor: # coordenada y
        for row in cursor:
            arcpy.env.y = (row[0])

    now = datetime.now()
    fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
    print (fecha)
    arcpy.env.fecha = fecha


    archivo = arcpy.env.carp_cliente + "0 datos_basicos.txt"

    with codecs.open(archivo, 'w', encoding='utf-8') as archivo: # se usa la codificación utf-8 para evitar problemas con acentos y caracteres especiales
        archivo.write(u"DATOS GENERALES DEL PROYECTO" + '\n')
        archivo.write(u"Fecha de creación: " + arcpy.env.fecha + '\n')
        archivo.write(u"Autor: " + chr(9) + "Gustavo Martinez Velasco" + '\n\n')
        archivo.write(u"Proyecto: " + chr(9) + arcpy.env.proyecto + '\n')
        archivo.write(u"Cliente: " + chr(9) + arcpy.env.cliente + '\n')
        archivo.write(u"Estado: " + chr(9) + arcpy.env.estado + '\n')
        archivo.write(u"Municipio: " + chr(9) + arcpy.env.municipio + '\n')
        archivo.write(u"Localidad: " + chr(9) + arcpy.env.localidad + '\n')
        archivo.write(u"Colonia: " + chr(9) + arcpy.env.colonia + '\n')
        archivo.write(u"Codigo postal: " + chr(9) + arcpy.env.cp + '\n')
        archivo.write(u"Sistema urbano nacional: " + chr(9) + arcpy.env.clavesun + '\n')
        archivo.write(u"Ambito urbano: " + chr(9) + arcpy.env.ambito + '\n\n')
        archivo.write(u"Sistema de coordenadas: " + chr(9) + arcpy.env.coordnombre + '\n')
        archivo.write(u"Tipo de coordenadas: " + chr(9) + arcpy.env.coordtipo + '\n')
        archivo.write(u"Clave WKID de coordenadas: " + chr(9) + str(arcpy.env.coordWKID) + '\n')
        archivo.write(u"Altitud (MSNMM): " + chr(9) + str(arcpy.env.altitud) + '\n')
        archivo.write(u"Latitud: " + chr(9) + str(arcpy.env.latitud) + '\n')
        archivo.write(u"Longitud: " + chr(9) + str(arcpy.env.longitud) + '\n')
        archivo.write(u"Coordenada X: " + chr(9) + str(arcpy.env.x) + '\n')
        archivo.write(u"Coordenada Y: " + chr(9) + str(arcpy.env.y) + '\n')
        archivo.write(u"Continentalidad (km): " + chr(9) + str(arcpy.env.continentalidad) + '\n\n')
        archivo.write(u"Ruta de carpeta de proyecto: " + chr(9) + arcpy.env.carp_cliente)

    print("Proceso de datos basicos realizado satisfactoriamente")
        
    
