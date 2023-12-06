# -*- coding: utf-8 -*-

# ESTA RUTINA ELIMINA FÍSICAMENTE UN ARCHIVO O GRUPO DE ARCHIVOS CON NOMBRE IGUAL AL DEFINIDO MEDIANTE LA SELECCIÓN POR VENTANA
# DE UNA CARPETA (DEFINIDA TAMBIÉN MEDIANTE VENTANA) Y SUS SUBCARPETAS
# DA UN TRATAMIENTO DISTINTO DE ACUERDO A LA TERMINACIÓN DEL ARCHIVO:
# LOS ARCHIVOS .SHP (Y TODOS LOS ASOCIADOS) SE ELIMINAN MEDIANTE LA LIBRERÍA 'ARCPY' MIENTRAS QUE EL RESTO SE ELIMINAN USANDO LA FUNCIÓN 'OS.REMOVE'
# ESTE SCRIPT TIENE COMO VENTAJA AL BORRADO MEDIANTE COMANDO QUE ELIMINA LOS ARCHIVOS .SHP Y ASOCIADOS DE SUBCARPETAS DE UN SOLO PASO.

import arcpy
import os
import Tkinter, tkFileDialog

carpeta_inicio = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023"



def borrar_archivo_si_existe(archivo_borrar):
    if os.path.exists(archivo_borrar):
        
        nombarch = os.path.basename(archivo_sim)
        extarch = os.path.splitext(nombarch)[1]
        # print (extarch.encode('utf-8'))
        try:
            
            if extarch == ".shp" or extarch == ".SHP":
                arcpy.Delete_management(archivo_borrar)
                if os.path.exists(archivo_borrar):
                    print (u'>> ERROR, Archivo shapefile. \n{} NO se ha borrado.'.format(archivo_borrar))
                else:
                    print (u'Archivo shapefile. \n{} borrado exitosamente.'.format(archivo_borrar))
            else:
                os.remove(archivo_borrar)
                print (u'Archivo genérico. \n{} borrado exitosamente.'.format(archivo_borrar))
        except Exception as e:
            print (e)
    else:
        print ('no existe, \nno se ha borrado.')



def inicio():
    # Crear una instancia de Tkinter y ocultar la ventana principal
    root = Tkinter.Tk()
    root.withdraw()
    

    def archsim():

        global archivo_sim
        # define mediante una ventana el nombre de archivo similar que se borrará.
        archivo_sim = tkFileDialog.askopenfilename(parent=root, 
                                                    initialdir=carpeta_inicio, 
                                                    title="Selecciona un archivo con nombre igual a los que deseas eliminar de disco.", 
                                                    )   #  filetypes=[('Shapefile', '*.shp')]
        archivo_sim = os.path.basename(archivo_sim)
        archivo_sim = archivo_sim.replace("\\","/")
        print("\n\n\n\n")
        print (archivo_sim.encode('utf-8'))
    
    def carpetasel():

        

        # Mostrar un cuadro de diálogo para seleccionar la carpeta
        directorio = tkFileDialog.askdirectory(parent=root, initialdir=carpeta_inicio, title='Por favor selecciona un directorio de bísqueda para borrado')

        # Para cada directorio, subdirectorio y archivo en el directorio seleccionado
        for dirpath, dirnames, archivos in os.walk(directorio):
            # Para cada archivo en el directorio actual
            for nombre_archivo in archivos:
                # Si el archivo es un .shp
                if nombre_archivo.endswith(archivo_sim):
                    # Imprimir la ruta completa del archivo .shp
                    shapefile = (os.path.join(dirpath, nombre_archivo))
                    print("\n\n")
                    print (shapefile).encode('utf-8')
                    borrar_archivo_si_existe(shapefile)

    archsim()           # Seleccionar el nombre de archivo que se eliminará (no necesariamente se borrará ese archivo, solo los que están en la ruta de búsqueda). 
    carpetasel()        # Seleccionar la carpeta a buscar (inclusive)
