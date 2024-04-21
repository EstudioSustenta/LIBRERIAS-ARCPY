# -*- coding: utf-8 -*-

"""
Librería para crear mapas temáticos.
"""

import os
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
reload(ESU)
import UTILERIAS.Utilerias_shp as USH
reload(USH)
from UTILERIAS.UTIL_JSON import agdicson
import arcpy
from ESUSTENTA_UTILERIAS import log


def proceso_identi(valoresclip,creajson):
    """
    Función para identificar los valores de una capa en base a una sobreposición de un archivo shp de puntos con un solo elemento.

    parámetros:
          valoresclip: diccionario de valores para la ejecución del proceso de identidad:
                capapunto: archivo de punto (ruta completa)
                capaident: archivo con los datos a transferir a 'capapunto' (ruta completa)
                carpeta_proy: carpeta del proyecto
                camposidenti: diccionario con los campos de 'capaident' a recuperar

    creajson: Booleano, verdadero se se va a generar un archivo json con los resultados del proceso de identidad
    
    returns: mensaje con los resultados del proceso de sobreposición de las capas.
    """
    try:
        archlog=valoresclip['archlog']
        log(u"Reporte de 'proceso_identi'...",archlog,presalto=2)
        shp = valoresclip['capaident']
        camposidenti=valoresclip['camposidenti']

        # Obtener la descripción del shapefile
        desc = arcpy.Describe(shp)

        # Obtener el tipo de geometría
        tipo_geometria = desc.shapeType

        log(u"Tipo de geometría del archivo 'ident'={}".format(tipo_geometria),archlog)
        if tipo_geometria == "Polygon":
            idres=USH.identidadclip(valoresclip)
            if isinstance(idres, dict):
                log(u"Se ha realizado 'identidad'. ",archlog)
                log(u"el valor creajson es {}.".format(creajson),archlog)
                if creajson==True:
                    log(u"Se creará un archivo .txt",archlog)
                    carpeta_proy=(valoresclip['carpeta_proy'])
                    carpeta_jsons=carpeta_proy + 'jsons/'
                    if not os.path.exists(carpeta_jsons):
                        os.makedirs(carpeta_jsons)
                        log(u"Se ha creado la carpeta 'jsons'. ",archlog)
                    else:
                        log(u"Ya existe la carpeta 'jsons'. ",archlog)
                    nombrejson=os.path.basename(valoresclip['capaident']).split(".")[0]
                    archivo=carpeta_jsons + nombrejson + "_identi.json"
                    agdicson(archivo,"PROYECTO",valoresclip['proyecto'])
                    for dato in idres:
                        clave=camposidenti[dato]
                        valor=idres[dato]
                        if valor=="" or valor=="0"or valor=="0.0":
                            valor="Fuera de zona de analisis"
                        
                        agdicson(archivo,clave,valor)
                    log(u"Se ha creado el archivo {}. ".format(archivo),archlog)
                else:
                    log(u"No se ha creado el archivo .txt para 'ident'",archlog)
            else:
                log(idres + ". ",archlog)
        else:
            log(u"No se puede procesar {} porque no es geometría de polígonos. ".format(shp),archlog)
    except Exception as e:
        # traza_de_pila = traceback.extract_tb(e.__traceback__)
        # # Obtener el número de línea del primer marco de la pila
        # numero_de_linea = traza_de_pila[-1].lineno
        log(u">>>>>ERROR en 'proceso_identi': {}, en línea '' ".format(e),archlog)
    finally:
        log(u"Proceso 'proceso_identi' finalizado.",archlog)
        return "'proceso_identi' ejecutado"

def proceso_near(valoresnear,creajson):
    """
    Función para identificar las distancias de una capa de punto 
    a los elementos de otra capa.
    parámetros:
    valoresnear: Diccionario con los valores para la ejecución de la identidad.
      elementos: entero que define la cantidad de elementos más cercanos a 'archivobase a recuperar. 
      archivobase: archivo shp (ruta completa) a analizar cercanía
      archivonear: archivo (ruta completa) con uno o más elementos de los cuales se desea conocer su cercanía con el único elemento de 'archivobase'.
      carpeta_proy: carpeta del proyecto.
    
    creajson: valor booleano; verdadero=se crea un archivo json con los resultados del análisis 'near' en una subcarpeta
    
    returns: lista con la distancia del elemento más lejano y una cadena con los resultados del proceso de análisis de cercanía
    """
    import codecs
    try:
        # os.environ["PYTHONIOENCODING"] = "utf-8"
        archlog=valoresnear['archlog']
        log(u"Reporte de 'proceso_near':", archlog,presalto=2)
        archivonear=valoresnear['archivonear']
        carpeta_proy=valoresnear['carpeta_proy']
        datos = USH.nearbuff(valoresnear, rapido=False) # el parámetro 'rapido' no está funcionando correctamente
        lista1=datos[0]
        log(u"tipo recuperado de nearbuff: '{}'".format(type(lista1)),archlog)
        if type(lista1) is list:
            log(u"Se ha recibido una lista de la librería 'near', proceso correcto.",archlog)
            log(u"Valores de la lista: {}".format(lista1),archlog)
            if creajson==True:
                log(u"Se creará un archivo .json.",archlog)
                carpetajson=carpeta_proy + "jsons/"
                if not os.path.exists(carpetajson):
                    log(u"La carpeta {} no existe, se creará".format(carpetajson),archlog)
                    os.makedirs(carpetajson)
                else:
                    log(u"La carpeta {} ya existe".format(carpetajson),archlog)
                
                archivo=u"{}{}_near.txt".format(carpetajson, os.path.basename(archivonear).split(".")[0])
                
                distancias=[]
                texto=""
                for elemento in lista1:
                    nombre=elemento['nombre']
                    dis=elemento['distancia']
                    distancias.append(dis)
                    texto+=u"{}\t{}\n".format(nombre,dis)
                with codecs.open(archivo, "w", encoding='utf-8') as archivotexto:
                    archivotexto.write(texto)
                    archivotexto.close()
                if os.path.exists(archivo):
                    log(u"Se ha creado el archivo .txt '{}'.".format(archivo),archlog)
                else:
                    log(u"No se ha creado el archivo .txt '{}'.".format(archivo),archlog)
            distmax=max(distancias)
            return [distmax]
        else:
            log(u"El objeto es {}".format(type(lista1)),archlog)
    except Exception as e:
        # traza_de_pila = traceback.extract_tb(e.__traceback__)
        # # Obtener el número de línea del primer marco de la pila
        # numero_de_linea = traza_de_pila[-1].lineno
        log(u">>>>>ERROR en 'proceso_near', no se ha ejecutado adecuadamente la librería 'near'. {}.".format(e),archlog)
        log(u">>>>>ERROR en 'proceso_near', no se ha ejecutado adecuadamente la librería 'near'. {}.".format(e.args),archlog)
        log(u">>>>>ERROR en 'proceso_near', no se ha ejecutado adecuadamente la librería 'near'. {}.".format(e.__str__()),archlog)
        log(u">>>>>ERROR en 'proceso_near', no se ha ejecutado adecuadamente la librería 'near'. {}.".format(e.__class__),archlog)
        log(u">>>>>ERROR en 'proceso_near', no se ha ejecutado adecuadamente la librería 'near'. {}.".format(e.__doc__),archlog)
        return e

    finally:
        log(u"proceso 'proceso_near' finalizado.",archlog)

def proceso_prepa(valprocesofin,capas_a_cargar):
    """
    Función para integrar los procesos finales para la creación de mapas temáticos.
    \nparámetros:
    \nmxd : Objeto mapa
    \ndf :  Objeto data frame
    \ntitulomapa :  título del mapa
    \nsubtitulomapa:
    \ncapazoom :
    \nradio :
    \nescala :
    \nsistema :
    \ncarpeta_proy: 
    \narchsalida: 
    """
    mxd=valprocesofin['mxd']
    df=valprocesofin['df']
    titulomapa=valprocesofin['titulomapa']
    subtitulomapa=valprocesofin['subtitulomapa']
    capazoom=valprocesofin['capazoom']
    radio=valprocesofin['radio']
    escala=valprocesofin['escala']
    sistema=valprocesofin['sistema']
    carpeta_proy=valprocesofin['carpeta_proy']
    archsalida=valprocesofin['archsalida']
    archlog=valprocesofin['archlog']

    log(u"Reporte de 'proceso_prepa'... ",archlog,presalto=1)
    elementos=len(capas_a_cargar)
    capabase=capas_a_cargar[elementos - 1]
    archivo=capabase['shapefile']
    carpeta=os.path.dirname(archivo)
    basedbf=os.path.basename(archivo).split(".")[0]
    archivodbf="{}/{}.dbf".format(carpeta,basedbf)

    #============================================
    log("resultado " * 5,archlog,presalto=1)
    resultado=""
    try:
        from Utilerias_DBF import cant_de_registros
        registros=cant_de_registros(archivodbf)
        log(u"Registros en archivo '{}': {}".format(archivodbf,registros),archlog)
        if registros > 15:
            resultado=USH.clipparamapa(carpeta_proy,archivo,radio)    #resultado es la ruta nueva del archivo shapefile recortado
            print("Resultado de clipparamapa: {}".format(resultado))
            if "ERROR" in resultado:
                log(resultado,archlog)
            else:
                capabase['shapefile']=resultado
                log("Se ha cambiado la ruta del archivo base a {}".format(resultado),archlog)
    except Exception as e:
        log(">>>>>ERROR en clippmapa: ".format(e),archlog,postsalto=2)
    log("resultado " * 5,archlog,postsalto=1)
    #============================================

    for capa_a_cargar in capas_a_cargar:
        log(USH.carga_capa_y_formatea(capa_a_cargar),archlog)
        if capa_a_cargar['nombreshape']=='Caminos':
            expr=u"""("TIPO_VIAL" = 'Avenida' OR "TIPO_VIAL" = 'Boulevard' OR "TIPO_VIAL" = 'Carretera')"""
            capa=capa_a_cargar['nombreshape']
            USH.fil_expr(mxd,capa,expr)
            log(u"se ha aplicado el filtro a la capa {}".format(capa),archlog)

    log(USH.formato_layout(mxd, titulomapa,subtitulomapa),archlog)
    log(USH.zoom_extent(mxd,df,capazoom),archlog)
    if radio != None:
        USH.escala_en_diametro(mxd,df,sistema,radio * 3)
    if escala != None:
        df.scale=escala
    log(USH.exportar(mxd,carpeta_proy,archsalida,serial=True),archlog)
    log(USH.elimina_shp(resultado),archlog)
    log(u"'proceso_prepa' finalizado.",archlog,presalto=1)

    return "Se ha ejecutado proceso final."

def proc_integra(diccionariosnear,diccionariosidenti,valprocesofin,capas_a_cargar,creajson):
    """
    Función integradora de proceso para creación de mapas.
    """

    try:
        valoresnear=diccionariosnear[0]
        archlog=valoresnear['archlog']
        mapa=valprocesofin['subtitulomapa']
        radios=[]
        for diccionarionear in diccionariosnear:
            resnear=proceso_near(diccionarionear,creajson=True)
            log(type(resnear),archlog,tabuladores=3)
            if type(resnear[0]) is float or type(resnear[0]) is int:
                radios.append(resnear[0])
            else:
                log(resnear,archlog)
                radios.append(20000)     # activar esta línea si se desea visualizar el mapa con otro radio distinto al obtenido en el proceso 'near'
        radio=sum(radios) / len(radios)
        log(u"Distancia para radio de zoom: '{}'. ".format(radio),archlog)
        valprocesofin['radio']=radio

        for valoresidenti in diccionariosidenti:
            log(proceso_identi(valoresidenti, creajson),archlog)
        log(proceso_prepa(valprocesofin,capas_a_cargar),archlog)
        return u"Proceso '{}' terminado satisfactoriamente.".format(mapa)
        
    except Exception as e:
        mensaje=u">>>>>ERROR en 'proc_integra' para {}: {}.".format(mapa,e)
        log(mensaje,archlog)
        return mensaje
    finally:
        log(USH.borrainn(valprocesofin['mxd'],valprocesofin['df']),archlog)
        
