# -*- coding: utf-8 -*-

# ----RUTINA PARA IMPRIMIR MAPAS DE UBICACIÓN A NIVEL PAIS, ESTADO, MUNICIPIO, REGIÓN, ZONA Y SITIO

import arcpy
import sys
import importlib
import codecs
import datetime

# arcpy.env.addOutputsToMap = "CURRENT"

# Proceso para inicializar cuadros de diálogo
import Tkinter as tk
import tkFileDialog
root = tk.Tk()
root.withdraw()

# Agrega la ruta del paquete al path de Python

ruta_libreria = "Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

arcpy.env.mxd = arcpy.mapping.MapDocument("CURRENT")                    # Obtener acceso al documento actual
mxd = arcpy.env.mxd
arcpy.env.df = arcpy.mapping.ListDataFrames(mxd)[0]
df = arcpy.env.df
arcpy.env.layout = "Layout"

# Importar el módulo desde el paquete LIBRERIA utilizando importlib
dbas = importlib.import_module("LIBRERIA.datos_basicos")
log = importlib.import_module("LIBRERIA.archivo_log")


def rutacarp():

    # Abre un cuadro de diálogo para seleccionar una carpeta
    carp_mapas = "Y:/02 CLIENTES (EEX-CLI)/(2001-0001) FAMILIA MARTINEZ DEL RIO/(2008-PIN-0005) CASA BUENAVISTA/SIG"
    carpeta_cliente = tkFileDialog.askdirectory(initialdir=carp_mapas, title="Selecciona la carpeta destino de los mapas") + "/"
    arcpy.env.carp_cliente = carpeta_cliente
    # Verifica si el usuario seleccionó una carpeta
    if carpeta_cliente:
        log.log(u"Ruta de la carpeta seleccionada: %s" % carpeta_cliente)
    else:
        print(u"No se seleccionó ninguna carpeta.")
        log.log(u"No se seleccionó ninguna carpeta.")
    

# Preliminares
def db():

    dbas.datosbasicos() # define los datos básicos del proyecto y crea el archivo txt correspondiente
    log.log(u"\n\n\n")
    log.log(u"--------------INICIO DE SECCIÓN LOG \--------------------------")
    log.log(u"\n")
    log.log(u"Proceso 'datos básicos' iniciando...")
    log.log(u"Proceso 'datos básicos' finalizado! \n\n")

def cargalib():

    log.log(u"Proceso 'cargalib' iniciando...")

    global ccapas
    global ctrlcapa
    global ctrlgrup
    global exportma
    global filtro
    global formato
    global simbologia
    global z_extent
    global act_rot
    global buff_cl
    global transp
    global renombra
    global urbano
    global rural
    global dwgs
    global servicios
    global cliptema
    global idproy
    global nearexp
    global log
    global leyenda

    ccapas = importlib.import_module("LIBRERIA.cargar_capas")               #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
    ctrlcapa = importlib.import_module("LIBRERIA.control_de_capa")          #carga el script de control de capas  -----> funciones: apagacapa(capa_a_apagar), encendercapa(capa_a_encender)
    ctrlgrup = importlib.import_module("LIBRERIA.control_de_grupo")         #carga el script de control de grupos
    exportma = importlib.import_module("LIBRERIA.exportar_mapas")           #carga el script para exportar mapas a pdf y jpg
    filtro = importlib.import_module("LIBRERIA.filtro")                     #carga el script para aplicar filtros a una capa
    formato = importlib.import_module("LIBRERIA.formato")                   #carga el script para aplicar formato a layout
    simbologia = importlib.import_module("LIBRERIA.simbologia_lyr")         #carga el script para aplicar simbología a capas
    z_extent = importlib.import_module("LIBRERIA.zoom_extent")              #carga el script para aplicar zoom extent a una capa 
    act_rot = importlib.import_module("LIBRERIA.activa_rotulos")            #carga el script para activar y desactivar los rótulos de una capa  -----> funciones: 
    buff_cl = importlib.import_module("LIBRERIA.buffer_clip")               #carga el script para activar y desactivar los rótulos de una capa  -----> funciones: clip(ruta, radio)
    transp = importlib.import_module("LIBRERIA.aplica_transparencia")       #carga el script para aplicar transparencia a capas
    renombra = importlib.import_module("LIBRERIA.renombrar_capa")           #carga el script para cambiar el nombre a capas
    urbano = importlib.import_module("LIBRERIA.urbano_nacional")            # ejecuta rutina de zonas urbanas
    rural = importlib.import_module("LIBRERIA.rural_nacional")              # ejecuta rutina de zonas rurales
    dwgs = importlib.import_module("LIBRERIA.cuadro_de_localizacion")
    servicios = importlib.import_module("LIBRERIA.servicios")
    cliptema = importlib.import_module("LIBRERIA.clip_tematico")
    idproy = importlib.import_module("LIBRERIA.identity_sistema")
    nearexp = importlib.import_module("LIBRERIA.near_a_sistema")
    log = importlib.import_module("LIBRERIA.archivo_log")
    leyenda = importlib.import_module("LIBRERIA.leyenda_ajuste")
    
    
    
    reload(ctrlcapa)
    reload(ctrlgrup)
    reload(exportma)
    reload(filtro)
    reload(formato)
    reload(simbologia)
    reload(z_extent)
    reload(act_rot)
    reload(buff_cl)
    reload(transp)
    reload(renombra)
    reload(urbano)
    reload(rural)
    reload(dwgs)
    reload(servicios)
    reload(cliptema)
    reload(idproy)
    reload(nearexp)
    reload(log)
    reload(leyenda)

    ccapas.carga_capas("Y:/0_SIG_PROCESO/00 GENERAL", "SISTEMA")
    simbologia.aplica_simb("SISTEMA")
    transp.transp("SISTEMA",50)
    z_extent.zoom_extent(arcpy.env.layout, "SISTEMA")

    #formato.formato_layout("Preparacion")

    log.log(u"Proceso 'cargalib' finalizado! \n\n")

    # nota, para poder cargar las librería y que se genere el archivo .pyc adecuadamente, cada librería debe iniciar con la línea: # -*- coding: utf-8 -*-


# -------------------------------------------------------------------------------


def borrainn():

    log.log(u"iniciando proceso de borrado capas innecesarias...")

    # elimina todas las capas, excepto "SISTEMA"

    capas_a_mantener = []

    # Iterar a través de todas las capas en el DataFrame
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        # Verificar si el nombre de la capa es "SISTEMA"
        if lyr.name == "SISTEMA":
            capas_a_mantener.append(lyr)  # Agregar la capa a la lista de capas a mantener

    # Eliminar todas las capas del DataFrame
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        if lyr not in capas_a_mantener:
            arcpy.mapping.RemoveLayer(df, lyr)
            log.log(u"Removiendo capa " + str(lyr))

    # Actualizar el contenido del DataFrame
    arcpy.RefreshTOC()
    log.log(u"Proceso de borrado capas innecesarias finalizado! \n\n")



def mapaPais(nummapa):

    log.log(u"Proceso 'mapaPais' iniciando...")

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa a nivel pais
    
    nombre_capa = "ESTATAL decr185"
    ruta_arch = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
    ccapas.carga_capas(ruta_arch, nombre_capa)
    act_rot.activar_rotulos(nombre_capa,"NOM_ENT")
    z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    formato.formato_layout("UBICACIÓN A NIVEL PAÍS")
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " pais"
    nnomb = u"Entidades Federativas"
    renombra.renomb(nombre_capa, nnomb)
    exportma.exportar(r_dest)
    ccapas.remover_capas(nnomb)
    arcpy.env.nummapa = nummapa + 1
    log.log(u"Proceso 'mapaPais' finalizado! \n\n")

def mapaEstatal(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa estatal

    log.log(u"Proceso 'mapaEstatal' iniciando...")

    nombre_capa = "MUNICIPAL CENSO 2020 DECRETO 185"
    ruta_arch = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"
    ruta_arch1 = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + "/cartografia"
    nombre_capa1 = "manzana_localidad"
    campo = "NOM_ENT"
    ccapas.carga_capas(ruta_arch, nombre_capa)
    filtro.aplicar_defq(nombre_capa, campo, "'" + arcpy.env.estado + "'")
    z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
    simbologia.aplica_simb(nombre_capa)
    formato.formato_layout("UBICACIÓN A NIVEL ESTADO")
    act_rot.activar_rotulos(nombre_capa,"NOM_MUN")
    ccapas.carga_capas(ruta_arch1, "red nacional de caminos")
    simbologia.aplica_simb("red nacional de caminos")
    transp.transp("red nacional de caminos",50)
    ccapas.carga_capas(ruta_arch1, nombre_capa1)        # carga las manzanas del estado correspondiente.
    simbologia.aplica_simb(nombre_capa1)
    r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + " " + str(nummapa) + " estado"
    nnomb = "Municipios " + arcpy.env.estado
    renombra.renomb(nombre_capa, nnomb)
    renombra.renomb("manzana_localidad", "Manzanas urbanas")
    exportma.exportar(r_dest)
    ccapas.remover_capas(nnomb)
    ccapas.remover_capas("Manzanas urbanas")
    arcpy.env.nummapa = nummapa + 1
    log.log(u"Proceso 'mapaEstatal' finalizado! \n\n")


def mapaMunicipal(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa municipal

    log.log(u"Proceso 'mapaMunicipal' iniciando...")
    log.log(u"Ámbito urbano: " + arcpy.env.ambito + " para mapa municipal")

    if arcpy.env.ambito != "Rural":
        # proceso si el sistema es urbano
        urbano.purbano(nummapa)

        # 
    else:
        # proceso si el sistema es rural
        rural.prural(nummapa)
    log.log(u"Proceso 'mapaMunicipal' finalizado! \n\n")


def cuadroConstruccion():
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de construcción en formato dwg

    log.log(u"Proceso 'cuadroConstruccion' iniciando...")
    
    # reload(dwgs)
    dwgs.dxf("aaaa")
    log.log(u"Proceso 'cuadroConstruccion' finalizado! \n\n")

def servicios_urbanos(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para analizar servicios cercanos al sistema (5 minutos caminando a 5 km/hr)

    log.log(u"Proceso 'servicios' iniciando...")

    if  arcpy.env.ambito != "Rural":
        # proceso si el sistema es urbano
        log.log(u"Iniciando proceso de servicios urbanos")
        servicios.servicios(nummapa)
    else:
        log.log(u"El proceso de servicios no se aplica al ámbito rural")
    log.log(u"Proceso 'servicios' finalizado! \n\n")


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Proceso para el medio físico natural

def usodeSuelo(nummapa):
    #-----------------> USO DE SUELO<------------------------------------------

    log.log(u"Proceso 'usodeSuelo' iniciando...")

        # tabla
    rutaCl = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI" # ruta del archivo a identificar
    capaCl = "USO DE SUELO INEGI SERIE IV.shp" # archivo a identificar
    capa_salida = "Uso de suelo" # capa a crear en el mapa
    camposCons = ["DESCRIP", "INFYS_0409", "VEG_FORES", 
                  "CVE_FAO", "HECTARES", "FORMACION", 
                  "DESVEG", "ECOS_VEGE"] # campos a escribir en el archivo
    dAlter = ["PROYECTO", "INFORMACION DEL SISTEMA", "VEGETACION FORESTAL", 
              "CLAVE FAO", "HECTAREAS", "FORMACION", 
              "DESCRIPCION DE VEGETACION", "ECOSISTEMA VEGETAL"]

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        # mapa
    capas = ["USO DE SUELO INEGI SERIE IV"]
    rutas = ["Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"]
    ncampo = ["ECOS_VEGE"]
    tipo = "municipal"
    nummapa = arcpy.env.nummapa
    tit = "USO DE SUELO INEGI SERIE IV"
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'usodeSuelo' finalizado! \n\n")



def curvasdeNivel(nummapa):
    #----------------->CURVAS DE NIVEL<------------------------------------------

    log.log(u"Proceso 'curvasdeNivel' iniciando...")

        # mapa
    capas = ["Curvas de nivel"]
    rutas = ["Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"]
    tipo = "municipal"
    ncampo = ["ALTURA"]
    nummapa = arcpy.env.nummapa
    tit = "Curvas de nivel"
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'curvasdeNivel' finalizado! \n\n")



def hidrologia(nummapa):
    #----------------->HIDROLOGÍA<------------------------------------------

    log.log(u"Proceso 'hidrologia' iniciando...")

        # mapa
    capas = ["Corrientes de agua", "Cuerpos de agua"]
    rutaor = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
    rutas = [rutaor, rutaor]
    tipo = "municipal"
    ncampo = ["NOMBRE", "NOMBRE"]
    nummapa = arcpy.env.nummapa
    

        # near a corrientes de agua
    rutaorigen = rutaor + "/"
    capa = capas[0]
    distancia = 50
    campo = "NEAR_DIST"
    valor = -1
    n=0
    camporef = ncampo[n]
    archivo = capa + " near"
    cantidad = 20
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # near a cuerpos de agua
    rutaorigen = rutaor + "/"
    capa = capas[1]
    distancia = 50
    campo = "NEAR_DIST"
    valor = -1
    n=1
    camporef = ncampo[n]
    archivo = capa + " near"
    cantidad = 20
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tit = u"Hidrología"
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

    log.log(u"Proceso 'hidrologia' finalizado! \n\n")


def lineasElectricas(nummapa):
    
    #----------------->LINEAS DE TRANSMISIÓN ELECTRICA<------------------------------------------
    
    log.log(u"Proceso 'lineasElectricas' iniciando...")

        # mapa
    rutaCl = "Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI" # ruta del archivo a identificar
    capas = ["Linea de transmision electrica", "Planta generadora", "Subestacion electrica"]
    rutaor = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
    rutas = [rutaor, rutaor, rutaor]
    ncampo = ["TIPO", "NOMBRE", "NOMBRE"]  # Esta variable se usa para los rótulos de los elementos gráficos en el mapa
    tit = u"Infraestructura eléctrica de alta tensión"

    #     # near a Linea de transmision electrica
    # rutaorigen = rutaor + "/"
    # capa = capas[0]
    # distancia = 50
    # campo = "NEAR_DIST"
    # valor = -1
    # camporef = "TIPO"
    # archivo = capa + " near"
    # cantidad = 20

        # near primera capa
    n=0
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[n]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # near segunda capa
    n=1
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[n]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # near tercera capa
    n=2
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[n]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # mapas

    tipo = "estatal"
    nummapa = arcpy.env.nummapa
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

    tipo = "municipal"
    nummapa = arcpy.env.nummapa
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'lineasElectricas' finalizado! \n\n")


def malpais(nummapa):
    #-----------------> MALPAIS<------------------------------------------

    log.log(u"Proceso 'malpais' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Malpais.shp" # archivo a identificar
    capa_salida = "Malpais" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "CODIGO"] # campos a escribir en el archivo
    dAlter = ["IDENTIFICADOR GEOGRAFICO", "CLAVE DE IDENTIFICACION", "CODIGO DE IDENTIFICACION"] # descriptores para los campos en el archivo txt de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        # mapa
    capas = ["Malpais"]
    rutas = [rutaCl]
    ncampo = ["IDENTIFICA"] # campo para el rótulo
    tipo = "estatal" # código para el nivel de representación
    nummapa = arcpy.env.nummapa
    tit = "MALPAIS INEGI SERIE IV"  # título del mapa en el layout
    ordinal = 4

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'malpais' finalizado! \n\n")


def pantano(nummapa):
    #-----------------> PANTANO<------------------------------------------

    log.log(u"Proceso 'pantano' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Pantano.shp" # archivo a identificar
    capa_salida = "Pantano" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA"] # campos a escribir en el archivo
    dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN"] # descriptores para los campos en el archivo txt de salida
    
    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)
    
        # mapa
    capas = ["Pantano"]
    rutas = [rutaCl]
    ncampo = ["IDENTIFICA"] # campo para el rótulo
    tipo = "estatal" # código para el nivel de representación
    nummapa = arcpy.env.nummapa           # consecutivo para el número de mapa en el nombre del archivo
    tit = "PANTANOS INEGI SERIE IV"  # título del mapa en el layout
    ordinal = 4
    
    
        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'pantano' finalizado! \n\n")


def pistadeAviacion(nummapa):
    #-----------------> PISTA DE AVIACIÓN<------------------------------------------

    log.log(u"Proceso 'pistadeAviacion' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Pista de aviacion.shp" # archivo a identificar
    capa_salida = "Pista de aviacion" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "NOMBRE", "CONDICION", "TIPO"] # campos a escribir en el archivo
    dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN", u"NOMBRE", u"CONDICIÓN", u"TIPO"] # descriptores para los campos en el archivo txt de salida

    # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        # mapa
    capas = ["Pista de aviacion"]
    rutas = [rutaCl]
    ncampo = ["NOMBRE"]                       # campo para el rótulo
    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    tit = u"PISTAS DE AVIACIÓN"                 # título del mapa en el layout
    ordinal = 5
        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos

    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'pistadeAviacion' finalizado! \n\n")



def presa(nummapa):

    #-----------------> PRESA<------------------------------------------
    
    log.log(u"Proceso 'presa' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Presa.shp" # archivo a identificar
    capa_salida = "Presa" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "NOMBRE", "CONDICION"] # campos a escribir en el archivo
    dAlter = [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"CONDICION"] # descriptores para los campos en el archivo txt de salida

    # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        # mapa
    capas = ["Presa"]
    rutas = [rutaCl]
    ncampo = ["NOMBRE"]                           # campo para el rótulo
    tit = u"Presa".upper()                      # título del mapa en el layout


          # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)  

    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 5
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'presa' finalizado! \n\n")




def rasgoArqueologico(nummapa):

    #-----------------> RASGO ARQUEOLOGICO<------------------------------------------

    log.log(u"Proceso 'rasgoArqueologico' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Rasgo arqueologico.shp" # archivo a identificar
    capa_salida = "Rasgo arqueologico" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "NOMBRE", "TIPO"] # campos a escribir en el archivo
    dAlter = ["IDENTIFICADOR GEOGRAFICO", "CLAVE DE IDENTIFICACION", "NOMBRE", "TIPO"] # descriptores para los campos en el archivo txt de salida

    # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        # mapa
    capas = ["Rasgo arqueologico"]
    rutas = [rutaCl]
    ncampo = ["NOMBRE"]                           # campo para el rótulo
    tit = "Rasgo arqueologico".upper()                      # título del mapa en el layout
        
        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 4
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'rasgoArqueologico' finalizado! \n\n")



def salina(nummapa):

    #-----------------> SALINA<------------------------------------------

    log.log(u"Proceso 'salina' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Salina.shp" # archivo a identificar
    capa_salida = "Salina" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "NOMBRE", "TIPO"] # campos a escribir en el archivo
    dAlter = ["IDENTIFICADOR GEOGRAFICO", "CLAVE DE IDENTIFICACION", "NOMBRE", "TIPO"] # descriptores para los campos en el archivo txt de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Salina"]
    rutas = [rutaCl]
    ncampo = ["NOMBRE"]                           # campo para el rótulo
    tit = "Salina".upper()                      # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # mapa
    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 3
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'salina' finalizado! \n\n")




def viaferrea(nummapa):

    #-----------------> VIA FERREA<------------------------------------------

    log.log(u"Proceso 'Vía Ferrea' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Via ferrea.shp" # archivo a identificar
    capa_salida = "Via ferrea" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "CONDICION", "TIPO"] # campos a escribir en el archivo
    dAlter = ["IDENTIFICADOR GEOGRAFICO", "CLAVE DE IDENTIFICACION", "CONDICION", "TIPO"] # descriptores para los campos en el archivo txt de salida

    # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Via ferrea"]
    rutas = [rutaCl]
    ncampo = ["TIPO"]                         # campo para el rótulo
    tit = capa_salida.upper()                      # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # mapa
    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 5
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'Via ferrea' finalizado! \n\n")




def zonaarenosa(nummapa):

    #-----------------> ZONA ARENOSA<------------------------------------------

    log.log(u"Proceso 'Zona arenosa' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
    capaCl = "Zona arenosa.shp" # archivo a identificar
    capa_salida = "Zona arenosa" # capa a crear en el mapa
    camposCons = ["GEOGRAFICO", "IDENTIFICA", "CALI_REPR", "TIPO"] # campos a escribir en el archivo
    dAlter = ["IDENTIFICADOR GEOGRAFICO", "CLAVE DE IDENTIFICACION", "CALIDAD DE REPRESENTACION", "TIPO"] # descriptores para los campos en el archivo txt de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Zona arenosa"]
    rutas = [rutaCl]
    ncampo = ["TIPO"]                           # campo para el rótulo en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # mapa
    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 5
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'Zona arenosa' finalizado! \n\n")


#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
# CARTOGRAFÍA DEL INIFAP




def area_nat_protegida(nummapa):

    #-----------------> AREA NATURAL PROTEGIDA <------------------------------------------

    log.log(u"Proceso 'Areas naturales protegidas' iniciando...")

        # tabla

    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar
    capaCl = "Areas naturales protegidas.shp" # archivo a identificar
    capa_salida = "Areas naturales protegidas" # capa a crear en el mapa
    camposCons = ["NOMBRE", "TIPO", "CATEGORIA", "FUENTE", "SUP_DEC2", "ESTADO"] # campos a escribir en el archivo identity
    dAlter = ["NOMBRE", "TIPO", "CATEGORÍA", "FUENTE", "SUPERFICIE DECRETADA", "ESTADO"] # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Areas naturales protegidas"]
    rutas = [rutaCl]
    ncampo = ["NOMBRE"]                         # campo para el rótulo
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        # mapa
    tipo = "nacional"                           # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    log.log(u"Proceso 'Areas naturales protegidas' finalizado! \n\n")



def clima_koppen(nummapa):

    #-----------------> CLIMA <------------------------------------------

    log.log(u"Proceso 'Climas' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar
    capaCl = "Climas.shp" # archivo a identificar
    capa_salida = "Climas" # capa a crear en el mapa
    camposCons = ["CLIMA_TIPO", "DES_TEM", "DESC_PREC"] # campos a escribir en el archivo identity
    dAlter = ["CLIMA KOPPEN", "DESCRIPCIÓN TEMPERATURA", "DESCRIPCIÓN PRECIPITACIÓN"] # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Climas"]
    rutas = [rutaCl]
    ncampo = ["CLIMA_TIPO"]                     # campo para el rótulo
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 20                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Clima' finalizado! \n\n")


def clima_olgyay(nummapa):

    #-----------------> CLIMA <------------------------------------------

    log.log(u"Proceso 'Clima Olgyay' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/00 PROPIOS/CLIMA" # ruta del archivo a identificar
    capaCl = "MEXICO_OLGYAY.shp" # archivo a identificar
    capa_salida = "Climas Olgyay" # capa a crear en el mapa
    camposCons = ["CLIMA"] # campos a escribir en el archivo identity
    dAlter = ["CLIMA OLGYAY"] # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["MEXICO_OLGYAY"]
    rutas = [rutaCl]
    ncampo = ["CLIMA"]                          # campo para el rótulo
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 2                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "nacional"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Clima Olgyay' finalizado! \n\n")



def cuenca(nummapa):

    #-----------------> CUENCA HIDROLOGICA <------------------------------------------

    log.log(u"Proceso 'Cuenca hidrologica' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                       # ruta del archivo a identificar
    capaCl = "Cuenca hidrologica.shp"                                   # archivo a identificar
    capa_salida = "Cuenca hidrologica"                                  # capa a crear en el mapa
    camposCons = ["CUENCA", "REGION"]  # campos a escribir en el archivo identity
    dAlter = ["CUENCA", "REGION"]     # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Cuenca hidrologica"]
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "nacional"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Cuenca hidrologica' finalizado! \n\n")


def edafologia(nummapa):

    #-----------------> EDAFOLOGIA <------------------------------------------

    log.log(u"Proceso 'Edafologia' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
    capaCl = "Edafologia.shp"                                                       # archivo a identificar
    capa_salida = "Edafologia"                                                      # capa a crear en el mapa
    camposCons = ["DESCRIPCIO","SUE1","DESC_TEX","DESC_FASFI","DESC_FAQUI"]     # campos a escribir en el archivo identity
    dAlter = ["DESCRIPCION","CLAVE EDAFOLÓGICA","TEXTURA","FASE FÍSICA","FASE QUÍMICA"]    # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Edafologia"]                      #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Edafologia' finalizado! \n\n")


def humedad(nummapa):

    #-----------------> HUMEDAD DEL SUELO <------------------------------------------

    log.log(u"Proceso 'Humedad del suelo' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
    capaCl = "Humedad del suelo.shp"                                                # archivo a identificar
    capa_salida = "Humedad del suelo"                                               # capa a crear en el mapa
    camposCons = ["TIPO"]                                                           # campos a escribir en el archivo identity
    dAlter = ["Tipo de humedad en suelo"]                                           # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Humedad del suelo"]               #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Humedad del suelo' finalizado! \n\n")


def precip(nummapa):

    #-----------------> PRECIPITACION ISOYETAS <------------------------------------------

    log.log(u"Proceso 'Precipitacion isoyetas' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
    capaCl = "Precipitacion isoyetas.shp"                                           # archivo a identificar
    capa_salida = "Precipitación isoyetas"                                          # capa a crear en el mapa
    camposCons = ["PRECI_RANG"]                                                     # campos a escribir en el archivo identity
    dAlter = ["Rango de precipitacion (l/m2)"]                                      # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Precipitacion isoyetas"]          #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Precipitacion isoyetas' finalizado! \n\n")


def subcuenca(nummapa):

    #-----------------> SUBCUENCA HIDROLÓGICA <------------------------------------------

    log.log(u"Proceso 'Subcuencas hidrologicas' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
    capaCl = "Subcuencas hidrologicas.shp"                                          # archivo a identificar
    capa_salida = "Subcuencas hidrólgicas"                                          # capa a crear en el mapa
    camposCons = ["NOMBRE", "DESCRIPCI", "TIPO"]                                    # campos a escribir en el archivo identity
    dAlter = ["NOMBRE", "DESCRIPCIÓN", "TIPO"]                                      # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Subcuencas hidrologicas"]         #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Subcuencas hidrologicas' finalizado! \n\n")


def subregion(nummapa):

    #-----------------> SUBREGIÓN HIDROLÓGICA <------------------------------------------

    log.log(u"Proceso 'Subregiones hidrologicas' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
    capaCl = "Subregiones hidrologicas.shp"                                         # archivo a identificar
    capa_salida = "Subregiones hidrólgicas"                                         # capa a crear en el mapa
    camposCons = ["NOMBRE"]                                    # campos a escribir en el archivo identity
    dAlter = ["NOMBRE"]                                      # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Subregiones hidrologicas"]        #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Subregiones hidrologicas' finalizado! \n\n")



def zonaecol(nummapa):

    #-----------------> ZONAS ECOLÓGICAS <------------------------------------------

    log.log(u"Proceso 'Zonas ecologicas' iniciando...")

        # tabla
    rutaCl = "Y:/GIS/MEXICO/VARIOS/conabio/WGS84"               # ruta del archivo a identificar
    capaCl = "Zonas ecologicas.shp"                             # archivo a identificar
    capa_salida = "Zonas ecológicas"                            # capa a crear en el mapa
    camposCons = ["NOMZONECOL", "TIPO_ZONA"]                    # campos a escribir en el archivo identity
    dAlter = ["NOMBRE", "TIPO"]                                 # descriptores para los campos en el archivo identity de salida

    idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

        
    capas = ["Zonas ecologicas"]                #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
    rutas = [rutaCl]
    ncampo = dAlter [0]                         # campo para el rótulo de los features en el mapa
    tit = capa_salida.upper()                   # título del mapa en el layout

        # near 
    rutaorigen = rutaCl + "/"                   # Ruta del archivo a analizar
    capa = capas[0]                             # Capa a analizar
    distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
    campo = "NEAR_DIST"                         # campo donde se guarda la distancia al sistema
    valor = -1                                  # valor a eliminar del campo 'campo'
    n=0
    camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
    archivo = capa + " near"                    # nombre del archivo de texto a generar para proceso 'near'
    cantidad = 10                               # cantidad de registros más cercanos
    nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

    tipo = "estatal"                            # código para el nivel de representación
    nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
    ordinal = 0
    cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    log.log(u"'Zonas ecologicas' finalizado! \n\n")




#========================================INICIO DEL PROCESO=============================================

# Con algunos fallos de generación de mapas, funciona correr por secciones los procesos siguientes



rutacarp()
cargalib()
db()

borrainn()
arcpy.env.nummapa = 1
nummapa = 1 # línea temporal cuando no se tiene definido el número de mapa
# mapaPais(arcpy.env.nummapa)
# mapaEstatal(arcpy.env.nummapa)
# mapaMunicipal(arcpy.env.nummapa)

# cuadroConstruccion()

# #----------------------------CARTOGRAFÍA MAPAS TEMÁTICOS INEGI

# servicios_urbanos(arcpy.env.nummapa)
# curvasdeNivel(arcpy.env.nummapa)
# hidrologia(arcpy.env.nummapa)
# lineasElectricas(arcpy.env.nummapa)
# malpais(arcpy.env.nummapa)
# pantano(arcpy.env.nummapa)
# pistadeAviacion(arcpy.env.nummapa)
# presa(arcpy.env.nummapa) 
# rasgoArqueologico(arcpy.env.nummapa)
# salina(arcpy.env.nummapa)
# usodeSuelo(arcpy.env.nummapa)
# viaferrea(nummapa)
# zonaarenosa(nummapa)

# #----------------------------CARTOGRAFÍA INIFAP

# area_nat_protegida(nummapa)
# clima_koppen(nummapa)
# clima_olgyay(nummapa)
# cuenca(nummapa)
edafologia(nummapa)
humedad(nummapa)
precip(nummapa)
subcuenca(nummapa)
subregion(nummapa)
zonaecol(nummapa)

log.log(u"\n\n PROCESO SIG FINALIZADO!!")
print ("\n\n\n\n PROCESO SIG FINALIZADO!! \n\n No es necesario guardar el mapa.")