import os

# Lista de subcarpetas a crear
existentes = [
    "denue_01_shp", "denue_02_shp", "denue_03_shp", "denue_04_shp", "denue_05_shp", "denue_06_shp", "denue_07_shp",
    "denue_08_shp", "denue_09_shp", "denue_10_shp", "denue_11_shp", "denue_12_shp", "denue_13_shp", "denue_14_shp",
    "denue_15_shp", "denue_16_shp", "denue_17_shp", "denue_18_shp", "denue_19_shp", "denue_20_shp", "denue_21_shp",
    "denue_22_shp", "denue_23_shp", "denue_24_shp", "denue_25_shp", "denue_26_shp", "denue_27_shp", "denue_28_shp",
    "denue_29_shp", "denue_30_shp", "denue_31_shp", "denue_32_shp"
]

# Ruta base donde se crearán las subcarpetas
ruta_base = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/"

def crear_carpetas():
    for subcarpeta in existentes:
        ruta_subcarpeta = os.path.join(ruta_base, subcarpeta)
        os.makedirs(ruta_subcarpeta)
        print("Carpeta creada: {}".format(ruta_subcarpeta))

# Llama a la función para crear las carpetas
crear_carpetas()
