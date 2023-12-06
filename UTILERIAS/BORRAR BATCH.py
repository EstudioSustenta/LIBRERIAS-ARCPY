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

    lista_denue_shp = [
        "denue_01_shp", "denue_02_shp", "denue_03_shp", "denue_04_shp", "denue_05_shp", "denue_06_shp", "denue_07_shp",
        "denue_08_shp", "denue_09_shp", "denue_10_shp", "denue_11_shp", "denue_12_shp", "denue_13_shp", "denue_14_shp",
        "denue_15_shp", "denue_16_shp", "denue_17_shp", "denue_18_shp", "denue_19_shp", "denue_20_shp", "denue_21_shp",
        "denue_22_shp", "denue_23_shp", "denue_24_shp", "denue_25_shp", "denue_26_shp", "denue_27_shp", "denue_28_shp",
        "denue_29_shp", "denue_30_shp", "denue_31_shp", "denue_32_shp"]


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