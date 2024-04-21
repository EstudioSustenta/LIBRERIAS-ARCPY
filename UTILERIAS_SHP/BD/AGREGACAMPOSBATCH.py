# -*- coding: utf-8 -*-

import arcpy
import os
import json
from itertools import islice
import codecs
import traceback
import time
from dbfread import DBF
import pandas as pd


def escribearch(cadena, modo, archlog):
    # -*- coding: utf-8 -*-
    with codecs.open(archlog, modo, encoding='utf-8') as archivo_log:
        timestamp = time.time()     # Obtiene la fecha y hora actual en segundos desde la época (timestamp)
        estructura_tiempo_local = time.localtime(timestamp)     # Convierte el timestamp a una estructura de tiempo local
        fecha_hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", estructura_tiempo_local)     # Formatea la estructura de tiempo local como una cadena legible

        cadena1 = u"\n{}\t{}".format(cadena,fecha_hora_actual)
        archivo_log.write(cadena1)
        archivo_log.close()  # Corregir llamada a close()
        print(cadena1.encode('utf-8'))

# REGRESA EL VALOR DE CAMPO
def archjson(campo):
    # Ruta al archivo de texto
    ruta_json = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/DESCRIPTORES.json"     # este es el archivo que contiene las descripciones

    try:
        # escribearch(u"'archjson' iniciando... '{}'".format(campo),'a',archlog)  ---->>   NO ACTIVAR ESTA LÍNEA, HACE MUY LENTO EL CÓDIGO Y GENERA UN ARCHIVO LOG MUY GRANDE
        if (not os.path.exists(ruta_json)):
            raise Exception(u"EL ARCHIVO {} NO EXISTE.".format(ruta_json))

        # Leer datos desde el archivo JSON
        with open(ruta_json, 'r') as archivo: # , encoding='utf-8'
            datos_json = json.load(archivo)
        
        # escribearch(u"'archjson' terminado con éxito '{}'".format(campo),'a',archlog)  ---->>   NO ACTIVAR ESTA LÍNEA, HACE MUY LENTO EL CÓDIGO Y GENERA UN ARCHIVO LOG MUY GRANDE
        return datos_json[campo]

    except Exception as err:
        titsus = str(err)
        print(titsus)
        escribearch(u"ERROR RECUPERANDO VALOR DE '{}'".format(campo),'a',archlog)
        return u"---VERIFICAR---\n{}".format(titsus)


    # ---finaliza rutina para asignar una descripción al campo

def creacampo(valores):    

    archivo = valores['archivo1']
    camp = valores['campo']
    tipo = valores['tipo']
    precision = valores['precision']
    longit = valores['long']
    archlog = valores['archlog']

    escribearch(u"'creacampo' iniciando...",'a',archlog)

    if os.path.exists(archivo):
        escribearch(u"El archivo \n'{}' \nexiste".format(archivo),'a',archlog)

        camposs = [campo.name for campo in arcpy.ListFields(archivo)]

        print(">>>>>>>>>>>>")
        print(camposs)

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
            escribearch(u"El campo '{}' se ha creado en {}".format(camp,archivo),'a',archlog)
    else:
        escribearch(u"El archivo: \n'{}' \n no existe".format(archivo),'a',archlog)
        # raise ValueError("Este es un mensaje de error.")
        
def calculacampo(valores):

    archlog = valores['archlog']
    archivo1 = valores['archivo1']
    campo = valores['campo']
    expresion = valores['expresion']
    tipoexp = valores['tipoexp']
    bloquecodigo = valores['bloquecodigo']  # esta variable está pendiente de usar

    escribearch(u"\nProceso de cálculo de campo iniciando...",'a', archlog)
    escribearch(u"\nvalores: archivo:{}, campo: {}, expresion:{}, tipo: {}, bloque: {}".format(archivo1,campo,expresion,tipoexp,bloquecodigo),'a', archlog)

    # arcpy.CalculateField_management(archivo, camp, expresion, "PYTHON")

    arcpy.CalculateField_management(in_table=archivo1,
                                field=campo,
                                expression=expresion,
                                expression_type=tipoexp
                                )

    escribearch(u"\nProceso de cálculo de campo terminado",'a', archlog)

def eliminar_archivo(archivoselim, archlog):
    escribearch(u"\nProceso eliminación de archivos iniciando...",'a',archlog)
    escribearch(u"\nArchivos a eliminar:\n{}".format(archivoselim),'a',archlog)
    try:
        for archivo in archivoselim:
                if os.path.exists(archivo):
                    os.remove(archivo)
                    escribearch(u"\nArchivo eliminado:\n{}".format(archivo),'a',archlog)
                else:
                    escribearch(u"\n{}\nno existe.".format(archivo),'a',archlog)
    except OSError as e:
        # print("Error al eliminar el archivo: {e}".format(archivo))
        escribearch(u"\nError al eliminar el archivo:\n{}\n{}".format(archivo,e),'a',archlog)

def calc_camp_compl(valores):
    archivo = valores['archivo1'.encode('latin-1')]
    print("ARCHIVO >>> " + valores['archivo1'])
    table = DBF(archivo, encoding='latin-1')
    df = pd.DataFrame(iter(table))
    print(df[1:7])

def calc_area_dens(estados):

    """
    Crea y calcula el campo de área de las manzanas
    Crea y calcula el campo de densidad de las manzanas
    Crea y calcula el campo de POB36_a de las manzanas (no necesario)
    Crea y calcula el campo de el grupo dominante de las manzanas
    
    """

    global archlog
    archlog = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/00 log resultados.txt"

    arcpy.env.overwriteOutput = True

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
                    # camp, tipo, precision, long = "area_has", "FLOAT", 9, ""
                    expresion = "!shape.area@hectares!"
                    
                    valores = {'archlog' : archlog,
                               'archivo1' : archivo,
                               'campo' : "area_has",
                               'tipo' : 'FLOAT',
                               'precision' : 3,
                               'long' : "",
                               'expresion' : expresion,
                               'tipoexp' : "PYTHON",
                               'bloquecodigo' : ""
                               }

                    creacampo(valores)

                    escribearch(u"\tProceso de actualización de campos iniciando...",'a',archlog)
                    calculacampo(valores)   # ejecuta la función para calcular el campo
                    # arcpy.CalculateField_management(archivo, camp, expresion, "PYTHON")
                    escribearch(u"\texpresión '{}' agregada al archivo".format(expresion),'a',archlog)
                    escribearch(u"Proceso de área terminado",'a',archlog)

                def densidad(archivo):
                    escribearch(u"\nProceso densidad iniciando...",'a',archlog)

                    # camp, tipo, precision, long = "dens_ha", "LONG", 6, ""
                    expresion = "[POB1] / [area_has]"   # expresión en vb
                    
                    valores = {'archlog' : archlog,
                               'archivo1' : archivo,
                               'campo' : "dens_ha",
                               'tipo' : 'FLOAT',
                               'precision' : 3,
                               'long' : "",
                               'expresion' : expresion,
                               'tipoexp' : "VB",
                               'bloquecodigo' : ""
                               }
                    
                    creacampo(valores)
                    # arcpy.CalculateField_management(archivo, camp, expresion, expression_type="VB", code_block="")
                    calculacampo(valores)   # ejecuta la función para calcular el campo

                    escribearch(u"Proceso densidad terminado",'a',archlog)

                def pob36_a(archivo):

                    escribearch(u"\nProceso de 'POB36_a' iniciando...",'a',archlog)

                    # camp, tipo, precision, long = "POB36_a", "SHORT", 6, ""

                    valores = {'archlog' : archlog,
                               'archivo1' : archivo,
                               'campo' : "POB36_a",
                               'tipo' : 'SHORT',
                               'precision' : 6,
                               'long' : ""
                               }
                    
                    creacampo(valores)

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

                    valores = {'archlog' : archlog,
                               'archivo1' : archivo,
                               'campo' : "ordinal",
                               'tipo' : 'TEXT',
                               'precision' : "",
                               'long' : 150
                               }
                    
                    creacampo(valores)

                    valores['campo'] = 'pobdom'

                    creacampo(valores)

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
                                "POB16",
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
                    
                dicc = {'archlog' : archlog, 'estado' : estado}

                area(archivo)   #calcula el área de las manzanas
                densidad(archivo)   # calcula la densidad de habitantes por manzana
                # pob36_a(archivo)  # Calcula el campo POB36_a (Esta función se había creado porque aparentemente no existía el rango de población de 60-64 años, pero sí existe, es el campo POB16)
                grupo_dom(archivo)
                
                # eliminar_campo_si_existe("densid_ha",archivo)     #función para borrar el campo de desnsidad

                escribearch(u"\n{} TERMINADO\n".format(estado.upper()),'a',archlog)

            else:
                escribearch(u"\n>ERROR.\t'{}' no existe\n".format(archivo),'a',archlog)

    except Exception as err:
        escribearch(u">> ERROR DE PROCESO.\n   {}\n".format(str(traceback.print_exc())),'a',archlog)
        # print (err)
        # traceback.print_exc()

def tablapob(estados):
    for estado in estados:

        print(u"\n\n\n{}".format(estado.upper()))

        archivo = 'manzana_localidad'
        nuevo_nombre = 'cpv2020_{}_poblacion.dbf'.format(archivo)
        origen = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/{}.shp".format(estado, archivo)
        dirdest = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/".format(estado)
        destino = u'{}{}.dbf'.format(dirdest, archivo)

        # Verifica si el archivo de origen existe
        if not os.path.exists(origen):
            print(u"01 El archivo\n{}\nno existe, se detendrá el proceso".format(origen))
        else:
            print(u"01 El archivo\n{}\nexiste, el proceso continúa".format(origen))

            # Verifica si el archivo de destino ya existe
            if os.path.exists(destino):
                print(u"02 El archivo\n{}\nya existe, no se creará".format(destino))
            else:
                # Crea el archivo .dbf a partir del shapefile
                print(u"02 El archivo\n{}\nno existe, se creará".format(destino))
                arcpy.TableToDBASE_conversion(Input_Table="'"+origen+"'", Output_Folder=dirdest)
                print(u"03 El archivo dbf se ha creado satisfactoriamente")

            # Verifica nuevamente si el archivo de destino existe después de la conversión
            if os.path.exists(destino) and not os.path.exists(dirdest+nuevo_nombre):
                # Renombra el archivo .dbf
                print(u"04 El archivo\n{}\nno existe, se renombrará".format(dirdest+nuevo_nombre))
                os.rename(destino, dirdest+nuevo_nombre)
                print(u"05 Proceso completado satisfactoriamente para \n{}{}".format(dirdest, nuevo_nombre))
            else:
                print(u"04 El archivo\n{}\nno existe, no se puede renombrar".format(destino))

def rangos_de_edad(estados):
    print(u"\n\nIniciando")

    archlog = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/00 log rangos_de_edad.txt"
    archtr1 = u"cpv2020_manzana_localidad_poblacion"

    escribearch('\n\nARCHIVO DE REPORTE DE INCIDENCIAS', 'w', archlog)
    escribearch('\n\n', 'a', archlog)
    for estado in estados:
        
        escribearch(u"\nIniciando {}".format(estado),'a',archlog)
        archivo1 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/{}.dbf".format(estado,archtr1)
        # escribearch(archivo1,'a',archlog)
        
        campos = [
            # ('infantes','[POB2] + [POB4] + [POB5]'),
            # ('jovenes','[POB7] + [POB9]'),
            # ('aduljov','[POB13] + [POB30] + [POB31]'),
            # ('adultos','[POB32] + [POB33] + [POB34] + [POB35] + [POB36]'),
            ('ancianos','[POB36_a] + [POB37] + [POB38] + [POB39] + [POB40] + [POB41]')
            ]
        
        for valores in campos:
            campo = valores[0]
            expresion = valores[1]
            dicc = {'archlog' : archlog,
                    'archivo1' : archivo1,
                    'campo' : campo,
                    'tipo' : 'LONG',
                    'precision' : 3,
                    'long' : "",
                    'expresion' : expresion,
                    'tipoexp' : "VB",
                    'bloquecodigo' : ""
                    }
            
            creacampo(dicc)
            calculacampo(dicc)
            
            escribearch(u"campo: {}, expresión: {}".format(campo,expresion),'a',archlog)
        escribearch(u"\nTerminado {}".format(estado),'a',archlog)
    escribearch(u"\n\nTerminado total",'a',archlog)

def copiatablamanzana(valores):
    import shutil

    try:
        estados = valores['estados']
        for estado in estados:
            print("\n\n")
            print (estado)
            origen = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/manzana_localidad.dbf'.format(estado)
            destino = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/cpv2020_manzana_poblacion.dbf'.format(estado)
            if os.path.exists(origen):
                
                shutil.copy(origen, destino)
                print (u"\n{} \ncopiado correctamente".format(destino))
            else:
                print (u"\n{} \nno existe".format(origen))

    except Exception as e:
        print (str(e))

def verificaarchivo(valores1):
    #Rutina para verificar que un archivo exista en la ruta y carpeta especificada
    estados = valores1['estados']
    subcarpeta = valores1['subcarpeta']
    arch = valores1['archivo']
    for estado in estados:
        archivo = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}/{}".format(estado, subcarpeta, arch)
        try:
            print ("\n")
            print (estado)
            if os.path.exists(archivo):
                print (u"--->>{} \nexiste".format(archivo))
            else:
                print (u"\tERROR--->>{} \n\tNO EXISTE".format(archivo))
        except Exception as e:
            print (str(e))

def borracampospob(valores2):

    #Rutina para borrar los campos de un archivo shp

    estados = valores2['estados']   # estados en los que se aplicará el borrado
    subcarpeta = valores2['subcarpeta'] # subcarpeta (en base a la estructura del scince 2020)
    arch = valores2['archivo']  # archivo (con extensión) que contiene los campos a borrar
    campos = valores2['campos']     #lista de campos a borrar

    def borracampos(estado, archivo, campos):
        print (u'Borrando campos de {}'.format(estado))
        print (archivo)
        print (campos)
        # arcpy.DeleteField_management(in_table=archivo,
        #                              drop_field=campos)
        
        # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
        # The following inputs are layers or table views: "manzana_localidad"
        # arcpy.DeleteField_management(in_table="manzana_localidad", drop_field="POB1;POB2;POB2_R;POB4;POB4_R;POB5;POB5_R;POB6;POB6_R;POB7;POB7_R;POB8;POB8_R;POB9;POB9_R;POB10;POB10_R;POB11;POB11_R;POB12;POB12_R;POB13;POB13_R;POB14;POB14_R;POB15;POB15_R;POB17;POB17_R;POB18;POB18_R;POB19;POB19_R;POB20;POB20_R;POB21;POB21_R;POB22;POB22_R;POB23;POB23_R;POB24;POB24_R;POB25;POB25_R;POB42;POB42_R;POB43;POB43_R;POB45;POB45_R;POB46;POB46_R;POB47;POB47_R;POB48;POB48_R;POB49;POB49_R;POB50;POB50_R;POB51;POB51_R;POB52;POB52_R;POB53;POB53_R;POB54;POB54_R;POB55;POB55_R;POB56;POB56_R;POB57;POB57_R;POB59;POB59_R;POB60;POB60_R;POB61;POB61_R;POB62;POB62_R;POB63;POB63_R;POB64;POB64_R;POB65;POB65_R;POB66;POB66_R;POB67;POB67_R;POB84;POB84_R;POB85;POB85_R;POB87;POB87_R;POB88;POB88_R;POB89;POB89_R;POB90;POB90_R;POB91;POB91_R;POB92;POB92_R;POB93;POB93_R;POB94;POB94_R;POB95;POB95_R;POB96;POB96_R;POB97;POB97_R;POB98;POB98_R;POB100;POB100_R;POB101;POB101_R;POB102;POB102_R;POB103;POB103_R;POB104;POB104_R;POB105;POB105_R;POB106;POB106_R;POB107;POB107_R;POB108;POB108_R;POB125_R;POB126_R;POB127_R;POB128_R;POB129_R;POB130_R;POB131_R;POB132_R;POB133_R;POB134_R;POB3;POB3_R;POB16;POB16_R;POB26;POB26_R;POB27;POB27_R;POB28;POB28_R;POB29;POB29_R;POB30;POB30_R;POB31;POB31_R;POB32;POB32_R;POB33;POB33_R;POB34;POB34_R;POB35;POB35_R;POB36;POB36_R;POB37;POB37_R;POB38;POB38_R;POB39;POB39_R;POB40;POB40_R;POB41;POB41_R;POB44;POB44_R;POB58;POB58_R;POB68;POB68_R;POB69;POB69_R;POB70;POB70_R;POB71;POB71_R;POB72;POB72_R;POB73;POB73_R;POB74;POB74_R;POB75;POB75_R;POB76;POB76_R;POB77;POB77_R;POB78;POB78_R;POB79;POB79_R;POB80;POB80_R;POB81;POB81_R;POB82;POB82_R;POB83;POB83_R;POB86;POB86_R;POB99;POB99_R;POB109;POB109_R;POB110;POB110_R;POB111;POB111_R;POB112;POB112_R;POB113;POB113_R;POB114;POB114_R;POB115;POB115_R;POB116;POB116_R;POB117;POB117_R;POB118;POB118_R;POB119;POB119_R;POB120;POB120_R;POB121;POB121_R;POB122;POB122_R;POB123;POB123_R;POB124;POB124_R;OID_1")

        arcpy.DeleteField_management(in_table="Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/manzana_localidad.shp".format(estado), drop_field="POB2_R;POB4_R;POB5_R;POB6_R;POB7_R;POB8_R;POB9_R;POB10_R;POB11_R;POB12_R;POB13_R;POB14_R;POB15_R;POB17_R;POB18_R;POB19_R;POB20_R;POB21_R;POB22_R;POB23_R;POB24_R;POB25_R;POB42_R;POB43_R;POB45_R;POB46_R;POB47_R;POB48_R;POB49_R;POB50_R;POB51_R;POB52_R;POB53_R;POB54_R;POB55_R;POB56_R;POB57_R;POB59_R;POB60_R;POB61_R;POB62_R;POB63_R;POB64_R;POB65_R;POB66_R;POB67_R;POB84_R;POB85_R;POB87_R;POB88_R;POB89_R;POB90_R;POB91_R;POB92_R;POB93_R;POB94_R;POB95_R;POB96_R;POB97_R;POB98_R;POB100_R;POB101;POB101_R;POB102;POB102_R;POB103;POB103_R;POB104;POB104_R;POB105;POB105_R;POB106;POB106_R;POB107;POB107_R;POB108;POB108_R;POB125_R;POB126_R;POB127_R;POB128_R;POB129_R;POB130_R;POB131_R;POB132_R;POB133_R;POB134_R;POB3_R;POB16_R;POB26_R;POB27_R;POB28_R;POB29_R;POB30_R;POB31_R;POB32_R;POB33_R;POB34_R;POB35_R;POB36_R;POB37_R;POB38_R;POB39_R;POB40_R;POB41_R;POB44_R;POB58_R;POB68_R;POB69_R;POB70_R;POB71_R;POB72_R;POB73_R;POB74_R;POB75_R;POB76_R;POB77_R;POB78_R;POB79_R;POB80_R;POB81_R;POB82_R;POB83_R;POB86_R;POB99_R;POB109;POB109_R;POB110;POB110_R;POB111;POB111_R;POB112;POB112_R;POB113;POB113_R;POB114;POB114_R;POB115;POB115_R;POB116;POB116_R;POB117;POB117_R;POB118;POB118_R;POB119;POB119_R;POB120;POB120_R;POB121;POB121_R;POB122;POB122_R;POB123;POB123_R;POB124;POB124_R;OID_1;FID_loc_ur;CVEGEO_1;NOM_ENT;NOM_MUN;NOMGEO;CABECERA;POB1_1;POB2_1;POB2_R_1;POB4_1;POB4_R_1;POB5_1;POB5_R_1;POB6_1;POB6_R_1;POB7_1;POB7_R_1;POB8_1;POB8_R_1;POB9_1;POB9_R_1;POB10_1;POB10_R_1;POB11_1;POB11_R_1;POB12_1;POB12_R_1;POB13_1;POB13_R_1;POB14_1;POB14_R_1;POB15_1;POB15_R_1;POB17_1;POB17_R_1;POB18_1;POB18_R_1;POB19_1;POB19_R_1;POB20_1;POB20_R_1;POB21_1;POB21_R_1;POB22_1;POB22_R_1;POB23_1;POB23_R_1;POB24_1;POB24_R_1;POB25_1;POB25_R_1;POB42_1;POB42_R_1;POB43_1;POB43_R_1;POB45_1;POB45_R_1;POB46_1;POB46_R_1;POB47_1;POB47_R_1;POB48_1;POB48_R_1;POB49_1;POB49_R_1;POB50_1;POB50_R_1;POB51_1;POB51_R_1;POB52_1;POB52_R_1;POB53_1;POB53_R_1;POB54_1;POB54_R_1;POB55_1;POB55_R_1;POB56_1;POB56_R_1;POB57_1;POB57_R_1;POB59_1;POB59_R_1;POB60_1;POB60_R_1;POB61_1;POB61_R_1;POB62_1;POB62_R_1;POB63_1;POB63_R_1;POB64_1;POB64_R_1;POB65_1;POB65_R_1;POB66_1;POB66_R_1;POB67_1;POB67_R_1;POB84_1;POB84_R_1;POB85_1;POB85_R_1;POB87_1;POB87_R_1;POB88_1;POB88_R_1;POB89_1;POB89_R_1;POB90_1;POB90_R_1;POB91_1;POB91_R_1;POB92_1;POB92_R_1;POB93_1;POB93_R_1;POB94_1;POB94_R_1;POB95_1;POB95_R_1;POB96_1;POB96_R_1;POB97_1;POB97_R_1;POB98_1;POB98_R_1;POB100_1;POB100_R_1;POB101_1;POB101_R_1;POB102_1;POB102_R_1;POB103_1;POB103_R_1;POB104_1;POB104_R_1;POB105_1;POB105_R_1;POB106_1;POB106_R_1;POB107_1;POB107_R_1;POB108_1;POB108_R_1;POB125_R_1;POB126_R_1;POB127_R_1;POB128_R_1;POB129_R_1;POB130_R_1;POB131_R_1;POB132_R_1;POB133_R_1;POB134_R_1;POB3_1;POB3_R_1;POB16_1;POB16_R_1;POB26_1;POB26_R_1;POB27_1;POB27_R_1;POB28_1;POB28_R_1;POB29_1;POB29_R_1;POB30_1;POB30_R_1;POB31_1;POB31_R_1;POB32_1;POB32_R_1;POB33_1;POB33_R_1;POB34_1;POB34_R_1;POB35_1;POB35_R_1;POB36_1;POB36_R_1;POB37_1;POB37_R_1;POB38_1;POB38_R_1;POB39_1;POB39_R_1;POB40_1;POB40_R_1;POB41_1;POB41_R_1;POB44_1;POB44_R_1;POB58_1;POB58_R_1;POB68_1;POB68_R_1;POB69_1;POB69_R_1;POB70_1;POB70_R_1;POB71_1;POB71_R_1;POB72_1;POB72_R_1;POB73_1;POB73_R_1;POB74_1;POB74_R_1;POB75_1;POB75_R_1;POB76_1;POB76_R_1;POB77_1;POB77_R_1;POB78_1;POB78_R_1;POB79_1;POB79_R_1;POB80_1;POB80_R_1;POB81_1;POB81_R_1;POB82_1;POB82_R_1;POB83_1;POB83_R_1;POB86_1;POB86_R_1;POB99_1;POB99_R_1;POB109_1;POB109_R_1;POB110_1;POB110_R_1;POB111_1;POB111_R_1;POB112_1;POB112_R_1;POB113_1;POB113_R_1;POB114_1;POB114_R_1;POB115_1;POB115_R_1;POB116_1;POB116_R_1;POB117_1;POB117_R_1;POB118_1;POB118_R_1;POB119_1;POB119_R_1;POB120_1;POB120_R_1;POB121_1;POB121_R_1;POB122_1;POB122_R_1;POB123_1;POB123_R_1;POB124_1;POB124_R_1;OID_12")

    for estado in estados:
        archivo = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/{}/{}".format(estado, subcarpeta, arch)
        try:
            print ("\n")
            print (estado)
            if os.path.exists(archivo):
                print (u"--->>{} \nexiste".format(archivo))
                borracampos(estado, archivo, campos)
            else:
                print (u"\tERROR--->>{} \n\tNO EXISTE".format(archivo))
        except Exception as e:
            print (str(e))

def listacampos(valores3):
    archlog = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/log_campos_estados1.txt' 
    escribearch(u'\n\niniciando proceso\n\n', 'w', archlog)
    estados = valores['estados']

    def extraer_campos_shapefile(ruta_shapefile):
        campos = [field.name for field in arcpy.ListFields(ruta_shapefile)]
        numero_campos = len(campos)
        datos = {'cantidad' : numero_campos,
                 'campos' : campos}
        return datos

    for estado in estados:
        ruta_shapefile = u'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/manzana_localidad.shp'.format(estado)
        datos = extraer_campos_shapefile(ruta_shapefile)
        campos = datos['campos']
        cantidad = datos['cantidad']
        # mensaje = u"\n\testado: {}--> {} campos \nruta: {} \ncampos: \n{}".format(estado, cantidad, ruta_shapefile, campos)
        mensaje = u"{}\t{}".format(estado, cantidad)
        escribearch(mensaje, 'a', archlog)

    escribearch('\nproceso terminado', 'a', archlog)
        

estados = [ 
            # u"Aguascalientes",
            u"Baja California",
            # u"Baja California Sur",
            # u"Campeche",
            # u"Chiapas",
            # u"Chihuahua",
            # u"Ciudad de Mexico",
            # u"Coahuila",  
            # u"Colima",          
            # u"Durango",
            # u"Guanajuato",
            # u"Guerrero",
            # u"Hidalgo",
            # u"Jalisco",
            # u"Mexico",
            # u"Michoacan de Ocampo",
            # u"Morelos",
            # u"Nayarit",
            # u"Nuevo Leon",
            # u"Oaxaca",
            # u"Puebla",
            # u"Queretaro",
            # u"Quintana Roo",
            # u"San Luis Potosi",
            # u"Sinaloa",
            # u"Sonora",
            # u"Tabasco",
            # u"Tamaulipas",
            # u"Tlaxcala",
            # u"Veracruz de Ignacio de la Llave",
            # u"Yucatan",
            # u"Zacatecas"
            ]

valores = {'estados' : estados}

valores1 = {'estados' : estados,
            'subcarpeta': 'tablas',
            'archivo': 'cpv2020_manzana_poblacion.dbf'}

camposbase = '"POB1;POB2;POB3;POB4;POB5;POB6;POB7;POB8;POB9;POB10;POB11;POB12;POB13;POB14;POB15;POB16;POB17;POB18;POB19;POB20;POB21;POB22;POB23;POB24;POB25;POB26;POB27;POB28;POB29;POB30;POB31;POB32;POB33;POB34;POB35;POB36;POB36_a;POB37;POB38;POB39;POB40;POB41;POB42;POB43;POB44;POB45;POB46;POB47;POB48;POB49;POB50;POB51;POB52;POB53;POB54;POB55;POB56;POB57;POB58;POB59;POB60;POB61;POB62;POB63;POB64;POB65;POB66;POB67;POB68;POB69;POB70;POB71;POB72;POB73;POB74;POB75;POB76;POB77;POB78;POB79;POB80;POB81;POB82;POB83;POB84;POB85;POB86;POB87;POB88;POB89;POB90;POB91;POB92;POB93;POB94;POB95;POB96;POB97;POB98;POB99;POB100"'

# camposcomp = "area_has;dens_ha;POB36_a;ordinal;pobdom;"

# camposborr = camposcomp + camposbase

valores2 = {'estados' : estados,
            'subcarpeta': 'cartografia',
            'archivo': 'manzana_localidad.shp',
            'campos' : camposbase}

valores3 = {'estados' : estados,
            'subcarpeta': 'cartografia',
            'archivo': 'manzana_localidad.shp',
            'campos' : camposbase}


# Llama a la función para ejecutar el código
# tablapob(estados)
calc_area_dens(estados)
# rangos_de_edad(estados)
# copiatablamanzana(valores)
# verificaarchivo(valores1)
# borracampospob(valores2)
# listacampos(valores3)

