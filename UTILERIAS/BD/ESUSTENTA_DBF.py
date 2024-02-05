# -*- coding: utf-8 -*-

from dbfread import DBF
from ESUSTENTA_UTILERIAS import escribearch as escr
from dbf import Table, DbfError
import os
import shutil

fichero = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/campos_estados.txt'

def lista_campos_dbf(ruta_dbf):
    """
    funcion para listar campos de una tabla 'ruta_dbf'
    Returns; una lista que contiene los campos de la tabla
    """
        
    # Leer el archivo DBF
    tabla_dbf = DBF(ruta_dbf)

    # Obtener la lista de nombres de campos
    nombres_campos = tabla_dbf.field_names
    return nombres_campos

def escritura(fichero, estado):
    """
    Escribe el contenido de los campos de un archivo dbf mediante la librería dbfread
    y los escribe en un archivo de texto usando la librería 'escribearch' de elaboración
    propia.
    Returns: lista de datos que contiene el estado del que se extraen los datos [0]
    y una lista de los campos que conforman la tabla dbf.
    """
    escr(fichero, '/n' + lista_campos_dbf(estado)[0])
    cantcamp = len(lista_campos_dbf(estado)[1])
    escr(fichero, str(cantcamp))
    if cantcamp > 100:
        escr(fichero, 'más de 100 campos en archivo')
    else:
        for campo in lista_campos_dbf(estado)[1]:
            escr(fichero, campo)

def contar_campos_dbf(tabla):
    try:
        # Abrir la tabla DBF
        tabla_dbf = DBF(tabla)

        # Contar el número de campos
        numero_de_campos = len(tabla_dbf.field_names)

        return numero_de_campos

    except Exception as e:
        print("Error al contar campos en la tabla DBF: {}".format(e))
        return None

def verificar_existencia_campo(nombre_tabla_dbf, nombre_campo):
    try:
        # Leer la tabla DBF y obtener información sobre los campos
        with Table(filename=nombre_tabla_dbf) as tabla:
            campos_existentes = tabla.field_names

            if nombre_campo in campos_existentes:
                return True
            else:
                return False

    except Exception as e:
        return False

from dbfread import DBF

def obtener_valor_celda(nombre_tabla_dbf, campo, numero_registro):
    try:
        # Leer la tabla DBF especificando la codificación
        registros = list(DBF(nombre_tabla_dbf, encoding='latin-1'))

        # Verificar que el número de registro esté dentro de los límites
        if 0 <= numero_registro < len(registros):
            # Obtener el valor de la celda
            valor_celda = registros[numero_registro][campo]

            return valor_celda

        else:
            print("Número de registro fuera de los límites.")

    except Exception as e:
        print("Error al obtener el valor de la celda: {0}".format(e))











if __name__ == '__main__':
    import caracteres_inegi
    caracteres = caracteres_inegi.car_esp()
    # print(caracteres.encode())
    carmals = [ 
        # u'',
        u'├®',
        u'├¡',
        u'├║',
        u'├│',
        # u'',
        # u'',
        # u'',
        # u'',
        # u'',
        ]
    for car_incorr in carmals:
        ruta = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia/municipal - copia.dbf'
        car_corr = caracteres[car_incorr]
        # print (car_incorr + ">>" + car_corr)
        sustituir_caracteres_en_dbf(ruta, caracteres)
        

        # Ejemplo de uso
    nombre_tabla_dbf = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia/municipal - copia.dbf'
    campo_deseado = 'NOMGEO'
    numero_registro_deseado = 3

    valor_celda = obtener_valor_celda(nombre_tabla_dbf, campo_deseado, numero_registro_deseado)

    if valor_celda is not None:
        print("El valor en la celda '{0}' del campo '{1}' en el registro {2} es: \n{3}".format(campo_deseado, nombre_tabla_dbf, numero_registro_deseado, valor_celda).encode('utf-8'))



