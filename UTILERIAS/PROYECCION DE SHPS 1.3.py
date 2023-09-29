# -*- coding: utf-8 -*-

# SCRIPT PARA CAMBIAR DE PROYECCIÓN VARIOS ARCHIVOS SHP DE CARPETAS ESPECÍFICAS


import arcpy

# estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
#           "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
#           "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
#           "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
#           "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

estados = ["Oaxaca", "Puebla", "Querétaro", 
          "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
          "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

for estado in estados:
    
    print(estado + " en proceso...")

    folder = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia"
    
    cgs = "PROJCS['WGS_1984_UTM_Zone_13N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-105.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
    incgs = "PROJCS['Mexico_ITRF2008_LCC',GEOGCS['GCS_Mexico_ITRF2008',DATUM['D_Mexico_ITRF2008',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-102.0],PARAMETER['Standard_Parallel_1',17.5],PARAMETER['Standard_Parallel_2',29.5],PARAMETER['Latitude_Of_Origin',12.0],UNIT['Meter',1.0]]"
    
    ageb_urb = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/ageb_urb.shp" "';"
    eje_vial = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/eje_vial.shp" "';"
    estatal = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/estatal.shp" "';"
    loc_rur = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/loc_rur.shp" "';"
    loc_urb = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/loc_urb.shp" "';"
    manzana_localidad = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/manzana_localidad.shp" "';"
    municipal = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/municipal.shp" "';"
    servicios_a = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/servicios_a.shp" "';"
    servicios_l = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/servicios_l.shp" "';"
    servicios_p = "'" + "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/servicios_p.shp" "'"
    ifcd = ageb_urb + eje_vial + estatal + loc_rur + loc_urb + manzana_localidad + municipal + servicios_a + servicios_l + servicios_p

    archivos = ["ageb_urb", "eje_vial", "estatal", "loc_rur", "loc_urb", "manzana_localidad", "municipal", "servicios_a", "servicios_l", "servicios_p"]

    for archivo in archivos:
        shapefo = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/" + archivo + ".shp"
        shapefd = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/ITRF/" + archivo + ".shp"
        
        desc = arcpy.Describe(shapefo)
        sist_proy = desc.spatialReference
        sistema = sist_proy.name

        if not sistema == "WGS_1984_UTM_Zone_13N":
            
            if not arcpy.Exists(folder + "/ITRF"):
                arcpy.CreateFolder_management(out_folder_path=folder, out_name="ITRF")
                print(folder + " creada satisfactoriamente.")
            else:
                print(folder + "/ITRF ya existe, no se a creado la carpeta.")

            print("el archivo " + shapefo + " tiene una proyección distinta a WGS84")
            arcpy.CopyFeatures_management(in_features=shapefo, out_feature_class=shapefd, config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")
            if arcpy.Exists(shapefd):
                print(archivo + " en " + estado + " copiado correctamente, borrando " + archivo)
                arcpy.Delete_management(shapefo)
                print(shapefo + " borrado.")
                print("iniciando proyección de archivo " + str.upper(shapefo))
                arcpy.Project_management(in_dataset=shapefd, out_dataset=shapefo, out_coor_system=cgs, transform_method="Mexico_ITRF2008_To_WGS_1984_1", in_coor_system=incgs, preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
                print(str.upper(shapefo) + " proyectado adecuadamente")
            else:
                print("El archivo " + shapefo + " no se ha copiado adecuadamente, no es posible eliminarlo.")
        else:
            print(shapefo + " con proyección WGS 84")
            
    print(estado + " movido adecuadamente.")

    destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia"
    
    itrf = destino + "/ITRF"

    shap = arcpy.ListFeatureClasses("*", "All", itrf)
    if not shap:
        print("La carpeta " + itrf + " está vacía o no contiene shapefiles.")
        arcpy.Delete_management(itrf)
        if not arcpy.Exists(itrf):
            print("la carpeta " + itrf + " se ha borrado adecuadamente")
        else:
            print("Ha habido un error eliminando la carpeta " + itrf + " .")
    else:
        print("La carpeta " + itrf + " no está vacía y contiene shapefiles.")
print("proceso terminado en su totalidad!")
