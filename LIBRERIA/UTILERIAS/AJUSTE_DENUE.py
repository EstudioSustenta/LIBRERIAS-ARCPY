# -*- coding: utf-8 -*-

# PROGRAMA PARA ADECUAR LOS ARCHIVOS DEL DENUE (INEGI), AGREGANDO LOS CAMPOS CORRESPONDIENTES

# 1
# Define dos listas, actividad y codigos, que estan relacionadas entre sí.

# 2
# Define una función 'comp_denue' que toma como argumento la ruta a un archivo shapefile.

# 3
# Dentro de la función 'comp_denue', se definen dos nombres de campo, 'scian' y 'nomb_scian'.

# 4
# Luego, el código intenta agregar estos dos campos al archivo shapefile especificado 
# utilizando la función AddField_management de arcpy.

# 5
# Después de agregar los campos, define una función interna 'asigna_cod'.

# 6
# Dentro de la función 'asigna_cod', se crea un UpdateCursor en el archivo shapefile. 
# Este cursor permite iterar sobre las filas del archivo shapefile y actualizar los valores 
# de los campos.

# 7
# Para cada fila en el archivo shapefile, el código extrae los dos primeros dígitos del 
# campo codigo_act y los asigna al campo 'scian'. También asigna un valor al campo 'nomb_scian' 
# que es una cadena formada por el valor de 'scian' y el correspondiente valor de la lista 
# actividad basado en el índice del valor de 'scian' en la lista codigos.

# 8
# Finalmente, se imprime un mensaje indicando que los campos scian y 'nomb_scian' se han 
# agregado y llenado correctamente.

# 9
# Después de definir la función 'comp_denue', el código crea una instancia de Tkinter y 
# muestra un cuadro de diálogo para seleccionar un directorio. Una vez definido el 
# archivo se ejecuta la función interna 'asigna_cod' con el parámetro del archivo
# terminado con la cadena 'cadena'.



import arcpy
import os
import Tkinter, tkFileDialog
import itertools

# define listas

actividad = ["Agricultura y ganadería",
    "Minería",
    "Energía eléctrica, y gas natural",
    "Construcción",
    "Industrias manufactureras",
    "Industrias manufactureras",
    "Industrias manufactureras",
    "Comercio al por mayor",
    "Comercio al por menor",
    "Transportes, correos y almac.",
    "Transportes, correos y almac.",
    "Información en medios masivos",
    "Serv. financieros y de seguros",
    "Serv. inmobiliarios y de alquiler",
    "Serv. profesionales, científicos y técnicos",
    "Administración de grupos empresariales",
    "Serv. manejo de residuos, y serv. de remediación",
    "Serv. educativos",
    "Serv. de salud y de asistencia social",
    "Serv. de esparcimiento culturales y deportivos",
    "Serv. de alojamiento temporal y de prep. de alimentos",
    "Otros Serv. excepto actividades gubernamentales",
    "Actividades gubernamentales, de impartición de justicia"] # lista sin abreviaciones al final del código

codigos = ["11","21","22","23","31","32","33","43","46","48","49","51","52","53","54",
    "55","56","61","62","71","72","81","93"]

cadena = 'denue_wgs84z13.shp'     # define la terminación de los archivos denúe que se van a modificar


def asigna_cod(archivo_shapefile, scian, nombsian):
            
    # Actualiza el campo nuevo con los dos primeros dígitos de 'codigo_act'
    try:

        with arcpy.da.UpdateCursor(archivo_shapefile, ['codigo_act', scian, nombsian]) as cursor:
            # print ("inicio de cálculo de cantidad de registros...")
            # registros = len(list(cursor))
            # registros = "{:,}".format(registros)
            # contador = 0
            # print ("inicio de bucle...")
            for row in cursor:
            # for row in itertools.islice(cursor, 20):      # Esta línea escribe un número determinado de iteraciones
                # print ("Campo nomb_scian: '{}'".format(row[2]))

                # contador += 1

                # Verifica si 'codigo_act' tiene al menos dos caracteres antes de intentar extraer los dos primeros dígitos
                if row[0] and len(str(row[0])) >= 2:
                    
                    # Convierte 'codigo_act' a cadena y toma los dos primeros dígitos
                    dos_primeros_digitos = str(row[0])[:2]
                    
                    # Asigna los dos primeros dígitos al campo 'scian'
                    if row[1] == "": # or row[1] == " " or row[1] == None:

                        row[1] = dos_primeros_digitos
                        cursor.updateRow(row)
                        # print ("se ha modificado el registro # --{}-- con '{}'".format(contador, dos_primeros_digitos))

                    # else:
                    #     # print("El campo '{}' ya tiene contenido: '{}'.".format(scian, row[1])).encode('utf-8')
                    #     None

                    # Asigna valores al campo 'nombsian'
                    if row[2] == "": # or row[2] == " " or row[2] == None:
                        
                        row2 = actividad[codigos.index(row[1])]
                        row[2] = "{}-{}".format(row[1], row2)
                        cursor.updateRow(row)
                        # print ("se ha modificado el campo {} con registro {} con '{}'".format(nombsian, contador, (row[2]).encode('utf-8')))

                    # else:
                    #     # print("El campo '{}' ya tiene contenido: '{}'".format(nombsian, (row[2].encode('utf-8'))))

                else:
                    print(">> ERROR en el proceso con valor '{}'".format((row[0]).encode('utf-8')))

            # print ("se han modificado {} registros".format(registros))

    except Exception as e:
        print (str(e))

def comp_denue(archivo_shapefile):
    # Especifica la ruta completa al archivo shapefile
    

    # Nombre del nuevo campo a agregar
    scian = "scian"
    nombsian = "nomb_scian"
    campos = [f.name for f in arcpy.ListFields(archivo_shapefile)]

    # Crea el nuevo campo en el shapefile
    if scian not in campos:    
        try:

            arcpy.AddField_management(in_table=archivo_shapefile, field_name=scian, field_type="TEXT", field_precision="", field_scale="", field_length="3", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
            carpetaedo = (os.path.split(os.path.split(os.path.dirname(archivo_shapefile))[0])[1])
            print("\nCampo '{}' agregado correctamente en '{}'".format(scian, carpetaedo)).encode('utf-8')
        except Exception as e:
            print (str(e))
    else:
        print ("El campo '{}' ya existe en '{}'".format(scian.encode('utf-8'), archivo_shapefile.encode('utf-8')))
    
    if nombsian not in campos:
        try:
            arcpy.AddField_management(in_table=archivo_shapefile, field_name=nombsian, field_type="TEXT", field_precision="", field_scale="", field_length="160", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
            carpetaedo = (os.path.split(os.path.split(os.path.dirname(archivo_shapefile))[0])[1])
            print ("\nCampo '{}' agregado correctamente en '{}'\n\n".format(nombsian, carpetaedo)).encode('utf-8')
        except Exception as e:
            print (str(e))
    else:
        print ("El campo '{}' ya existe en '{}'".format(nombsian.encode('utf-8'), archivo_shapefile.encode('utf-8')))

            
    print ("iniciando proceso de asignación de valores a campos. Por favor espere...")
    asigna_cod(archivo_shapefile, scian, nombsian)

    print("\n\nSe han agregado los campos '{}' y '{}', y se ha llenado correctamente en el archivo shapefile.\n\n".format(scian,nombsian)).encode('utf-8')

carpeta_inicio = "Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/México/diccionario_de_datos/conjunto_de_datos/denue_wgs84z13.shp"
                #   Y:\GIS\MEXICO\VARIOS\INEGI\DENUE\2023\México\diccionario_de_datos\conjunto_de_datos\denue_wgs84z13.shp

def inicio():
    # Crear una instancia de Tkinter y ocultar la ventana principal
    root = Tkinter.Tk()
    root.withdraw()

    # Mostrar un cuadro de diálogo para seleccionar la carpeta
    directorio = tkFileDialog.askdirectory(parent=root, initialdir=carpeta_inicio, title='Por favor selecciona un directorio')

    # Para cada directorio, subdirectorio y archivo en el directorio seleccionado
    for dirpath, dirnames, archivos in os.walk(directorio):
        # Para cada archivo en el directorio actual
        print (dirnames)
        for nombre_archivo in archivos:
            # Si el archivo es un .shp
            if nombre_archivo.endswith(cadena):
                # Imprimir la ruta completa del archivo .shp
                shapefile = (os.path.join(dirpath, nombre_archivo))
                print (shapefile.encode('utf-8'))
                comp_denue(shapefile)

def archivodenue():
    # Crear una instancia de Tkinter y ocultar la ventana principal
    root = Tkinter.Tk()
    root.withdraw()

    # Mostrar un cuadro de diálogo para seleccionar un archivo
    nombre_archivo = tkFileDialog.askopenfilename(parent=root, 
                                                  initialdir=carpeta_inicio, 
                                                  title="Por favor selecciona un archivo a ajustar", 
                                                  filetypes=[('Shapefile', '*.shp')]
                                                  )
    print (nombre_archivo.encode('utf-8'))
    cadena = os.path.basename(nombre_archivo)

    if nombre_archivo.endswith(cadena):
        # Imprimir la ruta completa del archivo .shp
        print ("{} coincide con {}, se iniciará el proceso de complemento 'denue'".format(cadena.encode('utf-8'), nombre_archivo.encode('utf-8')))
        comp_denue(nombre_archivo)
    else:
        print (">> ERROR, {} NO coincide con {}, NO se iniciará el proceso de complemento 'denue'".format(cadena.encode('utf-8'), nombre_archivo.encode('utf-8')))



# CÓDIGOS SIN ABREVIACIONES:

# "11",      "Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza",
# "21",      "Minería",
# "22",      "Generación, transmisión, distribución y comercialización de energía eléctrica, suministro de agua y de gas natural por ductos al consumidor final",
# "23",      "Construcción",
# "31",      "Industrias manufactureras",
# "32",      "Industrias manufactureras",
# "33",      "Industrias manufactureras",
# "43",      "Comercio al por mayor",
# "46",      "Comercio al por menor",
# "48",      "Transportes, correos y almacenamiento",
# "49",      "Transportes, correos y almacenamiento",
# "51",      "Información en medios masivos",
# "52",      "Servicios financieros y de seguros",
# "53",      "Servicios inmobiliarios y de alquiler de bienes muebles e intangibles",
# "54",      "Servicios profesionales, científicos y técnicos",
# "55",      "Dirección y administración de grupos empresariales o corporativos",
# "56",      "Servicios de apoyo a los negocios y manejo de residuos, y servicios de remediación",
# "61",      "Servicios educativos",
# "62",      "Servicios de salud y de asistencia social",
# "71",      "Servicios de esparcimiento culturales y deportivos, y otros servicios recreativos",
# "72",      "Servicios de alojamiento temporal y de preparación de alimentos y bebidas",
# "81",      "Otros servicios excepto actividades gubernamentales",
# "93",      "Actividades legislativas, gubernamentales, de impartición de justicia y de organismos internacionales y extraterritoriales",

