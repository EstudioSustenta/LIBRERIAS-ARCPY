# -*- coding: utf-8 -*-

"""
Utilerias para trabajar con archivos .json
funciones:
lodicson(arch_ruta)   Recupera un diccionario de un archivo json
agdicson(archivo_json, nueva_clave, nuevo_valor)   Escribe un diccionario de un archivo json
"""
import json
import os

def lodicson(arch_ruta):
    """
    Regresa la información de un archivo json en forma de objeto
    """

    try:
        if os.path.exists(arch_ruta):
            with open(arch_ruta, "r") as archivo:
                contenido = archivo.read()
            # Convertir la cadena JSON a un diccionario
            datos = json.loads(contenido)
            return datos
        else:
            return '>>>>>ERROR: El archivo "{}" no existe'.format(arch_ruta)
    except Exception as e:
        return ">>>>>ERROR en lodicson: ".format(e)

def agdicson(archivo_json, nueva_clave, nuevo_valor):
    """
    Agrega información a un diccionario alojado en una
    estructura json.
    Si el archivo json no existe lo crea. 
    Si ya existe, agrega la clave y el valor
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(archivo_json):
            # Si el archivo no existe, crear un nuevo diccionario con la nueva clave y valor
            datos = {nueva_clave: nuevo_valor}
        else:
            # Si el archivo existe, cargar el contenido del archivo JSON en un diccionario
            with open(archivo_json, 'r') as f:
                datos = json.load(f)
            # Agregar nueva información al diccionario
            datos[nueva_clave] = nuevo_valor
        
        # Escribir el diccionario modificado de vuelta al archivo JSON
        with open(archivo_json, 'w') as f:
            json.dump(datos, f, indent=4)
        
        return '"{}" agregado en "{}" en el archivo "{}"'.format(nuevo_valor, nueva_clave, archivo_json)
    except Exception as e:
        return ">>>>>ERROR en agdicson: {}".format(e)
    """
    Regresa la información de un archivo json en forma de objeto
    """

    try:
        if os.path.exists(arch_ruta):
            with open(arch_ruta, "r") as archivo:
                contenido = archivo.read()
            # Convertir la cadena JSON a un diccionario
            datos = json.loads(contenido)
            return datos
        else:
            return '>>>>>ERROR: El archivo "{}" no existe'.format(arch_ruta)
    except Exception as e:
        return ">>>>>ERROR en lodicson: ".format(e)

def agdicson_arr(archivo_json, nueva_clave, nuevo_valor):
    """
    Agrega información a un diccionario alojado en una
    estructura json.
    Si el archivo json no existe lo crea. 
    Si ya existe, agrega la clave y el valor
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(archivo_json):
            # Si el archivo no existe, crear un nuevo diccionario con la nueva clave y valor
            datos = {nueva_clave: nuevo_valor}
        else:
            # Si el archivo existe, cargar el contenido del archivo JSON en un diccionario
            with open(archivo_json, 'r') as f:
                datos = json.load(f)
            # Agregar nueva información al diccionario
            datos.append(nuevo_valor)

        # Escribir el diccionario modificado de vuelta al archivo JSON
        with open(archivo_json, 'w') as f:
            json.dump(datos, f, indent=4)

        return '"{}" agregado en "{}" en el archivo "{}"'.format(nuevo_valor, nueva_clave, archivo_json)
    except Exception as e:
        return ">>>>>ERROR en agdicson: {}".format(e)


if __name__ == '__main__':
    arch = "D:/archivito2.json"
    for i in range(1,501):
        agdicson(arch, "campo" + str(i),"valor" + str(i))



