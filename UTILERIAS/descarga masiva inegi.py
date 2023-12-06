# Se realiza una descarga masiva de los archivos en la lista 'zips' y se guerdan en 

import urllib.request


zips = [    "denue_01_shp.zip",
            "denue_02_shp.zip",
            "denue_03_shp.zip",
            "denue_04_shp.zip",
            "denue_05_shp.zip",
            "denue_06_shp.zip",
            "denue_07_shp.zip",
            "denue_08_shp.zip",
            "denue_09_shp.zip",
            "denue_10_shp.zip",
            "denue_11_shp.zip",
            "denue_12_shp.zip",
            "denue_13_shp.zip",
            "denue_14_shp.zip",
            "denue_15_1_shp.zip",
            "denue_15_2_shp.zip",
            "denue_15_shp.zip",
            "denue_16_shp.zip",
            "denue_17_shp.zip",
            "denue_18_shp.zip",
            "denue_19_shp.zip",
            "denue_20_shp.zip",
            "denue_21_shp.zip",
            "denue_22_shp.zip",
            "denue_23_shp.zip",
            "denue_24_shp.zip",
            "denue_25_shp.zip",
            "denue_26_shp.zip",
            "denue_27_shp.zip",
            "denue_28_shp.zip",
            "denue_29_shp.zip",
            "denue_30_shp.zip",
            "denue_31_shp.zip",
            "denue_32_shp.zip"
        ]

estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", "Colima", 
    "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", 
    "México 01", "México 02", "Michoacán de Ocampo", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
    "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
    "Veracruz de Ignacio de la Llave", "Yucatán", "Zacatecas"]

def descarga_mass():
    print("Iniciando descarga...")
    i = 0
    for zip in zips:
        
        url = "https://www.inegi.org.mx/contenidos/masiva/denue/".format(zip)
        destino = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/{}/{}".format(estados[i],zip)

        try:
            urllib.request.urlretrieve(url, destino)
            print("Descarga exitosa.")
        except urllib.error.URLError as e:
            print("Error al descargar el archivo: {}".format(e))
        i += 1
    print("descarga finalizada!")
