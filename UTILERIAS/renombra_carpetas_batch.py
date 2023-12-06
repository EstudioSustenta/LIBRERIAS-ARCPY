# -*- coding: utf-8 -*-

import os
import arcpy

# Lista de subcarpetas a verificar
existentes = [
    "denue_01_shp", "denue_02_shp", "denue_03_shp", "denue_04_shp", "denue_05_shp", "denue_06_shp", "denue_07_shp",
    "denue_08_shp", "denue_09_shp", "denue_10_shp", "denue_11_shp", "denue_12_shp", "denue_13_shp", "denue_14_shp",
    "denue_15_shp", "denue_16_shp", "denue_17_shp", "denue_18_shp", "denue_19_shp", "denue_20_shp", "denue_21_shp",
    "denue_22_shp", "denue_23_shp", "denue_24_shp", "denue_25_shp", "denue_26_shp", "denue_27_shp", "denue_28_shp",
    "denue_29_shp", "denue_30_shp", "denue_31_shp", "denue_32_shp"
]

estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
    "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
    "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
    "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
    "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

# Carpeta base donde se buscarán las subcarpetas
carpeta_base = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/"

def renombra_dir():
    i = 0
    for subcarpeta in existentes:

        ruta_subcarpeta = "{}{}".format(carpeta_base, subcarpeta)
        estado = "{}{}".format(carpeta_base, estados[i])

        existente = ruta_subcarpeta
        nueva = estado

        if os.path.exists(existente) and os.path.isdir(existente):
            try:
                arcpy.Rename_management(existente, nueva)
                print ("La carpeta {} fue renombrada como {}".format(existente,nueva))
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
        else:
            resultado = "La subcarpeta '{}' NO existe en la carpeta base.".format(existente)
            print resultado
        i += 1

renombra_dir()