# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR EL PROCESO DE IDENTITI DE DOS ARCHIVOS SHP


import arcpy


# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "COLONIAS", "MUNICIPAL CENSO 2020 DECRETO 185"

# origen = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
#           "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
#           "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
#           "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
#           "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]
# 
origen = ["Chiapas"]


for estado in origen:
    
    ruta = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/manzana.shp"
    destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/manzana_localidad.shp"
    identidad = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/loc_urb.shp"
    
    print(str.upper(estado) + " en proceso de identidad...")
    arcpy.Identity_analysis(in_features=ruta, identity_features=identidad, out_feature_class=destino, join_attributes="ALL", cluster_tolerance="", relationship="NO_RELATIONSHIPS")
    print(str.upper(estado) + " identidad aplicada satisfactoriamente...")
    if arcpy.Exists(destino):
        print(destino + " en " + str.upper(estado) + " copiado correctamente, borrando origen...")
        arcpy.Delete_management(ruta)
        print(str.upper(ruta) + " borrado.")
    else:
       print("La identidad de " + str.upper(ruta) + " no se ha ejecutado adecuadamente, no es posible eliminarlo.")

    print(str.upper(estado) + " terminado!")
print("Proceso terminado.")