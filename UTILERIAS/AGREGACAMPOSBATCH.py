# -*- coding: utf-8 -*-


import arcpy
import os
import json
from itertools import islice
import codecs

global archlog
global campo
archlog = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/00 log resultados.txt"

def escribearch(cadena,modo):
    with codecs.open(archlog,modo, encoding = 'utf-8') as archivo_log:
        archivo_log.write(cadena)
        archivo_log.close

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


def creacampo(archivo, camp, tipo, precision, longit):
    # print ("'creacampo()' iniciando...")
    escribearch("'creacampo' iniciando..",'a')

    if os.path.exists(archivo):
        # print (archivo)
        escribearch("El archivo \n'{}' \nexiste\n".format(archivo),'a')
        

    camposs = [campo.name for campo in arcpy.ListFields(archivo)]
    
    if camp in camposs:       # Verificar si el campo existe
        # print("El campo '{}' existe en el shapefile.".format(camp))
        escribearch("El campo '{}' ya existe, no se creara".format(camp),'a')
        # None
    else:
        # print("El campo '{}' no existe en el shapefile, creando el campo.".format(camp))
        escribearch("El campo '{}' no existe, no se creara".format(camp),'a')
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
        # print("El campo {} ha sido creado en el shapefile.".format(camp))
        

    # print ("'creacampo()' finalizado.")


def calcula():

    arcpy.env.overwriteOutput = True
    estados = [ # "Aguascalientes",
                # "Baja California",
                # "Baja California Sur",
                # "Campeche",
                # "Coahuila",
                "Colima",
                # "Chiapas",
                # "Chihuahua",
                # "Ciudad de México",
                # "Durango",
                # "Guanajuato",
                # "Guerrero",
                # "Hidalgo",
                # "Jalisco",
                # "México",
                # "Michoacán de Ocampo",
                # "Morelos",
                # "Nayarit",
                # "Nuevo León",
                # "Oaxaca",
                # "Puebla",
                # "Querétaro",
                # "Quintana Roo",
                # "San Luis Potosí",
                # "Sinaloa",
                # "Sonora",
                # "Tabasco",
                # "Tamaulipas",
                # "Tlaxcala",
                # "Veracruz de Ignacio de la Llave",
                # "Yucatán",
                # "Zacatecas"
                ]

    
    escribearch("REPORTE DE INCIDENCIAS DE PROCESO 'AGREGARCAMPOSBATCH.py'\nGUSTAVO MARTINEZ VELASCO\n\n",'w')

    try:
        escribearch("inicio de escritura",'a')
        
        for estado in estados:

            global archivo
            archtr = "manzana_localidad"
            archivo = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado,archtr)

            print (estado)
            print (u"\nEjecutando proceso, espere...\n\n")

            escribearch("\n'{}' INICIANDO PROCESO PARA...".format(estado),'a')

            if os.path.exists(archivo):

                # campo_a = ""
                # campo36a = "POB36_a"

                def area():
                    print (u"Calculando campo de área")
                    camp, tipo, precision, long = "area_has", "FLOAT", 9, ""
                    escribearch("\n\t'{}' agregando...".format(camp),'a')
                    creacampo(archivo, camp, tipo, precision, long)

                    escribearch("\n\t'{}' agregado".format(camp),'a')

                    expresion = "!shape.area@hectares!"
                    arcpy.CalculateField_management(archivo, camp, expresion, "PYTHON")
                    escribearch("\n\t expresion '{}' agregada al archivo".format(expresion),'a')
                    print (u"Finalizado proceso para campo de área")

                def densidad():

                    print (u"Calculando campo de densidad")

                    camp, tipo, precision, long = "dens_ha", "LONG", 6, ""
                    creacampo(archivo, camp, tipo, precision, long)

                    expresion = "[POB1] / [area_has]"   # expresión en vb

                    arcpy.CalculateField_management(archivo, camp, expresion, expression_type="VB", code_block="")
                    escribearch("\n\t expresion '{}' agregada al archivo".format(expresion),'a')
                    print (u"Finalizado proceso para campo de densidad")

                def pob36_a():

                    print (u"Calculando campo de POB36_a")

                    camp, tipo, precision, long = "POB36_a", "SHORT", 6, ""
                    creacampo(archivo, camp, tipo, precision, long)

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

                    print (u"Finalizado proceso para campo de POB36_a")

                def grupo_dom():

                    print (u"Calculando campo de grupo dominante")

                    camp, tipo, precision, long = "ordinal", "TEXT", "", "150"
                    creacampo(archivo, camp, tipo, precision, long)

                    camp, tipo, precision, long = "pobdom", "TEXT", "", "150"
                    creacampo(archivo, camp, tipo, precision, long)

                    escribearch("\n\tIniciando proceso para grupo dominante",'a')
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
                                domtext = domtext.replace(u"Población de ", "")

                            manzana[-2] = valmaxim
                            manzana[-1] = domtext
                            manzanas.updateRow(manzana)


                    print (u"Finalizado proceso para campo de grupo dominante")


                def eliminar_campo_si_existe(nombre_campo):
                    # Comprobar si el campo existe en la capa
                    campos = [campo.name for campo in arcpy.ListFields(archivo)]
                    
                    if nombre_campo in campos:
                        # Eliminar el campo
                        arcpy.DeleteField_management(archivo, nombre_campo)
                        print("Campo '{}' eliminado exitosamente.".format(nombre_campo))
                    else:
                        print("El campo '{}' no existe en el shapefile.".format(nombre_campo))

                # Ruta del archivo shapefile

                area()
                densidad()
                pob36_a()
                grupo_dom()
                # eliminar_campo_si_existe("densid_ha")

                print (u"\n'{}' TERMINADO\n".format(estado))
                escribearch("\n{} TERMINADO\n".format(estado),'a')

            else:
                print(u"El archivo \n{} \nno existe\n\n".format(estado))
                escribearch("\n>ERROR.\t'{}' no existe\n".format(archivo),'a')

    except Exception as err:
        escribearch(">> ERROR DE PROCESO.\n   {}\n".format(err),'a')
        print (err)

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

