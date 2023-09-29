# -*- coding: utf-8 -*-

# ESTE SCRIPT TOMA UNA CAPA DE POLÍGONOS INCOMPLETOS DEL PAIS Y HACE UN MERGE CON LA CAPA DEL PAIS PARA TENER
# ÁREAS LLENAS EN TODO EL TERRITORIO NACIONAL

# base:         capa de entrada (incluye ruta y nombre de capa)
# salida:       capa de salida (incluye ruta y nombre de capa)
# campo:        nombre del campo a crear
# valor:        valor del campo para las áreas vacías de la capa merge




# ejemplo de valores:
# base = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI/Cuerpos de agua.shp"
# salida = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI/RENOMBRAME BIEN.shp"
# valor = '"fuera de cuerpo de agua"'
# campo = "NOMBRE"

import arcpy

def paislleno(base, salida, campo, valor):

    arcpy.env.overwriteOutput = True

    mexico = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI/MEXICO GENERAL.shp"
    # Obtiene la definición de campos (atributos) de la capa
    campos = arcpy.ListFields(base)
    camposmx = arcpy.ListFields(mexico)
    verif = "no existe"

    # Itera a través de los campos y muestra el nombre, tipo y longitud
    for campoexist in campos:
        if campoexist.name == campo:
            nombre_campo = campoexist.name
            tipo_campo = campoexist.type
            long = str(campoexist.length)
            if long < 20:
                long = 50
            # COMPRUEBA SI EXISTE EL CAMPO PREVIAMENTE EN LA CAPA
            for campomx in camposmx:
                if campomx.name == campo:
                    verif = "ya existe"
            if verif != "ya existe":
                print ("\n creando campo " + campo)
                # OBTIENE LOS VALORES DE CAMPO Y AGREGA EL CAMPO A LA CAPA DEL PAIS
                arcpy.AddField_management(in_table=mexico, 
                    field_name=campo,
                    field_type="TEXT",
                    field_precision="",
                    field_scale="",
                    field_length=str(long),
                    field_alias="",
                    field_is_nullable="NULLABLE",
                    field_is_required="NON_REQUIRED",
                    field_domain="")
            else:
                print("\n El campo " + campo + " ya existe en la tabla \n")
    # AGREGA EL VALOR AL CAMPO DEL PAIS
    print ("\n calculando campo " + campo + " con el valor " + valor)
    arcpy.CalculateField_management(in_table=mexico,
        field=campo,
        expression=valor,
        expression_type="VB",
        code_block="")
    # RESTA LA CAPA A INTEGRAR EN LA CAPA DEL PAIS
    salidatmp = "Y:/0_SIG_PROCESO/X TEMPORAL/proceso merge.shp"
    arcpy.Erase_analysis(in_features=mexico, 
        erase_features=base, 
        out_feature_class=salidatmp, 
        cluster_tolerance="")
    # EJECUTA EL MERGE DE LAS DOS CAPAS
    inp = "\"'" + base + "';'" + salidatmp + "'\""
    arcpy.Merge_management(inputs=inp, 
        output=salida, 
        field_mappings="")
    # ELIMINA EL CAMPO CREADO EN AL MAPA DE RECORTE (PAIS MEXICO)
    arcpy.DeleteField_management(in_table=mexico, drop_field=campo)


