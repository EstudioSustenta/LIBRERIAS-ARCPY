# -*- coding: utf-8 -*-

# rutina para ajustar la escala de un mapa a para que se visualicen un número (ordinal) determinado de elementos de una lista de objetos a una distancia
# determinada almacenados en un archivo (archivo), extrayendo el valor de la columna (columna), entendiendo que el valor debe
# ser numérico y que representa la distancia en metros a la que se aplicará el ajuste de escala.

import arcpy

# ordinal = 4
# columna = 3
# archivo = "Y:/02 CLIENTES (EEX-CLI)/(2001-0001) FAMILIA MARTINEZ DEL RIO/(2008-PIN-0005) CASA BUENAVISTA/SIG/Subestacion electrica near.txt"

def extraedato(archivo, ordinal, columna):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    ordinal = str(ordinal) + "\t"

    # Abrir el archivo para lectura
    with open(archivo, 'r') as file:
        # Iterar a través de cada línea en el archivo
        for line in file:
            # Verificar si la línea comienza con '4'
            if line.startswith((ordinal)):
                # Dividir la línea en columnas utilizando tabuladores como separadores
                columns = line.split('\t')
                
                # Verificar si hay al menos tres columnas
                if len(columns) >= columna:
                    # Extraer el valor de la tercera columna (índice 2)
                    print ("Ordinal = " + str(ordinal))
                    print("Columna = " + str(columna))
                    distancia = int(columns[2].strip())  # strip() elimina espacios en blanco adicionales y saltos de línea
                    print("distancia = " + str(distancia))

    escala = (distancia * 2) / 20 * 100
    print ("escala = " + str(escala))
    df.scale = escala
    arcpy.RefreshActiveView()