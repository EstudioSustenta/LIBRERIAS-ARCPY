# -*- coding: utf-8 -*-

# SCRIPT PARA REALIZAR LAS SIGUIENTES FUNCIONES DE UNA MATRIZ:
# CLIP
# ERASE

def funcioncomp(func):

    import arcpy

    estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
            "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
            "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
            "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
            "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

    # estados = ["Aguascalientes", "Colima"]

    # origen = "Y:/GIS/MEXICO/VARIOS/INEGI/RED NACIONAL DE CAMINOS 2017/conjunto_de_datos/red_vial_wgs84utm.shp"
    # capaclip = "estado decr185.shp"
    capaorig = "red nacional de caminos"
    capatrabajo = "loc_urb"
    # capadest = "red nacional de caminos"
    capadest = "Calles urbanas"

    for estado in estados:
        print(estado + " CLIP en proceso...")
        origen = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado,capaorig)
        capatrab = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado,capatrabajo)
        destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/" + capadest +".shp"
        if not arcpy.Exists(destino):
            print("       " + capadest + " no existe en " + estado + ", creándolo...")
            
            if func == "clip":
                arcpy.Clip_analysis(in_features=origen, clip_features=capatrab, out_feature_class=destino, cluster_tolerance="")
            elif func == "erase":
                arcpy.Erase_analysis(in_features=origen, erase_features=capatrab, out_feature_class=destino, cluster_tolerance="")
            else:
                print("No se definió una función válida")

            print("       " + capadest + " creado en " + estado)
        else:
            print("       " + capadest + " ya existe en " + estado)
    print(" ")
    print("   PROCESO CONCLUIDO")


