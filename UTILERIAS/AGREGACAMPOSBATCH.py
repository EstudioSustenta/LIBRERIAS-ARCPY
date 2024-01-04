# -*- coding: utf-8 -*-

import arcpy
import os
import json
from itertools import islice
import codecs
import traceback
import time

global campo


def escribearch(cadena, modo, archlog):
    with codecs.open(archlog, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena = u"\n{}\t{}".format(cadena,fecha_hora_actual)
        archivo_log.write(cadena)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena)



def archjson(campo):
    # Ruta al archivo de texto
    ruta_json = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/DESCRIPTORES.json"     # este es el archivo que contiene las descripciones

    try:
        if (os.path.exists(ruta_json)):
            # Leer datos desde el archivo JSON
            with open(ruta_json, 'r', encoding='utf-8') as archivo: # , encoding='utf-8'
                datos_json = json.load(archivo)

            # Buscar el valor de "DESCRIPCION" para "CAMPO" igual a 'campo'
            valor = next(item["DESCRIPCION"] for item in datos_json if item["CAMPO"] == campo)
            return valor
    except Exception as err:
        titsus = str(err)
        return "---VERIFICAR---\n{}".format(titsus)


    # ---finaliza rutina para asignar una descripción al campo


def creacampo(archivo, camp, tipo, precision, longit, archlog):
    escribearch(u"'creacampo' iniciando..",'a',archlog)

    if os.path.exists(archivo):
        escribearch(u"El archivo \n'{}' \nexiste".format(archivo),'a',archlog)
        

    camposs = [campo.name for campo in arcpy.ListFields(archivo)]
    
    if camp in camposs:       # Verificar si el campo existe
        escribearch(u"El campo '{}' ya existe, no se creará".format(camp),'a',archlog)
        # None
    else:
        escribearch(u"El campo '{}' no existe, se creará".format(camp),'a',archlog)
        arcpy.AddField_management(in_table=archivo,
                                field_name=camp,
                                field_type=tipo,
                                field_precision=precision,
                                field_scale="",
                                # field_length=longit,
                                field_alias="",
                                field_is_nullable="NULLABLE",
                                field_is_required="NON_REQUIRED",
                                field_domain="")


def calcula():

    archlog = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/00 log resultados.txt"

    arcpy.env.overwriteOutput = True
    estados = [ # u"Aguascalientes",
                # u"Baja California",
                # u"Baja California Sur",
                # u"Campeche",
                # u"Coahuila",
                # u"Colima",
                # u"Chiapas",
                # u"Chihuahua",
                # u"Ciudad de México",
                # u"Durango",
                # u"Guanajuato",
                # u"Guerrero",
                # u"Hidalgo",
                # u"Jalisco",
                # u"México",
                # u"Michoacán de Ocampo",
                # u"Morelos",
                # u"Nayarit",
                # u"Nuevo León",
                # u"Oaxaca",
                # u"Puebla",
                # u"Querétaro",
                # u"Quintana Roo",
                # u"San Luis Potosí",
                # u"Sinaloa",
                # u"Sonora",
                # u"Tabasco",
                # u"Tamaulipas",
                # u"Tlaxcala",
                # u"Veracruz de Ignacio de la Llave",
                u"Yucatán",
                # u"Zacatecas"
                ]

    
    escribearch(u"REPORTE DE INCIDENCIAS DE PROCESO 'AGREGARCAMPOSBATCH.py'\nGUSTAVO MARTINEZ VELASCO\n\n",'w',archlog)

    try:
        escribearch(u"inicio de escritura\n\n",'a',archlog)
        
        for estado in estados:

            archtr = "manzana_localidad"
            archivo = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado,archtr)

            escribearch(u"\n\n'{}' \nIniciando proceso...".format(estado.upper()),'a',archlog)

            if os.path.exists(archivo):

                def area(archivo):
                    escribearch(u"\nProceso de área iniciando...",'a',archlog)
                    camp, tipo, precision, long = "area_has", "FLOAT", 9, ""
                    
                    creacampo(archivo, camp, tipo, precision, long, archlog)

                    expresion = "!shape.area@hectares!"
                    escribearch(u"\tProceso de actualización de campos iniciando...",'a',archlog)
                    arcpy.CalculateField_management(archivo, camp, expresion, "PYTHON")
                    escribearch(u"\texpresión '{}' agregada al archivo".format(expresion),'a',archlog)
                    escribearch(u"Proceso de área terminado",'a',archlog)

                def densidad(archivo):
                    escribearch(u"\nProceso densidad iniciando...",'a',archlog)

                    camp, tipo, precision, long = "dens_ha", "LONG", 6, ""
                    creacampo(archivo, camp, tipo, precision, long, archlog)

                    expresion = "[POB1] / [area_has]"   # expresión en vb

                    escribearch(u"\tProceso de actualización de campos iniciando...",'a',archlog)

                    arcpy.CalculateField_management(archivo, camp, expresion, expression_type="VB", code_block="")
                    escribearch(u"\t expresión '{}' agregada al archivo".format(expresion),'a',archlog)
                    escribearch(u"Proceso densidad terminado",'a',archlog)

                def pob36_a(archivo):

                    escribearch(u"\nProceso de 'POB36_a' iniciando...",'a',archlog)

                    camp, tipo, precision, long = "POB36_a", "SHORT", 6, ""
                    creacampo(archivo, camp, tipo, precision, long, archlog)

                    campos = ["POB1",
                                "POB2",
                                "POB4",
                                "POB5",
                                "POB7",
                                "POB9",
                                "POB13",
                                "POB30",
                                "POB31",
                                "POB32",
                                "POB33",
                                "POB34",
                                "POB35",
                                "POB36",
                                "POB37",
                                "POB38",
                                "POB39",
                                "POB40",
                                "POB41",
                                "POB36_a"]

                    escribearch(u"\tActualizando campos para 'POB36_a'",'a',archlog)

                    with arcpy.da.UpdateCursor(archivo, campos) as manzanas:
                        for num_manzana, manzana in enumerate(manzanas, start=0):
                        # for num_manzana, manzana in enumerate(islice(manzanas, 20), start=0): # linea limitante, util para pruebas de código
                            val = list(islice(manzana, 1, 18))

                            if all(expr >= 0 for expr in val):
                                pob36a = manzana[0] - sum(val)
                                manzana[-1] = pob36a
                                manzanas.updateRow(manzana)
                            else:
                                manzana[-1] = -6
                                manzanas.updateRow(manzana)

                    escribearch(u"\tcampos para 'POB36_a' actualizados",'a',archlog)

                    escribearch(u"Proceso de 'POB36_a' terminado",'a',archlog)

                def grupo_dom(archivo):

                    escribearch(u"\nProceso para grupo dominante iniciando...",'a',archlog)

                    camp, tipo, precision, long = "ordinal", "TEXT", "", "150"
                    creacampo(archivo, camp, tipo, precision, long, archlog)

                    camp, tipo, precision, long = "pobdom", "TEXT", "", "150"
                    creacampo(archivo, camp, tipo, precision, long, archlog)

                    escribearch(u"\tIniciando proceso de actualización de campos...",'a',archlog)
                    campos = ["POB2",
                                "POB4",
                                "POB5",
                                "POB7",
                                "POB9",
                                "POB13",
                                "POB30",
                                "POB31",
                                "POB32",
                                "POB33",
                                "POB34",
                                "POB35",
                                "POB36",
                                "POB36_a",
                                "POB37",
                                "POB38",
                                "POB39",
                                "POB40",
                                "POB41",
                                "ordinal",
                                "pobdom"]

                    with arcpy.da.UpdateCursor(archivo, campos) as manzanas:

                        # for num_manzana, manzana in enumerate(islice(manzanas, 20), start=0):
                        for manzana in manzanas:
                            val = list(manzana[:-2])
                            valmax = max(val)
                            valmaxim = [campo for campo, valor in zip(campos, val) if valor == valmax]
                            domtext = ""
                            corte = 3
                            nuevalista = []
                            if valmax <= 0:
                                valmaxim = -6
                                domtext = u"Manzana con datos confidenciales"
                            else:
                                for campmax in valmaxim:
                                    if len(campmax) < 5:
                                        descr = archjson(campmax)
                                        campmax = campmax[:corte] + "0" + campmax[corte:]
                                        domtext = (u"{} ({}: {})".format(domtext, campmax, descr))
                                    else:
                                        domtext = (u"{} ({}: {})".format(domtext, campmax, archjson(campmax)))
                                for valorcampo in valmaxim:
                                    if len(valorcampo) > 4:
                                        nuevalista.append(valorcampo)
                                    else:
                                        nuevalista.append(valorcampo[:corte] + "0" + valorcampo[corte:])

                                valmaxim = nuevalista
                                valmaxim = ' '.join(valmaxim)
                                domtext = (u"{} personas en {}".format(int(valmax), domtext))
                                domtext = domtext.replace(u"Poblacion de ", "")

                            manzana[-2] = valmaxim
                            manzana[-1] = domtext
                            manzanas.updateRow(manzana)
                    
                    escribearch(u"\tProceso de actualización de campos terminado",'a',archlog)
                    escribearch(u"Proceso para grupo dominante terminado",'a',archlog)

                def eliminar_campo_si_existe(nombre_campo,archivo):
                    escribearch(u"Proceso para eliminar campos iniciando...",'a',archlog)
                    # Comprobar si el campo existe en la capa
                    campos = [campo.name for campo in arcpy.ListFields(archivo)]
                    
                    if nombre_campo in campos:
                        # Eliminar el campo
                        arcpy.DeleteField_management(archivo, nombre_campo)
                        escribearch(u"Campo '{}' eliminado exitosamente.".format(nombre_campo),'a',archlog)
                    else:
                        escribearch(u"El campo '{}' no existe en el shapefile.".format(nombre_campo),'a',archlog)
                    
                    escribearch(u"Proceso para eliminar campos terminado...",'a',archlog)

                # Ruta del archivo shapefile

                area(archivo)
                densidad(archivo)
                pob36_a(archivo)
                grupo_dom(archivo)
                # eliminar_campo_si_existe("densid_ha",archivo)

                escribearch(u"\n{} TERMINADO\n".format(estado.upper()),'a',archlog)

            else:
                escribearch(u"\n>ERROR.\t'{}' no existe\n".format(archivo),'a',archlog)

    except Exception as err:
        escribearch(u">> ERROR DE PROCESO.\n   {}\n".format(err),'a',archlog)
        traceback.print_exc()


# Llama a la función para ejecutar el código
calcula()



    #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  + 
    # [POB2, ]	Población de 0 a 2 años
    # [POB4, ]	Población de 3 a 5 años
    # [POB5, ]	Población de 6 a 11 años
    # [POB7, ]	Población de 12 a 14 años
    # [POB9, ]	Población de 15 a 17 años
    # [POB13, ]	Población de 18 a 24 años
    # [POB30, ]	Población de 25 a 29 años
    # [POB31, ]	Población de 30 a 34 años
    # [POB32, ]	Población de 35 a 39 años
    # [POB33, ]	Población de 40 a 44 años
    # [POB34, ]	Población de 45 a 49 años
    # [POB35, ]	Población de 50 a 54 años
    # [POB36, ]	Población de 55 a 59 años
    # [POB36_a] Población de 60 a 64 años *campo agregado, no nativo de INEGI
    # [POB37, ]	Población de 65 a 69 años
    # [POB38, ]	Población de 70 a 74 años
    # [POB39, ]	Población de 75 a 79 años
    # [POB40, ]	Población de 80 a 84 años
    # [POB41, ]	Población de 85 años y más

