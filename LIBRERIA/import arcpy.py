import arcpy
import codecs
import datetime

def obtener_datos_basicos():
    capa = "Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"  # Ruta al archivo shapefile

    # Crear un objeto de descripción de capa
    desc = arcpy.Describe(capa)

    # Obtener la proyección
    proyeccion = desc.spatialReference

    # Dictionary to store data
    datos_basicos = {}

    # Store proyeccion data
    if proyeccion is not None:
        datos_basicos['coordnombre'] = proyeccion.name
        datos_basicos['coordtipo'] = proyeccion.type
        datos_basicos['coordWKID'] = proyeccion.factoryCode
    else:
        print(u"La capa no tiene una proyección definida.")
        datos_basicos['coordnombre'] = u"Sin sistema de coordenadas definido"
        datos_basicos['coordtipo'] = u"Sin tipo de sistema de coordenadas"
        datos_basicos['coordWKID'] = u"Sin codigo WKID (ID de proyeccion)"

    # Leer el valor 'DESCRIP' del primer registro en el shapefile
    with arcpy.da.SearchCursor(capa, ("DESCRIP")) as cursor:
        for row in cursor:
            datos_basicos['proyecto'] = row[0]

    with arcpy.da.SearchCursor(capa, ("CLIENTE")) as cursor:
        for row in cursor:
            datos_basicos['cliente'] = row[0]

    with arcpy.da.SearchCursor(capa, ("NOM_ENT")) as cursor:
        for row in cursor:
            datos_basicos['estado'] = row[0]

    with arcpy.da.SearchCursor(capa, ("NOM_MUN")) as cursor:
        for row in cursor:
            datos_basicos['municipio'] = row[0]

    with arcpy.da.SearchCursor(capa, ("NOM_LOC")) as cursor:
        for row in cursor:
            datos_basicos['localidad'] = row[0]

    with arcpy.da.SearchCursor(capa, ("COLONIA")) as cursor:
        for row in cursor:
            datos_basicos['colonia'] = row[0]

    now = datetime.datetime.now()
    fecha = str(now.date())
    datos_basicos['fecha'] = fecha

    with arcpy.da.SearchCursor(capa, ("ALTITUD")) as cursor:
        for row in cursor:
            datos_basicos['altitud'] = row[0]

    with arcpy.da.SearchCursor(capa, ("AMBITO")) as cursor:
        for row in cursor:
            ambito = row[0]
            datos_basicos['ambito'] = "Urbano" if ambito == "U" else "Rural"

    with arcpy.da.SearchCursor(capa, ("CODIGOPOST")) as cursor:
        for row in cursor:
            datos_basicos['cp'] = row[0]

    with arcpy.da.SearchCursor(capa, ("CONTINENTA")) as cursor:
        for row in cursor:
            datos_basicos['continentalidad'] = row[0]

    with arcpy.da.SearchCursor(capa, ("CVE_SUN")) as cursor:
        for row in cursor:
            datos_basicos['clavesun'] = row[0]

    with arcpy.da.SearchCursor(capa, ("CVELOC")) as cursor:
        for row in cursor:
            datos_basicos['claveloc'] = row[0]

    with arcpy.da.SearchCursor(capa, ("LAT")) as cursor:
        for row in cursor:
            datos_basicos['latitud'] = row[0]

    with arcpy.da.SearchCursor(capa, ("LON")) as cursor:
        for row in cursor:
            datos_basicos['longitud'] = row[0]

    with arcpy.da.SearchCursor(capa, ("POINT_X")) as cursor:
        for row in cursor:
            datos_basicos['x'] = row[0]

    with arcpy.da.SearchCursor(capa, ("POINT_y")) as cursor:
        for row in cursor:
            datos_basicos['y'] = row[0]

    return datos_basicos

def escribir_archivo(datos_basicos, carp_cliente, file_name):
    archivo = carp_cliente + file_name

    with codecs.open(archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(u"DATOS GENERALES DEL PROYECTO" + '\n')
        archivo.write(u"Fecha de creación: " + datos_basicos['fecha'] + '\n')
        archivo.write(u"Autor: " + chr(9) + "Gustavo Martinez Velasco" + '\n\n')
        archivo.write(u"Proyecto: " + chr(9) + datos_basicos['proyecto'] + '\n')
        archivo.write(u"Cliente: " + chr(9) + datos_basicos['cliente'] + '\n')
        archivo.write(u"Estado: " + chr(9) + datos_basicos['estado'] + '\n')
        archivo.write(u"Municipio: " + chr(9) + datos_basicos['municipio'] + '\n')
        archivo.write(u"Localidad: " + chr(9) + datos_basicos['localidad'] + '\n')
        archivo.write(u"Colonia: " + chr(9) + datos_basicos['colonia'] + '\n')
        archivo.write(u"Codigo postal: " + chr(9) + datos_basicos['cp'] + '\n')
        archivo.write(u"Sistema urbano nacional: " + chr(9) + datos_basicos['clavesun'] + '\n')
        archivo.write(u"Ambito urbano: " + chr(9) + datos_basicos['ambito'] + '\n\n')
        archivo.write(u"Sistema de coordenadas: " + chr(9) + datos_basicos['coordnombre'] + '\n')
        archivo.write(u"Tipo de coordenadas: " + chr(9) + datos_basicos['coordtipo'] + '\n')
        archivo.write(u"Clave WKID de coordenadas: " + chr(9) + str(datos_basicos['coordWKID']) + '\n')
        archivo.write(u"Altitud (MSNMM): " + chr(9) + str(datos_basicos['altitud']) + '\n')
        archivo.write(u"Latitud: " + chr(9) + str(datos_basicos['latitud']) + '\n')
        archivo.write(u"Longitud: " + chr(9) + str(datos_basicos['longitud']) + '\n')
        archivo.write(u"Coordenada X: " + chr(9) + str(datos_basicos['x']) + '\n')
        archivo.write(u"Coordenada Y: " + chr(9) + str(datos_basicos['y']) + '\n')
        archivo.write(u"Continentalidad (km): " + chr(9) + str(datos_basicos['continentalidad']) + '\n\n')
        archivo.write(u"Ruta de carpeta de proyecto: " + chr(9) + carp_cliente)

    print("Proceso de datos básicos realizado satisfactoriamente")


# Call the functions to execute
datos_basicos = obtener_datos_basicos()
escribir_archivo(datos_basicos, arcpy.env.carp_cliente, "1 DATOS BASICOS.txt")