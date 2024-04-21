# ESTE SCRIPT DESCOMPRIME TODOS LOS ARCHIVOS .ZIP EN LA CARPETA DE SU UBICACIÓN, MEDIENTE LA SELECCIÓN
# DE UNA CARPETA, BUSCA EN TODAS LAS SUBCARPETAS Y REALIZA LAS ACCIONES CORRESPONDIENTES.


import arcpy
import os
import zipfile
import tkFileDialog  # En Python 2.7, se utiliza tkFileDialog en lugar de filedialog



# Función para descomprimir archivos zip en una carpeta y sus subcarpetas
def descomprimir_zip_en_carpeta(carpeta):
    for ruta, carpetas, archivos in os.walk(carpeta):
        print("Revisando carpeta {}".format(ruta))
        for archivo in archivos:
            print("Revisando {}".format(archivo))
            if archivo.endswith(".zip"):
                print("Zip encontrado: '{}'".format(archivo))
                ruta_completa = os.path.join(ruta, archivo)
                # descomprimir_zip(ruta_completa, ruta)

# Función para descomprimir un archivo zip
def descomprimir_zip(archivo_zip, carpeta_destino):
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_destino)

# Crear una ventana de selección de carpeta utilizando Tkinter
root = Tk()
root.withdraw()  # Ocultar la ventana principal de Tkinter

# Mostrar el cuadro de diálogo para seleccionar una carpeta
carpeta_seleccionada = tkFileDialog.askdirectory(title="Seleccionar Carpeta con Archivos ZIP")

# Verificar si se seleccionó una carpeta
if carpeta_seleccionada:
    try:
        # Descomprimir archivos zip en la carpeta seleccionada y subcarpetas
        descomprimir_zip_en_carpeta(carpeta_seleccionada)
        print("Archivos ZIP descomprimidos exitosamente.")
    except Exception as e:
        arcpy.AddError("Error al descomprimir archivos ZIP: {}".format(str(e)))
else:
    print("No se seleccionó ninguna carpeta. Operación cancelada.")

# Destruir la ventana de Tkinter
root.destroy()
