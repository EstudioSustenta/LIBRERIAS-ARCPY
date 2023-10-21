# -*- coding: utf-8 -*-

#RUTINA PARA GENERAR ARCHIVO DE datos_basicos DEL SISTEMA

import arcpy
import sys
import codecs

def datosbasicos():
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
    else:
        print(u"La capa no tiene una proyección definida.")
        arcpy.env.coordnombre = u"Sin sistema de coordenadas definido"
        arcpy.env.coordtipo = u"Sin tipo de sistema de coordenadas"
        arcpy.env.coordWKID = u"Sin codigo WKID (ID de proyeccion)"
    

    
    # Leer el valor 'DESCRIP' del primer registro en el shapefile
    with arcpy.da.SearchCursor(capa, (u"DESCRIP")) as cursor:
        for row in cursor:
            arcpy.env.proyecto = (row[0])
    
    with arcpy.da.SearchCursor(capa, (u"CLIENTE")) as cursor:
        for row in cursor:
            arcpy.env.cliente = (row[0])
    
    with arcpy.da.SearchCursor(capa, (u"NOM_ENT")) as cursor:
        for row in cursor:
            arcpy.env.estado = (row[0])

    with arcpy.da.SearchCursor(capa, (u"NOM_MUN")) as cursor:
        for row in cursor:
            arcpy.env.municipio = (row[0])

    with arcpy.da.SearchCursor(capa, (u"NOM_LOC")) as cursor:
        for row in cursor:
            arcpy.env.localidad = (row[0])

    with arcpy.da.SearchCursor(capa, (u"COLONIA")) as cursor:
        for row in cursor:
            arcpy.env.colonia = (row[0])

    import datetime  # Importar módulo para obtener fecha y hora
    from datetime import datetime
    now = datetime.now()
    fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
    arcpy.env.fecha = fecha

    with arcpy.da.SearchCursor(capa, (u"ALTITUD")) as cursor:
        for row in cursor:
            arcpy.env.altitud = (row[0])

    with arcpy.da.SearchCursor(capa, (u"AMBITO")) as cursor:
        for row in cursor:
            ambito = (row[0])
            if ambito == "U":
                ambito = u"Urbano"
            else:
                ambito = u"Rural"
    arcpy.env.ambito = ambito

    with arcpy.da.SearchCursor(capa, (u"CODIGOPOST")) as cursor:
        for row in cursor:
            arcpy.env.cp = (row[0])     #código postal

    with arcpy.da.SearchCursor(capa, (u"CONTINENTA")) as cursor:
        for row in cursor:
            arcpy.env.continentalidad = (row[0])    # continentalidad
    
    with arcpy.da.SearchCursor(capa, (u"CVE_SUN")) as cursor: # clave sistema urbano nacional
        for row in cursor:
            arcpy.env.clavesun = (row[0])

    with arcpy.da.SearchCursor(capa, (u"CVELOC")) as cursor: # clave de localidad
        for row in cursor:
            arcpy.env.claveloc = (row[0])

    with arcpy.da.SearchCursor(capa, (u"LAT")) as cursor: # latitud
        for row in cursor:
            arcpy.env.latitud = (row[0])

    with arcpy.da.SearchCursor(capa, (u"LON")) as cursor: # longitud
        for row in cursor:
            arcpy.env.longitud = (row[0])

    with arcpy.da.SearchCursor(capa, (u"POINT_X")) as cursor: # coordenada x
        for row in cursor:
            arcpy.env.x = (row[0])

    with arcpy.da.SearchCursor(capa, (u"POINT_y")) as cursor: # coordenada y
        for row in cursor:
            arcpy.env.y = (row[0])

    now = datetime.now()
    fecha = str(now.date())  # Obtener la fecha actual en formato de cadena
    print (fecha)
    arcpy.env.fecha = fecha


    archivo1 = arcpy.env.carp_cliente + "0 datos_basicos.txt"
    archivo2 = arcpy.env.carp_cliente + "00 archivo_log.txt"

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
        
    
