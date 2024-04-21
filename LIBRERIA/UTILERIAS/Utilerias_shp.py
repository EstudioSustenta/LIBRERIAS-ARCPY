# -*- coding: utf-8 -*-

"""
Este programa debe ejecutarse con el interpretador de PYTHON 2.7 de arcmap para que funcione
Contiene funciones de utilería para trabajar con archivos shp
Returns: None
"""

import os
import arcpy
import re
import datetime
from ESUSTENTA_UTILERIAS import log
from UTIL_JSON import lodicson


def existe(elemento):
    'verifica si la carpeta o el archivo existen fisicamente en disco'
    if os.path.exists(elemento):
        return True
    else:
        return False

def proyectar(fuente, destino, codepsg = 32613, sobreescribir = True):
    """
    Proyecta el un archivo fuente a un archivo destino con el 
    código epsg definido en el parámetro, el código epsg de salida
    siempres será 
    """
    codepsgdestino = codepsg      # Código EPSG = 32613 para WGS_1984_UTM_Zone_13N

    # obtiene la ruta del archivo destino
    dirdest = (os.path.dirname(destino))

    # verifica que exista la carpeta destino, de lo contrario la crea
    if not os.path.exists(dirdest):
        os.makedirs(dirdest)
    if existe(fuente):  #si ya existe el archivo destino lo proyecta sobreescribiéndolo
        if not os.path.exists(destino) and sobreescribir:
            proy(fuente,destino, codepsgdestino)
            if os.path.exists(destino) and epsg(destino) == codepsgdestino:
                return (u'el archvo se proyectó exitosamente')
            else:
                return (u'el archvo no pudo proyectarse')
        else:
            return (u'El shapefile destino ya existe, no se proyectó')
        
    else:
        return (u'no existe el archivo fuente')

def elimina_campos(archivo1, campos):
    """
    Elimina los campos de la lista 'campos' de un archivo shapefile 'archivo1'
    """
    try:
        arcpy.DeleteField_management(archivo1, campos)
        return True
    except:
        return False

def calcula_campo_shp(shape,campo,expresion,tipo):
    """
    Calcula el área y densidad de el shapefile 'shape' agregando el contenido
    en el campo 'campo' con la expresión 'expresion' del tipo 'tipo'
    se entiende que el tipo de expresiones puede ser 'PYTHON' o 'VB'
    """
    try:
        arcpy.AddField_management(in_table=shape, field_name=campo,field_type='FLOAT', field_precision="4")
        arcpy.CalculateField_management(in_table=shape,field=campo,expression=expresion,expression_type=tipo) # calcula el área
        arcpy.AddField_management(in_table=shape, field_name='densidad',field_type='FLOAT', field_precision="2")
        arcpy.CalculateField_management(in_table=shape,field='densidad',expression='[POB1] / [area_has]',expression_type='VB')     #Calcula la densidad

        return u'Campos "{}" y "densidad" creados y calculados'.format(campo)
    except Exception as e:
        return e

def borra_campos(shape, campos):
    """
    Elimina los campos suministrado en la lista 'campos' en el archivo 'shape'
    """
    try:
        # for campo in campos:
        arcpy.DeleteField_management(in_table=shape, drop_field=campos)
        return 'Campos eliminados de shapefile {}'.format(shape)
    except Exception as e:
        return e

def crea(shapeorig, destino, campos):
    """
    Esta función copia un archivo shapefile y borra los campos definidos en el parámetro 'campos'
    Esto se realiza para eliminar las columnas de la tabla que contienen palabras con acentos,
    puesto que no fue posible integrar columnas de texto con acentos a la base de datos y
    conservar el contenido del campo 'CVEGEO' con ceros iniciales.
    ejemplos de parámetros
    shapeorig = "C:/SCINCE 2020/01_AGS/cartografia/municipal.shp"
    campos = 'NOM_ENT;NOMGEO'
    return: estado del resultado del script
    """
    if not os.path.exists(destino) and os.path.exists(shapeorig):
        arcpy.CopyFeatures_management(in_features=shapeorig,
                                    out_feature_class=destino,
                                    config_keyword="",
                                    spatial_grid_1="0",
                                    spatial_grid_2="0",
                                    spatial_grid_3="0")
        arcpy.DeleteField_management(in_table=destino, drop_field=campos)
        if os.path.exists(destino):
            return '/n\n"{}" copiado satisfactoriamente'.format(destino)
        else:
            return '\n\n"===>> ERROR: {}" no se copió.'.format(destino)
    else:
        return '\n\n===>> ERROR: Origen no existe o destino ya existe'.format(destino)

def borrashp(shape):
    """
    Elimina un shapefile (con todos los archivos asociados)
    del disco.
    \nshape: nombre del archivo a borrar (ruta completa)
    \nreturns: reporte de las acciones
    """
    if os.path.exists(shape):
        if os.path.exists(shape):
            arcpy.Delete_management(shape)
        else:
            return '"{}" no existe en disco'.format(shape)
        if not os.path.exists(shape):
            return '"{}" borrado satisfactoriamente'.format(shape)
        else:
            return '"{}" no se pudo borrar'.format(shape)
    else:
        return '"{}" no existe en disco'.format(shape)

def elimina_shp(shape):
    u"""
    Elimina físicamente de disco el archivo que se le envíe
    """
    try:
        if os.path.exists(shape):
            arcpy.Delete_management(shape)
        else:
            return 'El archivo "{}" no existe en disco'.format(shape)
        if os.path.exists(shape):
            return 'No se ha podido eliminar el shapefile "{}"'.format(shape)
        else:
            return 'El shapefile "{}" ha sido eliminado de disco'.format(shape)
    except Exception as e:
        return '>>>>ERROR {}'.format(e)

def remueve_capa(mxd, df, nombre_capa):
    """Elimina una capa del mapa actual."""
    
    # Buscar la capa por su nombre
    capas = arcpy.mapping.ListLayers(mxd, nombre_capa, df)
    if capas:
        capa = capas[0]
        arcpy.mapping.RemoveLayer(df, capa)
        return("Capa '{}' eliminada del mapa actual.".format(nombre_capa))
    else:
        return("No se encontró la capa '{}' en el mapa actual.".format(nombre_capa))

def cargar_capa(mxd, df, ruta_capa):
    """
    Carga una capa a partir de un archivo shapefile de disco
    en el mapa y dataframe definidos
    """


    try:
        if os.path.exists(ruta_capa):
            # Obtener el nombre de la capa sin extensión
            nombre_capa = os.path.basename(ruta_capa)
            nombre_capa = os.path.splitext(nombre_capa)[0]

            # Verificar si la capa ya está agregada al mapa
            capa_existente = arcpy.mapping.ListLayers(mxd, nombre_capa, df)

            if not capa_existente:
                # Construir la ruta completa a la capa
                # Agregar la capa al data frame
                capa = arcpy.mapping.Layer(ruta_capa) # crea el objeto shapefile basado en la ruta
                arcpy.mapping.AddLayer(df, capa) # Agrega el shapefile al dataframe definido
                mensaje= u"Capa '{}' agregado correctamente al dataframe.".format(nombre_capa)
            else:
                mensaje= u"{} ya existe en el dataframe, no se agregó.".format(nombre_capa)
        else:
            mensaje='No existe el archivo {}'.format(ruta_capa)
        
        return mensaje

    except Exception as e:
        return u">>>>> ERROR: '{}'.".format(e)

def zoom_extent(mxd, df, capa, over=0):
    """
    Hace zoom extent a una capa del dataframe.
    Si se especifica el parámetro 'over', se está 
    indicando que se ampliará la vista el porcentaje
    adicional definido en el parámetro. (3%, 20%, etc.)
    no se debe agregar el signo de porcentaje.
    """

    try:
        lyr_sistema = arcpy.mapping.ListLayers(mxd, capa)[0]    # Obtener acceso a la capa "nombre_capa" por su nombre
        extent = lyr_sistema.getExtent()    # Obtener la extensión de la capa "nombre_capa"
        df.extent = extent  # Establecer la extensión de la vista de datos a la extensión de la capa "nombre_capa"
        mensaje=u'Zoom extent aplicado con "0%" de ajuste en {}'.format(capa)
        if over != 0:
            porcentaje= float(1 + (float(over) / 100))
            df.scale = df.scale * porcentaje
            mensaje=u'Zoom extent aplicado con "{}%" de ajuste en "{}"'.format(over, capa)
        return mensaje
    except Exception as e:
        return u'>>>>>ERROR en zoom_extent: {}'.format(e)

def aplica_simbologia(mxd, df, capa, lyr):
    """
    Aplica la simbología a la capa con la simbología 'lyr'
    mxd = objeto mapa
    df = objeto dataframe
    capa = nombre de la capa (en el dataframe del mapa)
    lyr = ruta completa del archivo 
    """
    try:
        lyr_capa = arcpy.mapping.ListLayers(mxd,capa,df)[0]
        lyr_capa = lyr_capa.datasetName
        arcpy.ApplySymbologyFromLayer_management(lyr_capa,lyr)
        return u'Simbología aplicada en "{}"'.format(capa)
    
    except Exception as e:
        return u'>>>>>ERROR: no se ha aplicado la simbología "{}" a la capa "{}"'.format(os.path.basename(lyr), capa)

def transp(mxd, df, capa, transparencia):
    """
    Aplica una transparencia a la capa definida
    """

    try:
        for capatr in arcpy.mapping.ListLayers(mxd, "*", df):
            if capatr.name == capa:
                capatr.transparency = transparencia
        return u'Transparencia del "{}" aplicado a "{}"'.format(str(transparencia), capa)
    except Exception as e:
        return u'>>>>>ERROR en transp: {}'.format(e)

def activar_rotulos(mxd, df, capa, campo_rotulo):

    """
    Activa los rótulos de una capa mostrando los datos del campo 'campo'
    """

    try:
        capa = arcpy.mapping.Layer(capa)
        # Habilita los rótulos para la capa
        capa.showLabels = True
        # Configura la expresión de rótulo
        labelClass = capa.labelClasses[0]
        labelClass.expression = u"[{}]".format(campo_rotulo)
        return u'Rótulos activados en "{}" con el campo "{}"'.format(capa, campo_rotulo)
    except Exception as e:
        return u'>>>>>ERROR en activar_rotulos: {}'.format(e)

def activar_rot_exp(mxd, df, capa, expresion):
    """
    Activa los rótulos con una expresión SQL
    """

    try:
        capa = arcpy.mapping.Layer(capa)
        # Configura la expresión de rótulo
        labelClass = capa.labelClasses[0]
        labelClass.expression = u"{}".format(expresion)
        # Habilita los rótulos para la capa
        capa.showLabels = True
        
        return u'Rótulos activados en "{}" con la expresión "{}"'.format(capa, expresion)
    except Exception as e:
        return u'>>>>>ERROR en activar_rot_exp:"{}", {}'.format(capa, e)

def desactivar_rotulos(mxd, df, capa):
    """
    Desactiva los rótulos de una capa
    """

    try:
        # Obtiene la capa activa del mapa
        capa = arcpy.mapping.ListLayers(mxd, capa)[0]  # Ajusta el nombre de la capa según tu capa específica
        # Habilita los rótulos para la capa
        capa.showLabels = False
    except Exception as e:
        return u'>>>>>ERROR en desactivar_rotulos: {}'.format(e)

def refresca():
    """
    Refresca la vista del dataframe activo
    """
    arcpy.RefreshActiveView()
    return u'RefreshActiveView aplicado'

def leyenda(mxd, nueva_altura=0):
    """
    Ajusta la altura de la leyenda a la altura de la página

    FALTA: HACER QUE SE AJUSTE LA LEYENDA TAMBIÉN EN EL EJE 'X' (SIN AFECTAR LA VISUALIZACIÓN)
    """
    
    try:
            
        # Encuentra el cuadro de leyendas (legend) en el diseño
        cuadro_de_leyendas = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
        # Verifica si el cuadro de leyendas se sale del layout
        # Obtiene las coordenadas y el alto del cuadro de leyendas en el diseño
        x_leyenda = cuadro_de_leyendas.elementPositionX
        y_leyenda = cuadro_de_leyendas.elementPositionY
        alto_leyenda = cuadro_de_leyendas.elementHeight
        # Obtiene el alto del layout (página)
        


        if nueva_altura == 0:
            alto_layout = mxd.pageSize.height
            nueva_altura = y_leyenda
            nueva_altura = alto_layout - 2.5 - y_leyenda
            limite=alto_layout - 2.5
            if y_leyenda + alto_leyenda > limite:    # Calcula la nueva altura para ajustar al alto del layout
                # Establece la nueva altura para el cuadro de leyendas
                cuadro_de_leyendas.elementHeight = nueva_altura
                ancho=cuadro_de_leyendas.elementWidth
                return u'Se ha ajustado la leyenda a {} cm'.format(str(round(nueva_altura, 2)))
        else:
            ancho=cuadro_de_leyendas.elementWidth
            # Establece la nueva altura para el cuadro de leyendas
            cuadro_de_leyendas.elementHeight = nueva_altura
            ancholeyenda=2.2
            if ancho < ancholeyenda:
                cuadro_de_leyendas.elementWidth=ancholeyenda
                mensaje = (u"Ancho de leyenda menor: " + str(ancho))
            else:
                mensaje = (u"Ancho de leyenda mayor: " + str(ancho))
            return mensaje
            # return u'Se ha ajustado la leyenda a {} cm'.format(str(round(nueva_altura, 2)))

    except Exception as e:
        return u'>>>>>ERROR en leyenda: {}'.format(e)

def mueve_leyenda_x(mxd, posicion):
    """
    Mueve la leyenda en el eje 'x' a la posición indicada
    """
    try:
        # Obtener la leyenda por su nombre
        leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]
        # Mueve la leyenda
        leyenda.elementPositionX = posicion  # Mueve la leyenda a la posición indicada
    except Exception as e:
        return u'>>>>>ERROR en mueve_leyenda_x: {}'.format(e)

def exportar(mxd, r_dest, nombarch, jpg=False, serial=False):
    """
    Exporta un mapa a archivos pdf y/o jpg\n
    parámetros:\n
    nombarch: nombre del archivo (sin ruta ni extensión)
    """

    try:
        if len(str(arcpy.env.numeromapa)) <= 1:
            num_mapa = "0" + str(arcpy.env.numeromapa)
        else:
            num_mapa = str(arcpy.env.numeromapa)
        ruta = "{0}{2} {1}".format(r_dest,nombarch,num_mapa)
        
        # Proceso de ajuste de leyenda
        cuadro_de_leyendas = arcpy.mapping.ListLayoutElements(mxd, u"LEGEND_ELEMENT")[0]    #crea el objeto del cuadro de leyenda
        alto_leyenda_orig = cuadro_de_leyendas.elementHeight    # Obtiene la altura del cuadro de leyenda
        arcpy.env.overwriteOutput = True  # Permitir sobrescribir archivos de salida
        ruta_pdf = ruta + ".pdf"
        arcpy.mapping.ExportToPDF(mxd, ruta_pdf, "page_layout", 1024, 768, 350)  # Exportar a PDF
        if os.path.exists(ruta_pdf):
            mensaje='Se ha exportado el archivo PDF: "{}"'.format(ruta_pdf)
        else:
            mensaje='>>>>>ERROR: Se ha ejecutado el proceso pero no se ha creado el archivo pdf\n{}'.format(ruta_pdf)
        if jpg==True:
            ruta_jpg = ruta + ".jpg" 
            arcpy.mapping.ExportToJPEG(mxd, ruta_jpg, u"page_layout", 1024, 768, 250)  # Exportar a JPEG
            if os.path.exists(ruta_jpg):
                mensaje += ', se ha exportado el archivo JPG'
            else:
                mensaje='>>>>>ERROR: Se ha ejecutado el proceso pero no se ha creado el archivo jpg'

        cuadro_de_leyendas.elementHeight = alto_leyenda_orig
        if serial == True:
            arcpy.env.numeromapa += 1
            mensaje += ', se ha incrementado el serial de mapas'
        mensaje += '.'
        return mensaje
    except Exception as e:
        return '>>>>>ERROR en exportar: {}'.format(e)

def renombra(mxd, caparen, nuevonomb):
    """
    Renombra una capa en un dataframe
    """
    try:
        capas = arcpy.mapping.ListLayers(mxd)
        for capa in capas:
            if capa.name == caparen:
                capa.name = nuevonomb
                mensaje = "'{}' renombrada como '{}'".format(caparen, nuevonomb)
            else:
                mensaje="La capa '{}' no existe en el dataframe.".format(caparen)
        return mensaje
    except Exception as e:
        return '>>>>>ERROR en renombra: {}'.format(e)

def formato_layout(mxd, titulo1, subtitulo1):
    """
    Ajusta el subtítulo y la fecha del layout del mapa
    """
    try:
        # Obtiene la fecha actual
        fecha=datetime.datetime.now()
        fecha= fecha.strftime("%Y/%b/%d/%a")
        
        # Acceder a elementos de diseño por su nombre
        titulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"TITULO")[0]             #debe de existir el elemento de texto en layout llamado "TITULO"
        subtitulo = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"SUBTITULO")[0]       #debe de existir el elemento de texto en layout llamado "SUBTITULO"
        tfecha = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", u"FECHA")[0]              #debe de existir el elemento de texto en layout llamado "FECHA"
        leyenda = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", u"Legend")[0]          #debe de existir el elemento de leyenda en layout llamado "Legend"

        titulo.text = titulo1.upper()               # Actualiza el título
        subtitulo.text = subtitulo1.upper()         # Actualiza el subtítulo
        tfecha.text = fecha                         # Actualiza la fecha
        leyenda.title = u"SIMBOLOGÍA"               # Asigna el rótulo a la simbología

        return u'Se han aplicado los cambios para ajustar el formato'
    
    except Exception as e:
        return u'>>>>>ERROR en formato_layout: {}'.format(e)

def carga_capa_y_formatea(valores):
    """
    Carga un archivo shapefile y le da formato
    lo renombra en base al valor definido en 'nombreshape'
    se debe definir un diccionario con los siguientes elementos:
    \nmxd = mapa a usar
    \ndf = dataframe a usar
    \nshapefile = shapefile a cargar (ruta completa)
    \nnombreshape = nombre para impresión de la capa en el dataframe (optativo)
    \nlayer = archivo layer para la simbología (ruta completa)
    \ntransparencia = transparencia de la capa (optativo)
    \ncampo_rotulos = campo para aplicar en los rótulos (si el valor = False entonces no se activan los rótulos en el mapa) (optativo)
    \nreturns: reporte de resultados de los procesos.
    """
    mensaje=""
    try:

        mxd = valores['mxd']
        df = valores['df']
        shapefile = valores['shapefile']
        nombreshape = valores['nombreshape']
        layer = valores['layer']
        transparencia = valores['transparencia']
        mensaje+=cargar_capa(mxd, df, shapefile) + ". "
        shp = os.path.basename(shapefile).split(".")[0]
        campo_rotulos = valores['campo_rotulos']

        mensaje="Reporte de 'carga_capa_y_formatea' para '{}': ".format(nombreshape)

        if transparencia != None:
            mensaje+=transp(mxd, df, shp, transparencia) + ". "
        aplica_simbologia(mxd, df, shp, layer)
        if campo_rotulos != None:
            mensaje+=activar_rotulos(mxd, df, shp, campo_rotulos) + ". "
        if nombreshape != None:
            mensaje+=renombra(mxd, shp, nombreshape) + ". "
        return mensaje
    except Exception as e:
        mensaje+='>>>>>ERROR en carga_capa_y_formatea: {}. '.format(e)
        return mensaje

def escala_en_diametro(mxd, df, capa, diametro):
    """
    Ajusta la escala de visualización del dataframe a un diámetro definido (en metros)
    """
    altodf = df.elementHeight       # Devuelve el valor (en centímetros) del alto del dataframe
    escala = (diametro * 100)/altodf
    df.scale = escala
    arcpy.RefreshActiveView

def acentos(texto):
    """
    Reemplaza letras acentuadas por letras sin acentos
    returns: el texto sin acentos
    """

    # Definir un diccionario de reemplazo para las vocales acentuadas
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }

    # Utilizar una expresión regular para buscar y reemplazar las vocales acentuadas
    patron = re.compile("|".join(re.escape(k) for k in reemplazos))
    sinacento = patron.sub(lambda m: reemplazos[m.group(0)], texto)

    return sinacento

def borrainn(mxd,df):
    """
    Borra todas las capas distintas a 'SISTEMA'
    """

    try:

        # elimina todas las capas, excepto "SISTEMA"

        capas_a_mantener = []

        # Iterar a través de todas las capas en el DataFrame
        for lyr in arcpy.mapping.ListLayers(mxd, u"", df):
            # Verificar si el nombre de la capa es "SISTEMA"
            if lyr.name == "SISTEMA":
                capas_a_mantener.append(lyr)  # Agregar la capa a la lista de capas a mantener

        # Eliminar todas las capas del DataFrame
        for lyr in arcpy.mapping.ListLayers(mxd, u"", df):
            if lyr not in capas_a_mantener:
                arcpy.mapping.RemoveLayer(df, lyr)
        return 'Se han borrado las capas innecesarias'
    
    except Exception as e:
        return '>>>>>ERROR en borrainn: {}'.format(e)

def tiempo(tiempos):
    """
    Regresa el tiempo
    """

    try:

        # Convertir cadenas de tiempo a objetos datetime
        tiempo_inicial = datetime.strptime(tiempos[0], "%Y-%m-%d %H:%M:%S")
        tiempo_final = datetime.strptime(tiempos[1], "%Y-%m-%d %H:%M:%S")

        # Calcular la diferencia de tiempo
        diferencia_tiempo = tiempo_final - tiempo_inicial
        return(diferencia_tiempo)

    except Exception as e:
        return '>>>>>ERROR en tiempo: {}'.format(e)

def obtener_codigo_epsg(archivo_shp):
    describe = arcpy.Describe(archivo_shp)
    try:
        codigo_epsg = int(describe.spatialReference.factoryCode)
        return codigo_epsg
    except AttributeError:
        return None

def fil_expr(mxd, capa, expr):     
    """
    Aplica un filtro al parámetro 'capa'
    Esta función acepta la cadena de expresión completa, ejemplo:---> "NOM_MUN = 'Jesús María' AND NOM_ENT = 'Aguascalientes'"
    """
    try:
        capa = arcpy.mapping.ListLayers(mxd, capa)[0]
        capa.definitionQuery = expr
        mensaje=u"Se ha aplicado el filtro '{}' a la capa '{}'".format(expr,capa)
    except Exception as e:
        mensaje=u">>>>>ERROR en 'fil_expr': {} {}".format(expr, e)
    finally:
        return mensaje

def clipbuffer(valores):
    """
    Genera un buffer con una distancia definida y posteriormente 
    realiza un clip

    Recibe un diccionario con los siguientes valores:\n
    \ncaparecortar= #capa que se va a recortar (ruta completa)
    \ndistbuffer= #radio del buffer
    \nbuffer_in= #capa de la que se genera el buffer
    \narchivoclip= #nombre del archivo resultado del clip (ruta completa)
    \nbuffer_arch= #nombre del archivo resultado del buffer  (ruta completa)
    \n
    \nreturns: cadena con los resultados de las operaciones
    """
    mensaje = "Proceso 'clipbuffer': "

    arcpy.env.overwriteOutput = True

    try:
        mensaje += "Inicio ... "
        caparecortar=valores['caparecortar']
        distbuffer=valores['distbuffer']
        buffer_in=valores["buffer_in"]
        archivoclip=valores["archivoclip"]
        buffer_arch=valores["buffer_arch"]

        def bufferproc():
            mensaje="Proceso buffer: "
            arcpy.Buffer_analysis(in_features=buffer_in,
                out_feature_class=buffer_arch, 
                buffer_distance_or_field= str(distbuffer) + " Meters",
                line_side="FULL",
                line_end_type="ROUND",
                dissolve_option="NONE",
                dissolve_field="",
                method="PLANAR")
            if os.path.exists(buffer_arch):
                mensaje += "Se ha creado el buffer. "
            else:
                mensaje += "Error creando el buffer. "
            return mensaje
        def clipproc():
            mensaje = ""
            arcpy.Clip_analysis(in_features=caparecortar, clip_features=buffer_arch,out_feature_class=archivoclip, cluster_tolerance="")
            nom = os.path.basename(archivoclip)
            if os.path.exists(archivoclip):
                mensaje += "Se ha creado el clip '{}'. ".format(nom)
            else:
                mensaje += "No se ha creado el clip '{}'. ".format(nom)
            return mensaje

        mensaje += bufferproc()
        mensaje += clipproc()
        mensaje += "Proceso clipbuffer terminado."
    except Exception as e:
        mensaje += ">>>>>ERROR en 'clipbuffer': -'{}-'. ".format(e)
    finally:
        return mensaje

def exporta_dwg(archivosalida, lista_arch):
    """
    Exporta archivos shapefile a un dwg
    \n archivosalida: ruta completa del archivo dwg
    \n arch_exp: lista de archivos shapefile que serán exportados al dwg
    \n returns: reporte de resultados
    """
    arcpy.env.overwriteOutput = True
    
    mensaje="Reporte de 'exporta_dwg' dwg: "
    try:
        mensaje += "Iniciando 'exporta_dwg'. "
        arcpy.ExportCAD_conversion(
            in_features=lista_arch,
            Output_Type="DWG_R2013",
            Output_File=archivosalida,
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File="")
        if os.path.exists(archivosalida):
            mensaje += "Se han exportado los archivos a {}. ".format(archivosalida)
        else:
            mensaje += "No se han exportado los archivos. "
    except Exception as e:
        mensaje+=">>>>>ERROR en 'exporta_dwg': {}".format(e)
    finally:
        return mensaje

def dwg(dbasicos):
    """
    Genera los archivos para el cuadro de construcción en formato dwg para autocad
    """
    arcpy.env.overwriteOutput = True
    valores={}
    arch_log=dbasicos['archivo_log']
    ambito=dbasicos['ambitourb']
    scince=dbasicos['rutascince2020']
    carpeta_proy=dbasicos['carpeta_proy']
    estado=dbasicos['estado']
    carpeta_temp = carpeta_proy + "temp/"
    archivodwg=carpeta_proy + "cuadro_de_localizacion.dwg"
    capasist="SISTEMA"

    mensaje="Reporte dwg; "
    mensaje += u"Carpeta temporal: "
    arch_exp=[]

    if not os.path.exists(carpeta_temp):
        os.makedirs(carpeta_temp)
        mensaje += u"Se creó la carpeta temporal. "
    else:
        mensaje += u"La carpeta temporal ya existe. "

    valores={
        "arch_log"      : arch_log,
        "ambito"        : ambito,
        "scince"        : scince,
        "carpeta_temp"  : carpeta_temp,
        "buffer_in"     : capasist
    }

    try:
        
        
        def ambito_urbano():
            mensaje = "Iniciando ambito_urbano 'dwg'"
            valores["caparecortar" ]=scince + "manzana_localidad.shp"
            distancias=[
                1500,
                1000,
                500,
                200
                ]
            for distancia in distancias:
                valores["distbuffer"]=distancia
                archivobuff = "{}buffer_{}.shp".format(carpeta_temp,distancia)
                archivoclip = "{}clip_{}.shp".format(carpeta_temp,distancia)
                valores["archivoclip"]=archivoclip
                valores["buffer_arch"]=archivobuff
                mensaje += clipbuffer(valores)
                if os.path.exists(archivoclip):
                    arch_exp.append(archivoclip)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
                else:
                    mensaje += ">>>>>ERROR en cuadro de localización -urbano, no se ha agregado '{}'".format(archivoclip)
            arch_exp.append(capasist)
            return arch_exp

        def ambito_rural():
            mensaje = "Iniciando ambito_rural 'dwg'"
            distancias = {
                2500,
                1500,
                1000,
            }
            arch_orig = {
                "Y:/GIS/MEXICO/VARIOS/INEGI/RED NACIONAL DE CAMINOS 2017/conjunto_de_datos/{0}/Caminos_RNC_{0}.shp".format(estado),
                "{}loc_urb.shp".format(scince),
                "{}loc_rur.shp".format(scince),
            }
            for distancia in distancias:
                archivobuff = "{}buffer_{}.shp".format(carpeta_temp,distancia)
                valores["buffer_arch"]=archivobuff
                valores["distbuffer"]=distancia
                for elemento in arch_orig:
                    valores["caparecortar" ]=elemento
                    nom=os.path.basename(elemento)
                    archivoclip = "{}clip_{}_{}".format(carpeta_temp,distancia,nom)
                    valores["archivoclip"]=archivoclip
                    mensaje += clipbuffer(valores)
                    if os.path.exists(archivoclip):
                        arch_exp.append(archivoclip)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
                    else:
                        mensaje += "Iniciando ambito_urbano 'dwg'"">>>>>ERROR en cuadro de localización -rural, no se ha agregado '{}'".format(archivoclip)
                if os.path.exists(archivobuff):
                    arch_exp.append(archivobuff)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
            arch_exp.append(capasist)
            return arch_exp

        if ambito == "Urbano":
            mensaje +="Iniciando libreria 'ambito urbano'"
            arch_exp=ambito_urbano()
        elif ambito == "Rural":
            mensaje +="Iniciando libreria 'ambito rural'"
            arch_exp=ambito_rural()
        else:
            mensaje +=">>>>>ERROR en cuadro de localización: no se ha definido 'ambito' adecuadamente"

        archivos = ';'.join(arch_exp)
        mensaje +=exporta_dwg(archivodwg, archivos)

    except Exception as e:
        mensaje=">>>>>ERROR en 'cuadro de localizacion' {}".format(e)
        

    finally:
        # ESU.log("Finalizando libreria 'dxf'",arch_log, imprimir=True)
        for arch in arch_exp:
                if arch != capasist:
                    arcpy.Delete_management(arch)
                    mensaje +="Se ha eliminado {}".format(arch)
        return mensaje

def scrapval(archivo,campos):
    """
    obtiene los valores de los campos definidos en 'campos'.
    \nparámetros:
    \narchivo: ruta completa del archivo a trabajar
    \ncampos: lista de los campos a buscar
    \nreturns: diccionario con los valores obtenidos
    \nnota: si no existe alguno de los campos proporcionados, informa que no existe.
    """
    resultados={}

    try:
        if not os.path.exists(archivo):
            return "El archivo '{}' no existe en disco".format(archivo)
        else:
            for campo in campos:    # crea un cursor para el primer registro
                cursor = arcpy.SearchCursor(archivo,[campo])
                for fila in cursor: # obtiene los valores del campo del cursor
                    valordecampo = fila.getValue(campo)
                    resultados[campo]=valordecampo
        return resultados
    
    except Exception as e:
        return ">>>>>ERROR en 'scrapval': {}".format(e)

def identidad(valores):
    """
    Crea un mapa de identidad de una capa con un punto 
    y genera un archivo de texto con los valores de campo deseados
    \nparámetros de la función:
    \ncapapunto: archivo de punto (ruta completa)
    \ncapaident: archivo con los datos a transferir a 'capapunto' (ruta completa)
    \ncarpeta_proy: 
    \camposidenti: diccionario con los campos de 'capaident' a recuperar
    \nreturns: diccionario con los campos requeridos y sus valores
    """
    capapunto=valores['capapunto']
    capaident=valores['capaident']
    camposidenti=valores['camposidenti']
    archsalida=os.path.basename(capaident).split(".")[0]
    carpeta_proy=valores['carpeta_proy']


    carpetatemp=carpeta_proy + 'temp/'
    if not os.path.exists(carpetatemp):
        os.makedirs(carpetatemp)
    capasalida=carpetatemp + archsalida + '.shp'

    arcpy.env.overwriteOutput = True

    arcpy.Identity_analysis(in_features=capapunto,
            identity_features=capaident,
            out_feature_class=capasalida,
            join_attributes="ALL",
            cluster_tolerance="",
            relationship="NO_RELATIONSHIPS")
    campos=[]
    for campo in camposidenti:
        campos.append(campo)

    res=""
    if os.path.exists(capasalida):
        res=scrapval(capasalida,campos)
        arcpy.Delete_management(capasalida)
    resultados="resultados en cero"
    if isinstance(res, dict):
        resultados={}
        for trad in camposidenti:
            parametro=camposidenti[trad]
            valor=res[trad]
            resultados[parametro]=valor
    else:
        resultados=res
    return resultados

def dist_lejana(shapefile,objeto_id):

# no funciona

    # Obtener la geometría del objeto
    with arcpy.da.SearchCursor(shapefile, ["SHAPE@"], '"ID" = {}'.format(objeto_id)) as cursor:
        for row in cursor:
            objeto_geom = row[0]
            # Calcular el centroide
            centroide = objeto_geom.centroid
            # Inicializar la distancia máxima
            max_distancia = -1
            # Inicializar el punto más lejano
            punto_mas_lejano = None
            # Calcular la distancia entre el centroide y cada vértice del objeto
            for punto in objeto_geom:
                distancia = centroide.distanceTo(punto)
                # Actualizar el punto más lejano si encontramos una distancia mayor
                if distancia > max_distancia:
                    max_distancia = distancia
                    punto_mas_lejano = punto

    # Imprimir las coordenadas del punto más lejano
    print("Coordenadas del punto más lejano:", punto_mas_lejano.X, punto_mas_lejano.Y)

def identidadclip(valores):
    """
    Crea un mapa de identidad de una capa con un punto 
    y genera un archivo de texto con los valores de campo deseados
    \nparámetros de la función:
    \ncapapunto: archivo de punto (ruta completa)
    \ncapaident: archivo con los datos a transferir a 'capapunto' (ruta completa)
    \ncarpeta_proy: 
    \camposidenti: diccionario con los campos de 'capaident' a recuperar
    \nreturns: diccionario con los campos requeridos y sus valores
    """
    try:

        import Utilerias_DBF
        reload(Utilerias_DBF)

        archlog=valores['archlog']

        capapunto=valores['capapunto']
        capaident=valores['capaident']
        camposidenti=valores['camposidenti']
        archsalida=os.path.basename(capaident).split(".")[0]
        nombreident=os.path.basename(capaident)
        
        carpeta_proy=valores['carpeta_proy']
        carpetatemp=carpeta_proy + 'temp/'
        archbuffer="{}buffer.shp".format(carpetatemp)
        capasalida=carpetatemp + archsalida + '.shp'
        capaclip=carpetatemp + "clip.shp"
        archivoscreados=[
            archbuffer,
            capasalida,
            capaclip,
            ]

        log(u"Reporte de librería 'identidadclip'".format(nombreident),archlog)

        if not os.path.exists(carpetatemp):
            log(u"No existe '{}', se creará".format(carpetatemp),archlog)
            os.makedirs(carpetatemp)
        else:
            log(u"Ya existe '{}', no se creará".format(carpetatemp),archlog)
        arcpy.env.overwriteOutput = True
        arcpy.Buffer_analysis(capapunto,archbuffer,"2 kilometers")
        if os.path.exists(archbuffer):
            log(u"Se ha creado el archivo '{}'".format(archbuffer),archlog)
            arcpy.Clip_analysis(capaident,archbuffer,capaclip)
            if os.path.exists(capaclip):
                log(u"Se ha creado el archivo '{}'".format(capaclip),archlog)
                arcpy.Identity_analysis(in_features=capapunto,
                        identity_features=capaclip,
                        out_feature_class=capasalida,
                        join_attributes="ALL",
                        cluster_tolerance="",
                        relationship="NO_RELATIONSHIPS")
                log(u"Se extraerá información del archivo '{}'".format(capasalida),archlog)
                capasalidadbf="{}/{}.dbf".format(os.path.dirname(capasalida),os.path.basename(capasalida).split(".")[0])
                log(u"Capa DBF '{}'".format(capasalidadbf),archlog)
                
                try:
                    camposidentific=[]
                    for campo in camposidenti:
                        camposidentific.append(campo)
                    log(u"Campos identificacion {}".format(camposidentific),archlog)
                    resultados=Utilerias_DBF.recuperacamposdbf(capasalidadbf,camposidentific)
                except Exception as e:
                    log(u"Error ejecutando librería 'recuperacamposdbf': {}".format(e),archlog)
                log(u"Resultados de proceso de extracción '{}'".format(resultados),archlog)
                if type(resultados) is dict:
                    log(u"Se ha ejecutado la librería 'identidadclip' satisfactoriamente",archlog)
                    return resultados
                else:
                    log(u">>>>>ERROR en la librería 'identidadclip', no se relizó el proceso de recuperar valores de campos.",archlog)
            else:
                return u">>>>>ERROR en la librería 'identidadclip', no se creó {}".format(capaclip)
        else:
            return u">>>>>ERROR en la librería 'identidadclip', no se creó {}".format(archbuffer)
    except Exception as e:
        log(u">>>>>ERROR en 'identidadclip': {}".format(e),archlog)
        pass

    finally:
        for archivocreado in archivoscreados:
            if os.path.exists(archivocreado):
                arcpy.Delete_management(archivocreado)
                log("se ha elimiado de disco: '{}'".format(archivocreado),archlog)
                log(u"Librería 'identidadclip' finalizada".format(nombreident),archlog)

def nearbuff(valores, rapido=False):
    """
    Analiza la relación de cercanía de los elementos de una capa
    con relación a un elemento de otra capa (archivobase)
    -es importante que 'archivobase' tenga un solo elemento-
    esta función no verifica lo anterior, por lo que si 'archivobase'
    contiene más de un elemento puede dar resultados inconsistentes. 
    La función regresa los 'n' elementos definidos en la variable
    'elementos' del diccionario.
    La función no altera el archivo original, crea un archivo temporal en una
    carpeta temporal. Al finalizar el proceso elimina el archivo temporal.
    Recibe un diccionario con las siguientes variables:
        elementos: entero que define la cantidad de elementos más cercanos a 'archivobase a recuperar. 
        archivobase: archivo shp (ruta completa) a analizar cercanía
        archivonear: archivo (ruta completa) con uno o más elementos de los cuales se desea conocer su cercanía con el único elemento de 'archivobase'.
        campo: cadena que indica el campo descriptivo de los valores 'near'
        carpeta_proy: carpeta del proyecto.
        returns: lista que contiene una lista de diccionarios con los primeros 'n' elementos más cercanos a 'archivobase' y una cadena con el reporte de resultados del proceso

    """
    try:
        
        arcpy.env.overwriteOutput = True

        archivobase = valores['archivobase']
        archivonear = valores['archivonear']
        elementos = valores['elementos']
        radiobuffer = valores['radiobuffer']
        campo = valores['campo']
        nombre = (os.path.basename(archivonear).split("."))[0]
        carp_temp = valores['carpeta_proy'] + "temp/"
        archlog = valores['archlog']
        archivodest = "{}{}_temp.shp".format(carp_temp, nombre)
        archbuffer = "{}{}_buffer.shp".format(carp_temp, nombre)
        resultados=[]

        log(u"Reporte de librería 'nearbuff' para {}:".format(os.path.basename(archivonear).split("."[0])), archlog)

        if not os.path.exists(carp_temp):
            os.makedirs(carp_temp)
            log(u"Se ha creado la carpeta temporal en la carpeta del proyecto.", archlog)
        else:
            log(u"Ya existe la carpeta temporal en la carpeta del proyecto.", archlog)
        if not os.path.exists(archivodest):
            arcpy.Buffer_analysis(archivobase,archbuffer,radiobuffer)
            arcpy.Clip_analysis(archivonear,archbuffer,archivodest)
            log(u"Se ha creado el archivo buffer.", archlog)
            arcpy.Near_analysis(archivodest, archivobase, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR")
            log("Se ejecutado 'near' en el archivo fuente.", archlog)
        else:
            log(u"Ya existe el archivo {} en la carpeta del proyecto.".format(archivodest), archlog)
            campos_en_archivo=arcpy.ListFields(archivodest)
            campobuscado="NEAR_DIST"
            for camp in campos_en_archivo:
                if camp.name == campobuscado:
                    siexiste=True
                    break
                else:
                    siexiste=False
                    pass
            if siexiste:
                log(u"Sí existe el campo {}".format(campobuscado), archlog)
            else:
                log(u"No existe el campo", archlog)
                arcpy.Near_analysis(archivodest, archivobase, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR")
                log(u"Se ha ejecutado near en el archivo copiado. ", archlog,presalto=1)
            
        lista=[]
        with arcpy.da.SearchCursor(archivodest, ["NEAR_DIST",campo ,"FID"]) as cursor:
            for row in cursor:
                valor_campo0 = row[0]
                valor_campo1 = row[1]
                valor_campo2 = row[2]
                lista.append({"nombre":str(valor_campo2) + "_" + valor_campo1, "distancia": valor_campo0})
        
        lista_ordenada=sorted(lista,key=lambda x: x["distancia"])
        resultados=[lista_ordenada[:elementos]]

    except Exception as e:
        # traza_de_pila = traceback.extract_tb(e.__traceback__)
        # # Obtener el número de línea del primer marco de la pila
        # numero_de_linea = traza_de_pila[-1].lineno
        log(u">>>>>ERROR en arcpy.near: {}, numero de línea {}.".format(e), archlog)
    finally:
        if rapido==False:
            archivoborr=[
                archivodest,
                archbuffer,
            ]
            for archborr in archivoborr:
                if os.path.exists(archborr):
                    arcpy.Delete_management(archborr)
                    log(u"Se ha eliminado el archivo temporal '{}'.".format(archborr), archlog)
                else:
                    log(u">>>>>ERROR en 'nearbuff', no se ha creado el archivo '{}'.".format(archborr), archlog)
                if os.path.exists(archborr):
                    log(u">>>>>ERROR en 'nearbuff', no se ha borrado el archivo.'{}'".format(archborr), archlog)
                else:
                    log(u"Borrado verificado del archivo.'{}'".format(archborr), archlog)
        else:
            log(u"No se ha eliminado el archivo temporal.", archlog)
        log(u"Librería 'near' finalizada.", archlog)

        return resultados

def clipparamapa(carpeta_proy,capa_a_cargar,radio):

    try:
        arcpy.env.overwriteOutput = True  # Permitir sobrescribir archivos de salida
        radio= int(radio*3)
        carpeta_temp=carpeta_proy + "temp/"
        if not os.path.exists(carpeta_temp):
            os.makedirs(carpeta_temp)
        archjson=carpeta_proy + "datos_basicos.json"
        datosbasicos=lodicson(archjson)
        archsistema=datosbasicos['archsistema']
        archbuff=os.path.basename(capa_a_cargar).split(".")[0]
        buffer=carpeta_temp + "buffer_{}.shp".format(int(radio))
        archivo_clip="{}{}_{}.shp".format(carpeta_temp,archbuff,radio)

        print(archsistema,buffer,radio)

        arcpy.Buffer_analysis(
            in_features=archsistema,
            out_feature_class=buffer, 
            buffer_distance_or_field= str(radio) + " Meters",
            line_side="FULL",
            line_end_type="ROUND",
            dissolve_option="NONE",
            dissolve_field="",
            method="PLANAR")
        
        print(capa_a_cargar,archivo_clip,)
        
        if os.path.exists(buffer):
            arcpy.Clip_analysis(
                in_features=capa_a_cargar,
                clip_features=buffer,
                out_feature_class=archivo_clip,
                cluster_tolerance="")
            if os.path.exists(archivo_clip):
                arcpy.Delete_management(buffer)
                print("ejecutado " * 10)
                print(archivo_clip)
                return archivo_clip
            else:
                mensaje= u'No se realizó el clip.'
        else:
            mensaje= u'No se realizó el buffer.'
    except Exception as e:
        return u'>>>>>ERROR: {}----> {}'.format(mensaje,e)

def listacercanos(valores):
    """
    Regresa una lista con el valor 'FID' de los elementos dentro del radio de búsqueda definido
    parámetros:
    valores:    diccionario de valores que debe contener:
        capabase:   capa base, generalmente llamada "SISTEMA"
        capanear:   Capa de la cual se desea saber su distancia al sistema.
        radio:      Radio de búsqueda
        carp_tmp:   Carpeta del proyecto para los archivos temporales
        archlog:    Archivo log

    returns:    Lista de elementos o mensaje de error.
    """

    print(valores)

    capabase=valores['capabase']
    capanear=valores['capanear']
    radio=valores['radio']
    carp_tmp=valores['carp_tmp']
    arch_tmp=carp_tmp + "denue_near_tmp.dbf"
    # log("Iniciando 'listacercanos'...")
    if not os.path.exists(carp_tmp):
        os.makedirs(carp_tmp)

    'arcpy.GenerateNearTable_analysis(in_features="Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/Aguascalientes/conjunto_de_datos/denue_wgs84z13.shp", near_features="SISTEMA", out_table="C:/Users/Gustavo/Documents/ArcGIS/Default.gdb/denue_wgs84z13_GenerateNearT", search_radius="1000 Meters", location="LOCATION", angle="ANGLE", closest="CLOSEST", closest_count="0", method="PLANAR")'
    arcpy.GenerateNearTable_analysis(
        in_features=capanear,
        near_features=capabase,
        out_table=arch_tmp,
        search_radius="{} Meters".format(str(radio)),
        location="LOCATION",
        angle="ANGLE",
        closest="CLOSEST",
        closest_count="0",
        method="PLANAR"
        )
    import Utilerias_DBF as dbf
    reload(dbf)

    






if __name__=='__main__': # 

    # shapefile="Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/temp/USO DE SUELO INEGI SERIE IV_temp.shp"
    # objeto_id=62361
    # dist_lejana(shapefile,objeto_id)
    valores={
        "capabase"  :"Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp",
        "capanear"  :"Y:/GIS/MEXICO/VARIOS/INEGI/DENUE/2023/Aguascalientes/conjunto_de_datos/denue_wgs84z13.shp",
        "radio"     :1000,
        "carp_tmp"  :"Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/temp/",
        "arch_tmp"  :"Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/temp/denue_near_tmp.dbf",
    }

    listacercanos(valores)
    pass