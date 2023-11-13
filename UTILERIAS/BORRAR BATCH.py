# -*- coding: utf-8 -*-
# LIBRERÍA PARA BORRAR ARCHIVOS SHP DE LAS CARPETAS

def borrarcapa():

    import arcpy
    arcpy.env.overwriteOutput = True
    estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
            "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
            "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
            "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
            "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

    # estados = ["Aguascalientes"]

    # capa = "estado decr185"
    capa = "Carreteras"

    for estado in estados:
        print ("BUSCANDO " + estado)
        destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado,capa)
        if arcpy.Exists(destino):
            print("Borrando " + (destino))
            arcpy.Delete_management(destino)
        else:
            print("El archivo " + (destino) + " no existe")
    print ("proceso terminado para los estados")