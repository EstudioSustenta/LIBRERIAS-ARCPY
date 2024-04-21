# -*- coding: utf-8 -*-

# ----RUTINA PARA GENERAR MAPAS CON DATOS DE LA CONABIO
# RUTA DE LOS MAPAS:    Y:/GIS/MEXICO/VARIOS/conabio/WGS84

import arcpy
import importlib
import sys
import datetime


# Agrega la ruta del paquete al path de Python
ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

mxd = arcpy.env.mxd
df = arcpy.env.df

arcpy.env.overwriteOutput = True

global log
global idproy
global nearexp
global cliptema
global tiempo
global borrainn

#------------------------------> CARGA DE LIBRERÍAS <------------------------------------------

log = importlib.import_module(u"LIBRERIA.archivo_log")
idproy = importlib.import_module(u"LIBRERIA.identity_sistema")
nearexp = importlib.import_module(u"LIBRERIA.near_a_sistema")
cliptema = importlib.import_module(u"LIBRERIA.clip_tematico")
tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")
borrainn = importlib.import_module(u"LIBRERIA.borrainn")

reload(log)
reload(idproy)
reload(nearexp)
reload(cliptema)
reload(tiempo)
reload(borrainn)


#-----------------------------------------------------------------------------------------------
#------------------------------------> INICIO DE PROCESOS <-------------------------------------
#-----------------------------------------------------------------------------------------------


def area_nat_protegida(nummapa):

    #-----------------> AREA NATURAL PROTEGIDA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    

    log.log(repet,u"Proceso 'Areas naturales protegidas' iniciando...")

        # tabla

    rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar (sin el slash final)
    capaCl = u"Areas naturales protegidas.shp" # archivo a identificar
    capa_salida = u"Areas naturales protegidas" # capa a crear en el mapa
    camposCons =  [u"NOMBRE", u"TIPO", u"CATEGORIA", u"FUENTE", u"SUP_DEC2", u"ESTADO"] # campos a escribir en el archivo identity
    dAlter =  [u"NOMBRE", u"TIPO", u"CATEGORÍA", u"FUENTE", u"SUPERFICIE DECRETADA", u"ESTADO"] # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas =  [u"Areas naturales protegidas"]
    rutas = [rutaCl]
    ncampo = [camposCons[0]]                          # campo para el rótulo
    tit = capa_salida                           # título del mapa en el layout

    try:

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'area_nat_protegida'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'Areas naturales protegidas' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1



def clima_koppen(nummapa):

    #-----------------> CLIMA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Climas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Climas.shp" # archivo a identificar
        capa_salida = u"Climas" # capa a crear en el mapa
        camposCons =  [u"CLIMA_TIPO", u"DES_TEM", u"DESC_PREC"] # campos a escribir en el archivo identity
        dAlter =  [u"CLIMA KOPPEN", u"DESCRIPCIÓN TEMPERATURA", u"DESCRIPCIÓN PRECIPITACIÓN"] # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Climas"]
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                          # campo para el rótulo
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'clima_koppen'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()
    
    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Clima' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1



def clima_olgyay(nummapa):

    #-----------------> CLIMA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Clima Olgyay' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/00 PROPIOS/CLIMA" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"MEXICO_OLGYAY.shp" # archivo a identificar
        capa_salida = u"Climas Olgyay" # capa a crear en el mapa
        camposCons =  [u"CLIMA"] # campos a escribir en el archivo identity
        dAlter =  [u"CLIMA OLGYAY"] # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"MEXICO_OLGYAY"]
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                          # campo para el rótulo
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 2                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"nacional"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'clima_olgyay'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Clima Olgyay' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1


def cuenca(nummapa):

    #-----------------> CUENCA HIDROLOGICA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Cuenca hidrologica' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                       # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Cuenca hidrologica.shp"                                   # archivo a identificar
        capa_salida = u"Cuenca hidrologica"                                  # capa a crear en el mapa
        camposCons =  [u"CUENCA", u"REGION"]  # campos a escribir en el archivo identity
        dAlter =  [u"CUENCA", u"REGION"]     # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Cuenca hidrologica"]
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"nacional"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'cuenca'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()
    
    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Cuenca hidrologica' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1


def edafologia(nummapa):

    #-----------------> EDAFOLOGIA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    capa_salida = u"Edafologia" 
    tit = capa_salida                           # título del mapa en el layout
    

    try:

        log.log(repet,u"Proceso 'Edafologia' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Edafologia.shp"                                                       # archivo a identificar
        capa_salida = u"Edafologia"                                                      # capa a crear en el mapa
        camposCons =  [u"DESCRIPCIO",u"SUE1",u"DESC_TEX",u"DESC_FASFI",u"DESC_FAQUI"]     # campos a escribir en el archivo identity
        dAlter =  [u"DESCRIPCION",u"CLAVE EDAFOLÓGICA",u"TEXTURA",u"FASE FÍSICA",u"FASE QUÍMICA"]    # descriptores para los campos en el archivo identity de salida
        tit = capa_salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Edafologia"]                      #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                          # campo para el rótulo de los features en el mapa
        

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'edafologia'")
        log.log(repet,str(e) + u"\n\n\n\n")
        print(u"\n\n>> ERROR, no se pudo ejecutar 'edafologia'")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Edafologia' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1


def humedad(nummapa):

    #-----------------> HUMEDAD DEL SUELO <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Humedad del suelo' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Humedad del suelo.shp"                                                # archivo a identificar
        capa_salida = u"Humedad del suelo"                                               # capa a crear en el mapa
        camposCons =  [u"TIPO"]                                                           # campos a escribir en el archivo identity
        dAlter =  [u"Tipo de humedad en suelo"]                                           # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Humedad del suelo"]               #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'humedad'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Humedad del suelo' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1


def precip(nummapa):

    #-----------------> PRECIPITACION ISOYETAS <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Precipitacion' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Precipitacion.shp"                                           # archivo a identificar
        capa_salida = u"Precipitación"                                          # capa a crear en el mapa
        camposCons =  [u"PRECI_RANG"]                                                     # campos a escribir en el archivo identity
        dAlter =  [u"Rango de precipitacion (l/m2)"]                                      # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Precipitacion"]          #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'precip'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Precipitacion' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1


def subcuenca(nummapa):

    #-----------------> SUBCUENCA HIDROLÓGICA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Subcuencas hidrologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Subcuencas hidrologicas.shp"                                          # archivo a identificar
        capa_salida = u"Subcuencas hidrólgicas"                                          # capa a crear en el mapa
        camposCons =  [u"NOMBRE", u"DESCRIPCI", u"TIPO"]                                    # campos a escribir en el archivo identity
        dAlter =  [u"NOMBRE", u"DESCRIPCIÓN", u"TIPO"]                                      # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Subcuencas hidrologicas"]         #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'subcuenca'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Subcuencas hidrologicas' finalizado! \n\n") 

    arcpy.env.repet = arcpy.env.repet - 1


def subregion(nummapa):

    #-----------------> SUBREGIÓN HIDROLÓGICA <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Subregiones hidrologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Subregiones hidrologicas.shp"                                         # archivo a identificar
        capa_salida = u"Subregiones hidrólgicas"                                         # capa a crear en el mapa
        camposCons =  [u"NOMBRE"]                                    # campos a escribir en el archivo identity
        dAlter =  [u"NOMBRE"]                                      # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas = [u"Subregiones hidrologicas"]        #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'subregion'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Subregiones hidrologicas' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1



def zonaecol(nummapa):

    #-----------------> ZONAS ECOLÓGICAS <------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Zonas ecologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"               # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Zonas ecologicas.shp"                             # archivo a identificar
        capa_salida = u"Zonas ecologicas"                            # capa a crear en el mapa
        camposCons = [u"NOMZONECOL", u"TIPO_ZONA"]                    # campos a escribir en el archivo identity
        dAlter = [u"ZONA ECOLOGICA", u"TIPO"]                                 # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas = [u"Zonas ecologicas"]                #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                         # campo para el rótulo de los features en el mapa
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 10                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'zonaecol'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"'Zonas ecologicas' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1



