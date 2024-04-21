# -*- coding: utf-8 -*-

"""
Función para realizar un clip del mapa de la república mexicana
usando un query para cada una de las entidades federativas y realizando
el clipo de cada entidad con una capa con geometría a nivel pais
\n recorte: capa de entidades federativas (plantilla para el clip)
\n capaclip: Capa de la cual se hará el recorte
\n campo: el campo que servirá para formar los querys de filtrado de geometría para recorte
y clip
\n prefijo: prefijo para formar el nombre del archivo shapefile
\n returns: resultado de la operación
\n\nNota: el script dio problemas con estados con acentos y con veracruz
"""

import arcpy
import os

# Ruta al shapefile
recorte = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS/ESTATAL decr185.shp"
# capaclip = "Y:/GIS/MEXICO/VARIOS/INEGI/RED NACIONAL DE CAMINOS 2017/conjunto_de_datos/red_vial_wgs84utm_DISS_02.shp"
capaclip = "Y:/GIS/MEXICO/VARIOS/www.numeroslocos.com/COLONIAS.shp"


# Lista para almacenar los valores del campo 'NOM_ENT'
estados = []

# Iterar sobre los valores del campo 'NOM_ENT'
campo="ENTIDAD"
prefijo="Colonias_"
with arcpy.da.SearchCursor(recorte, campo) as cursor:
    for row in cursor:
        estados.append(row[0])

# Imprimir la lista de valores
# print(estados)

mxd=arcpy.mapping.MapDocument('CURRENT')
df=arcpy.mapping.ListDataFrames(mxd)[0]

# carga la capa de los estados
capa=arcpy.mapping.Layer(recorte)
arcpy.mapping.AddLayer(df, capa)
# Carga la capa de la red vial
caparv=arcpy.mapping.Layer(capaclip)
arcpy.mapping.AddLayer(df, caparv)

a_cortar=os.path.basename(capaclip).split(".")[0]
capa_recorte=os.path.basename(recorte).split(".")[0]

for estado in estados:
    try:
        ruta_destino="{}/{}/".format(os.path.dirname(capaclip),estado)
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
        expr= """("{}" = '{}')""".format(campo, estado)
        arch_destino="{}{}{}.shp".format(ruta_destino,prefijo,estado)
        capa = arcpy.mapping.ListLayers(mxd, capa_recorte)[0]
        capa.definitionQuery = expr
        arcpy.RefreshActiveView()
        arcpy.Clip_analysis(a_cortar,capa_recorte,arch_destino,cluster_tolerance="")
        if os.path.exists(arch_destino):
            print(u"Se ha creado el archivo '{}' con éxito".format(estado))
        else:
            print("Error creando el archivo {}".format(arch_destino))
    except Exception as e:
        print(">>>>>ERROR: {}".format(e))
capa.definitionQuery = None
arcpy.RefreshActiveView()

