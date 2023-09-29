# -*- coding: utf-8 -*-


def quitaregistros(capa, campoord)
# Ruta al shapefile o capa de interés
capa = "Cuerpoaguaintermitente"

# Nombre del campo 'distancia'
campoord = "NEAR_DIST"

# Crear una lista vacía para almacenar los valores de distancia
cercanos = []

# Utilizar SearchCursor para obtener los valores de 'distancia'
with arcpy.da.SearchCursor(capa, [campoord]) as cursor:
    for row in cursor:
        distancia = row[0]
        cercanos.append(distancia)

# Ordenar la lista de mayor a menor
cercanos.sort(reverse=False)

# Ahora, la lista 'cercanos' contiene los valores ordenados de mayor a menor
for i in range(10):
    print(cercanos[i])