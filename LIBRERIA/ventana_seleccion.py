import tkinter as tk
from tkinter import ttk
import arcpy

def ini():

    # Función para mostrar la selección y cerrar la ventana
    def mostrar_seleccion():
        seleccion = entry.get()
        if seleccion:
            print(u"Selección: " + seleccion)
        ventana.destroy()


    # Archivo shapefile de entrada
    shapefile = u"Y:/0_SIG_PROCESO/ORIGEN/PROYECTOS.shp"

    # Campo 'DESCRIP'
    campo_descrip = 'DESCRIP'

    # Leer todos los valores del campo 'DESCRIP' del shapefile
    valores_descrip = [row[0] for row in arcpy.da.SearchCursor(shapefile, [campo_descrip])]
    valores_descrip = sorted(set(valores_descrip))

    # Crear una ventana principal
    ventana = tk.Tk()
    ventana.title(u"Seleccionar Valor")

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Calcular el ancho y alto de la ventana
    nuevo_ancho = 400  # Cambia este valor según tus preferencias
    nuevo_alto = 200  # Cambia este valor según tus preferencias

    # Configurar el tamaño y posición de la ventana
    x = (ancho_pantalla - nuevo_ancho) // 2
    y = (alto_pantalla - nuevo_alto) // 2
    ventana.geometry(u"{}x{}+{}+{}".format(nuevo_ancho, nuevo_alto, x, y))

    # Etiqueta con instrucciones
    etiqueta = ttk.Label(ventana, text="Selecciona un valor:")
    etiqueta.pack(padx=20, pady=10)

    # Entry para mostrar los valores y permitir la selección
    entry = ttk.Combobox(ventana, values=valores_descrip, width=50)
    entry.pack(padx=20)

    # Botón para mostrar la selección
    yboton = 50   # determina la posición en 'y' del botón
    boton_seleccionar = ttk.Button(ventana, text="Seleccionar", command=mostrar_seleccion)
    boton_seleccionar.pack(pady=yboton)

    # Iniciar el bucle principal de la ventana
    ventana.mainloop()
