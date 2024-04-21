# -*- coding: utf-8 -*-


# Rutina para proyectar a 'WGS84z13' cualquier archivo .shp que contenga la cadena 'cadena'
# que se encuentre en al carpeta o subcarpetas seleccionadas mediante la ventana
# Puede (si se activa la función) borrar el archivo fuente una vez convertido a la nueva proyección

import os
import arcpy
from Tkinter import Tk  # Import the Tk class
import tkFileDialog  # En Python 2.7, se utiliza tkFileDialog en lugar de filedialog
import sys
import importlib
# import AJUSTE_DENUE as ajuste_denue



# ruta_libreria = u"C:/SCINCE 2020"
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

# ajuste_denue = importlib.import_module(u"UTILERIAS.AJUSTE_DENUE")


arcpy.env.overwriteOutput = True

def obtener_codigo_epsg(archivo_shp):
    describe = arcpy.Describe(archivo_shp)
    try:
        codigo_epsg = int(describe.spatialReference.factoryCode)
        return codigo_epsg
    except AttributeError:
        print(u"El archivo shapefile no tiene una proyección definida.")
        return None

def proyectar_shapefile(archivo_entrada, archivo_salida, proyeccion_destino):
    # Definir la proyección de destino
    proyeccion_destino = arcpy.SpatialReference(proyeccion_destino)

    # Proyectar el shapefile
    arcpy.Project_management(archivo_entrada, archivo_salida, proyeccion_destino)

def borrar_archivo_si_existe(arch_verif,arch_borr):
    if os.path.exists(arch_verif):
        try:
            arcpy.Delete_management(arch_borr)
            print ('{} existe, \n{} borrado exitosamente.'.format(arch_verif,arch_borr))
        except Exception as e:
            print (e)
    else:
        print ('no existe, \nno se ha borrado.')

def buscar_archivos_shp(carpeta_seleccionada):

    # Ruta de la carpeta principal
    # carpeta_seleccionada = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023"
    # cadena = "denue_inegi_"
    cadena = "manzana"
    extension = ".shp"
    archsal = "manzana_localidad"
    print("Se seleccionó la carpeta '{}'".format(carpeta_seleccionada.encode('utf-8')))
    print("Se proyectarán los archivos '{}' que contienen la cadena '{}'\n".format(extension, cadena))
    
    for ruta_actual, carpetas, archivos in os.walk(carpeta_seleccionada):
        for archivo in archivos:
            # if archivo.endswith(cadena):
            # print (archivo)
            if archivo.endswith(extension) and archivo.startswith(cadena):
                print ("\t{}".format(archivo))
                archivo_entrada = (os.path.join(ruta_actual, archivo))
                archivo_entrada = archivo_entrada.replace("\\","/")
                entrada = (os.path.splitext(os.path.basename(archivo_entrada))[0])
                print ("\nArchivo de entrada: '{}'".format(archivo_entrada.encode('utf-8')))

                # archivo_salida = os.path.join(ruta_actual, "wgs84z13 {}".format(archivo))
                archivo_salida = (os.path.join(ruta_actual, "{}.shp".format(archsal)))
                archivo_salida = archivo_salida.replace("\\","/")
                print ("Archivo de salida: '{}'".format(archivo_salida.encode('utf-8')))

                # Obtén el nombre del archivo sin la extensión
                salida = (os.path.splitext(os.path.basename(archivo_salida))[0])

                codigo = obtener_codigo_epsg(archivo_entrada)
                print ("el código epsg de '{} es '{}''".format(archivo.encode('utf-8'), codigo))

                if os.path.exists(archivo_salida):
                    print ("el archivo '{}' ya existe en '{}'".format(archivo.encode('utf-8'), os.path.dirname(archivo_salida.encode('utf-8'))))
                else:
                    print ("el archivo '{}' NO existe en '{}'".format(archivo.encode('utf-8'), os.path.dirname(archivo_salida.encode('utf-8'))))
                    print (codigo)
                    if codigo != 32613: # and codigo == None:
                        print ("'{}' a proyectar como '{}' en {}".format(entrada.encode('utf-8'),salida.encode('utf-8'),(ruta_actual.encode('utf-8'))))

                        # rutina para proyectar el archivo
                        proyeccion_destino = 32613      # Código EPSG para WGS_1984_UTM_Zone_13N
                        proyectar_shapefile(archivo_entrada, archivo_salida, proyeccion_destino)                # Llamar a la función para proyectar el shapefile

                        # # rutina para borrar el archivo original si se proyectó correctamente el archivo
                        # borrar_archivo_si_existe(archivo_salida,archivo_entrada)                                # Llamar a la función para borrar el shapefile

                        # # hace el ajuste de claves en archivo mediante librería externa
                        # reload (ajuste_denue)
                        # ajuste_denue.comp_denue(archivo_salida)                                                 # Llamar a la función externa de ajuste

                    else:
                        print("\n'{}' no se puede proyectar '{}'\n\n".format(entrada,codigo))



if __name__ == '__main__':
    # Crear una ventana de selección de carpeta utilizando Tkinter
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Mostrar el cuadro de diálogo para seleccionar una carpeta
    carpeta_inicial = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/conjunto_de_datos'
    carpeta_inicial = 'Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023'
    carpeta_seleccionada = tkFileDialog.askdirectory(initialdir=carpeta_inicial, title="Seleccionar Carpeta con Archivos '.shp' a proyectar")
    # print(carpeta_seleccionada)
    buscar_archivos_shp(carpeta_seleccionada)

