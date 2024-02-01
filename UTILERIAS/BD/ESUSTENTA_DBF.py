# -*- coding: utf-8 -*-

from dbfread import DBF
from ESUSTENTA_UTILERIAS import escribearch as escr

fichero = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/campos_estados.txt'

def lista_campos_dbf(estado):
    """
    funcion para listar campos
    """
        
    # Ruta al archivo DBF
    ruta_dbf = f'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{estado}/cartografia/manzana_localidad.dbf'

    # Leer el archivo DBF
    tabla_dbf = DBF(ruta_dbf)

    # Obtener la lista de nombres de campos
    nombres_campos = tabla_dbf.field_names
    datos = [estado, nombres_campos]
    # print(f'Lista de campos: {nombres_campos}')
    return datos

def escritura(fichero, estado):
    """
    Escribe el contenido de los campos de un archivo dbf mediante la librería dbfread
    y los escribe en un archivo de texto usando la librería 'escribearch' de elaboración
    propia.
    Returns: lista de datos que contiene el estado del que se extraen los datos [0]
    y una lista de los campos que conforman la tabla dbf.
    """
    escr(fichero, '\n' + lista_campos_dbf(estado)[0])
    cantcamp = len(lista_campos_dbf(estado)[1])
    escr(fichero, str(cantcamp))
    if cantcamp > 100:
        escr(fichero, 'más de 100 campos en archivo')
    else:
        for campo in lista_campos_dbf(estado)[1]:
            escr(fichero, f'{campo}')
