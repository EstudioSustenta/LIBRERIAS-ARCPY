# ESTE SCRIPT APLICA LA FUNCIÓN "SELECT" EN UNA RUTA ESPECIFICA DE CARPETAS.
import arcpy
# arcpy.env.overwriteOutput = True
estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche","Chiapas", "Chihuahua", "Ciudad de México", 
          "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
          "México", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
          "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
          "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

# estados = ["Aguascalientes"]

origen = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/0 UBICACION/ESTATAL decr185.shp"
campo = "NOM_ENT"
archivo = "estado decr185.shp"

for estado in estados:
    print (str.upper(estado))
    clausula = "'" + chr(34)+ "NOMGEO" + chr(34) + " = " + "'" + estado + "''"
    clausula = "\"" + campo + "\" = '" + estado + "'"
    destino = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + estado + "/cartografia/" + archivo
    if not arcpy.Exists(destino):
        print ("extrayendo " + estado)
        arcpy.Select_analysis(in_features=origen, out_feature_class=destino, where_clause=clausula)
        print (estado + "extraído")
    else:
        print("El archivo " + "perfil " + archivo + " en " + estado + " ya existe")

print "PROCESO CONCLUIDO"