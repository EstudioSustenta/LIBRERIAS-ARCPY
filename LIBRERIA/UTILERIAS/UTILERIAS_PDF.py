# -*- coding: utf-8 -*-

import sys
sys.path.append('c:/users/gustavo/appdata/local/packages/pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0/localcache/local-packages/python311/site-packages') 
import PyPDF2
import ESUSTENTA_UTILERIAS as ESU
import os

import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def join(carpeta, nombrearch, borrar=False):
    """
    Proceso para unir los mapas en un solo archivo,
    Este proceso se ejecuta en python 2.7
    """

    try:
            
        # Inicializa un objeto PdfFileWriter para contener todos los archivos PDF que se unirán
        pdf_writer = PyPDF2.PdfFileWriter()
        destino = '{}{}.pdf'.format(carpeta,nombrearch)
        pdf_readers = []

        if os.path.exists(destino):
            os.remove(destino)

        # Itera sobre cada archivo PDF en el directorio y agrégalo al objeto PdfFileWriter
        archivos = sorted(ESU.obtener_archivos_por_extension(carpeta,'pdf'))

        if len(archivos) > 0:
            for filename in archivos:
                if filename.endswith('.pdf'):
                    path = os.path.join(carpeta, filename)
                    pdf_reader = PyPDF2.PdfFileReader(open(path, 'rb'))
                    pdf_readers.append(pdf_reader)  # Agrega el
                    for page_number in range(pdf_reader.numPages):
                        page = pdf_reader.getPage(page_number)
                        pdf_writer.addPage(page)

            # Guarda el archivo PDF unido en el directorio de salida especificado
            
            with open(destino, 'wb') as out:
                pdf_writer.write(out)
            
            # Cierra los archivos pdf abiertos para que puedan eliminarse físicamente de disco
            for pdf_reader in pdf_readers:
                pdf_reader.stream.close()
            mensaje='Se han unido los archivos en "{}"'.format(destino)
            if borrar==True:
                # for pdf_reader in pdf_readers:
                #     pdf_reader.stream.close()

                contador=0
                for archivo in archivos:
                    try:
                        os.remove(archivo)
                        contador += 1
                        mensaje +='. \nSe ha borrado {} de disco'.format(archivo)
                    except Exception as e:
                        mensaje +='>>>>>ERROR en join: {}'.format(e)
        else:
            mensaje="No existen archivos pdf para unir en la carpeta {}".format(carpeta)
                
        return mensaje
    except Exception as e:
        return e

def pdf_join(carpeta, nombrearch, borrar=False):

    """
    Recopila todos los archivos 'pdf' de una carpeta y los ordena 
    alfabéticamente uniéndolos en un solo archivo.
    Si la opción 'borrar=True' está activada, elimina los archivos originales
    una vez que se ha verificado que se creó adecuadamente el archivo destino
    returns: reporte de resultado
    """
    try:

        # Lista de nombres de archivos PDF que deseas combinar
        archivos = sorted(ESU.obtener_archivos_por_extension(carpeta,'pdf'))
        # archivos = ["documento1.pdf", "documento2.pdf", "documento3.pdf"]

        # Crea un objeto PDFWriter para el archivo de salida
        pdf_writer = PyPDF2.PdfFileWriter()

        # Itera sobre cada archivo y agrega sus páginas al PDFWriter
        for archivo in archivos:
            with open(archivo, "rb") as archivo_pdf:
                pdf_reader = PyPDF2.PdfFileReader(archivo_pdf)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

        # Guarda el PDF combinado en un nuevo archivo
        destino="{}/{}.pdf".format(carpeta,nombrearch)
        with open(destino, "wb") as salida_pdf:
            pdf_writer.write(salida_pdf)
        if os.path.exists(destino):
            mensaje='El archivo se ha creado con éxito'
            if borrar==True:
                for archivo in archivos:
                    # print(archivo)
                    os.remove(archivo)
            mensaje='El archivo se ha creado con éxito y se han borrado los archivos originales'
        else:
            mensaje='No se ha creado el archivo'
        return mensaje
    except Exception as e:
        return '>>>>>ERROR en pdf_join: {}'.format(e)
