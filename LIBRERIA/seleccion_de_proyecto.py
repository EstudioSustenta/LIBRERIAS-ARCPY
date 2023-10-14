# -*- coding: utf-8 -*-

#PROCESO PARA DEFINIR EL PROYECTO QUE SE PROCESARÁ PARA LA GENERACIÓN DE MAPAS Y DATOS

import tkinter as tk
import arcpy
import sys
import importlib

# Agrega la ruta del paquete al path de Python
ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SIG_PROYECTO"
sys.path.append(ruta_libreria)

# defproy = importlib.import_module("LIBRERIA.ventana_seleccion")


# Función que se ejecuta cuando se hace clic en el botón "Sí"
def iniciar_proceso():
    # Aquí puedes poner el código para iniciar tu proceso
    ventana.destroy()
    # arcpy.AddMessage("Proceso iniciado")
    print("SELECCIONAR NUEVO PROYECTO")

    importlib.import_module("LIBRERIA.ventana_seleccion")
    # reload(ventSel)
    # importlib.import_module("EJECUTABLES.generacion_sistema")

# Función que se ejecuta cuando se hace clic en el botón "No"
def no_iniciar_proceso():
    ventana.destroy()
    # arcpy.AddMessage("Proceso no iniciado")
    print("PROCESO CON EL PROYECTO PREDEFINIDO")

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("DEFINIR PROYECTO")

# Obtener las dimensiones actuales de la ventana
ventana_ancho_actual = ventana.winfo_reqwidth()
ventana_alto_actual = ventana.winfo_reqheight()

# Multiplicar las dimensiones actuales por 2 para hacer la ventana más grande
nuevo_ancho = ventana_ancho_actual * 2
nuevo_alto = ventana_alto_actual * 1

# Configurar el tamaño de la ventana
ventana.geometry("{}x{}".format(nuevo_ancho, nuevo_alto))

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana en la pantalla
x = (ancho_pantalla - nuevo_ancho) / 2
y = (alto_pantalla - nuevo_alto) / 2

# Configurar la posición de la ventana en el centro de la pantalla
ventana.geometry("+%d+%d" % (x, y))

# Etiqueta con la pregunta
pregunta_label = tk.Label(ventana, text="¿Definir nuevo proyecto?")
pregunta_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Alineada en la primera fila

# Botón "Sí" que llama a la función iniciar_proceso al hacer clic
si_boton = tk.Button(ventana, text="Nuevo proyecto", command=iniciar_proceso)
si_boton.grid(row=1, column=0, padx=10, pady=10)  # Alineado en la segunda fila, primera columna

# Botón "No" que llama a la función no_iniciar_proceso al hacer clic
no_boton = tk.Button(ventana, text="Proyecto predefinido", command=no_iniciar_proceso)
no_boton.grid(row=1, column=1, padx=10, pady=10)  # Alineado en la segunda fila, segunda columna

# Iniciar el bucle principal de la ventana
ventana.mainloop()
