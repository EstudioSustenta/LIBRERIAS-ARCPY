# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR CLIP DE UNA MATRIZ.

import arcpy

estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
          "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
          "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
          "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
          "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

# estados = ["Aguascalientes", "Colima"]

origen = "Y:/GIS/MEXICO/VARIOS/INEGI/RED NACIONAL DE CAMINOS 2017/conjunto_de_datos/red_vial_wgs84utm.shp"
capaclip = "estado decr185.shp"
capadest = "red nacional de caminos"

for estado in estados:
    print(estado + " CLIP en proceso...")
    clip = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/" + capaclip
    destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/" + capadest +".shp"
    if not arcpy.Exists(destino):
        print("       " + capadest + " no existe en " + estado + ", creándolo...")
        arcpy.Clip_analysis(in_features=origen, clip_features=clip, out_feature_class=destino, cluster_tolerance="")
        print("       " + capadest + " creado en " + estado)
    else:
        print("       " + capadest + " ya existe en " + estado)
print(" ")
print("   PROCESO CONCLUIDO")