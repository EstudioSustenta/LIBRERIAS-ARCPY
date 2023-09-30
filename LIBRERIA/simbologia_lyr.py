# -*- coding: utf-8 -*-

# SCRIPT PARA APLICAR SIMBOLOGÍA A UNA CAPA.
# PARTE DEL PRINCIPIO DE QUE EXISTE UNA CAPA DE SIMBOLOGÍA EN EL DIRECTORIO CORRESPONDIENTE
# CON UN ARCHIVO .lyr DEL MISMO NOMBRE QUE LA CAPA QUE SE ESTÁ CARGANDO. LA RUTA DEL ARCHIVO
# TAMBIÉN ES LA PREDEFINIDA: ("Y:\0_SIG_PROCESO\MAPAS\SIMBOLOGIA")

print("RUTINA DE ASIGNACIÓN DE SIMBOLOGÍA CARGADA EXITOSAMENTE")

def aplica_simb(capa):

    import arcpy
    arcpy.env.overwriteOutput = True
    mxd = arcpy.mapping.MapDocument('current')
    df = arcpy.mapping.ListDataFrames(mxd,'Layers')[0]
    print(capa)
    simbologia = 'Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/' + capa + '.lyr'
    lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
    lyr_capa = lyr_capa.datasetName
    arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)
    print("Simbología de capa " + capa + " aplicada.")

def aplica_simb2(capa,lyr):

    import arcpy
    arcpy.env.overwriteOutput = True
    mxd = arcpy.mapping.MapDocument('current')
    df = arcpy.mapping.ListDataFrames(mxd,'Layers')[0]
    print(capa)
    simbologia = 'Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/' + lyr + '.lyr'
    lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
    lyr_capa = lyr_capa.datasetName
    arcpy.ApplySymbologyFromLayer_management(lyr_capa,simbologia)
    print("Simbología de capa " + capa + " aplicada.")