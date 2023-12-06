import os
import Tkinter as tk
import tkFileDialog
import zipfile

def seleccionar_carpeta():
    carpeta_seleccionada = tkFileDialog.askdirectory()
    if carpeta_seleccionada:
        descomprimir_archivos_zip(carpeta_seleccionada)

def descomprimir_archivos_zip(carpeta):
    for archivo_zip in obtener_archivos_zip(carpeta):
        try:
            nombre_subcarpeta = os.path.splitext(archivo_zip)[0]
            ruta_subcarpeta = os.path.join(carpeta, nombre_subcarpeta)

            with zipfile.ZipFile(os.path.join(carpeta, archivo_zip), 'r') as zip_ref:
                zip_ref.extractall(ruta_subcarpeta)

            print("Descomprimido '{}' en '{}'".format(archivo_zip, nombre_subcarpeta))
        except Exception as e:
            print("Error al descomprimir '{}': {}".format(archivo_zip, str(e)))

def obtener_archivos_zip(carpeta):
    archivos_zip = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.zip')]
    return archivos_zip

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Descomprimir Archivos ZIP")

# Botón para seleccionar carpeta
btn_seleccionar_carpeta = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
btn_seleccionar_carpeta.pack(pady=10)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
