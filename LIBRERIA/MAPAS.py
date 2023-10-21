# -*- coding: utf-8 -*-

# ----RUTINA PARA IMPRIMIR MAPAS DE UBICACIÓN A NIVEL PAIS, ESTADO, MUNICIPIO, REGIÓN, ZONA Y SITIO

import arcpy
import sys
import importlib
import codecs
import datetime

# arcpy.env.addOutputsToMap = u"CURRENT"

# Proceso para inicializar cuadros de diálogo
import Tkinter as tk
import tkFileDialog
root = tk.Tk()
root.withdraw()

# Agrega la ruta del paquete al path de Python

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

arcpy.env.mxd = arcpy.mapping.MapDocument(u"CURRENT")                    # Obtener acceso al documento actual
mxd = arcpy.env.mxd
arcpy.env.df = arcpy.mapping.ListDataFrames(mxd)[0]
df = arcpy.env.df
arcpy.env.layout = u"Layout"

# Importar el módulo desde el paquete LIBRERIA utilizando importlib
dbas = importlib.import_module(u"LIBRERIA.datos_basicos")
log = importlib.import_module(u"LIBRERIA.archivo_log")


def rutacarp():

    try:
        # Abre un cuadro de diálogo para seleccionar una carpeta
        carp_mapas = u"Y:/02 CLIENTES (EEX-CLI)/(2001-0001) FAMILIA MARTINEZ DEL RIO/(2008-PIN-0005) CASA BUENAVISTA/SIG"
        carpeta_cliente = tkFileDialog.askdirectory(initialdir=carp_mapas, title="Selecciona la carpeta destino de los mapas") + u"/"
        arcpy.env.carp_cliente = carpeta_cliente
        # Verifica si el usuario seleccionó una carpeta
        if carpeta_cliente:
            log.log(u"Ruta de la carpeta seleccionada: %s" % carpeta_cliente)
        else:
            print(u"No se seleccionó ninguna carpeta.")
            log.log(u"No se seleccionó ninguna carpeta.")
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'rutacarp'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()

    

# Preliminares
def db():

    try:

        dbas.datosbasicos() # define los datos básicos del proyecto y crea el archivo txt correspondiente
        log.log(u"\n\n\n")
        log.log(u"--------------INICIO DE SECCIÓN LOG \--------------------------")
        log.log(u"\n")
        log.log(u"Proceso 'datos básicos' iniciando...")
        log.log(u"Proceso 'datos básicos' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'db'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()

def cargalib():

    try:

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

        ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")               #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
        ctrlcapa = importlib.import_module(u"LIBRERIA.control_de_capa")          #carga el script de control de capas  -----> funciones: apagacapa(capa_a_apagar), encendercapa(capa_a_encender)
        ctrlgrup = importlib.import_module(u"LIBRERIA.control_de_grupo")         #carga el script de control de grupos
        exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")           #carga el script para exportar mapas a pdf y jpg
        filtro = importlib.import_module(u"LIBRERIA.filtro")                     #carga el script para aplicar filtros a una capa
        formato = importlib.import_module(u"LIBRERIA.formato")                   #carga el script para aplicar formato a layout
        simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")         #carga el script para aplicar simbología a capas
        z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")              #carga el script para aplicar zoom extent a una capa 
        act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")            #carga el script para activar y desactivar los rótulos de una capa  -----> funciones: 
        buff_cl = importlib.import_module(u"LIBRERIA.buffer_clip")               #carga el script para activar y desactivar los rótulos de una capa  -----> funciones: clip(ruta, radio)
        transp = importlib.import_module(u"LIBRERIA.aplica_transparencia")       #carga el script para aplicar transparencia a capas
        renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")           #carga el script para cambiar el nombre a capas
        urbano = importlib.import_module(u"LIBRERIA.urbano_nacional")            # ejecuta rutina de zonas urbanas
        rural = importlib.import_module(u"LIBRERIA.rural_nacional")              # ejecuta rutina de zonas rurales
        dwgs = importlib.import_module(u"LIBRERIA.cuadro_de_localizacion")
        servicios = importlib.import_module(u"LIBRERIA.servicios")
        cliptema = importlib.import_module(u"LIBRERIA.clip_tematico")
        idproy = importlib.import_module(u"LIBRERIA.identity_sistema")
        nearexp = importlib.import_module(u"LIBRERIA.near_a_sistema")
        log = importlib.import_module(u"LIBRERIA.archivo_log")
        leyenda = importlib.import_module(u"LIBRERIA.leyenda_ajuste")
        
        
        
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

        ccapas.carga_capas(u"Y:/0_SIG_PROCESO/00 GENERAL", u"SISTEMA")
        simbologia.aplica_simb(u"SISTEMA")
        transp.transp(u"SISTEMA",50)
        z_extent.zoom_extent(arcpy.env.layout, u"SISTEMA")

        #formato.formato_layout(u"Preparacion")

        log.log(u"Proceso 'cargalib' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'cargalib'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()

    # nota, para poder cargar las librería y que se genere el archivo .pyc adecuadamente, cada librería debe iniciar con la línea: # -*- coding: utf-8 -*-


# -------------------------------------------------------------------------------


def borrainn():
        
    try:

        log.log(u"iniciando proceso de borrado capas innecesarias...")

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
                log.log(u"Removiendo capa " + str(lyr))

        # Actualizar el contenido del DataFrame
        arcpy.RefreshTOC()
        log.log(u"Proceso de borrado capas innecesarias finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'borrainn'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def mapaPais(nummapa):

    try:

        log.log(u"Proceso 'mapaPais' iniciando...")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa a nivel pais
        
        nombre_capa = u"ESTATAL decr185"
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        act_rot.activar_rotulos(nombre_capa,"NOM_ENT")
        z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
        simbologia.aplica_simb(nombre_capa)
        formato.formato_layout(u"UBICACIÓN A NIVEL PAÍS")
        r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + u" " + str(nummapa) + u" pais"
        nnomb = u"Entidades Federativas"
        renombra.renomb(nombre_capa, nnomb)
        exportma.exportar(r_dest)
        ccapas.remover_capas(nnomb)
        arcpy.env.nummapa = nummapa + 1
        log.log(u"Proceso 'mapaPais' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'mapaPais'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()

def mapaEstatal(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa estatal

    try:


        log.log(u"Proceso 'mapaEstatal' iniciando...")

        nombre_capa = u"MUNICIPAL CENSO 2020 DECRETO 185"
        ruta_arch = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"
        ruta_arch1 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + u"/cartografia"
        nombre_capa1 = u"manzana_localidad"
        campo = u"NOM_ENT"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        filtro.aplicar_defq(nombre_capa, campo, u"'" + arcpy.env.estado + u"'")
        z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
        simbologia.aplica_simb(nombre_capa)
        formato.formato_layout(u"UBICACIÓN A NIVEL ESTADO")
        act_rot.activar_rotulos(nombre_capa,"NOM_MUN")
        ccapas.carga_capas(ruta_arch1, u"red nacional de caminos")
        simbologia.aplica_simb(u"red nacional de caminos")
        transp.transp(u"red nacional de caminos",50)
        ccapas.carga_capas(ruta_arch1, nombre_capa1)        # carga las manzanas del estado correspondiente.
        simbologia.aplica_simb(nombre_capa1)
        r_dest = arcpy.env.carp_cliente + arcpy.env.proyecto + u" " + str(nummapa) + u" estado"
        nnomb = u"Municipios " + arcpy.env.estado
        renombra.renomb(nombre_capa, nnomb)
        renombra.renomb(u"manzana_localidad", u"Manzanas urbanas")
        exportma.exportar(r_dest)
        ccapas.remover_capas(nnomb)
        ccapas.remover_capas(u"Manzanas urbanas")
        arcpy.env.nummapa = nummapa + 1
        log.log(u"Proceso 'mapaEstatal' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'mapaEstatal'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def mapaMunicipal(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa municipal

    try:

        log.log(u"Proceso 'mapaMunicipal' iniciando...")
        log.log(u"Ámbito urbano: " + arcpy.env.ambito + u" para mapa municipal")

        if arcpy.env.ambito != "Rural":
            # proceso si el sistema es urbano
            urbano.purbano(nummapa)

            # 
        else:
            # proceso si el sistema es rural
            rural.prural(nummapa)
        log.log(u"Proceso 'mapaMunicipal' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'mapaMunicipal'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def cuadroConstruccion():
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de construcción en formato dwg

    try:

        log.log(u"Proceso 'cuadroConstruccion' iniciando...")
        
        # reload(dwgs)
        dwgs.dxf(u"aaaa")
        log.log(u"Proceso 'cuadroConstruccion' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'cuadroConstruccion'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()

def servicios_urbanos(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para analizar servicios cercanos al sistema (5 minutos caminando a 5 km/hr)

    try:

        log.log(u"Proceso 'servicios' iniciando...")

        if  arcpy.env.ambito != "Rural":
            # proceso si el sistema es urbano
            log.log(u"Iniciando proceso de servicios urbanos")
            servicios.servicios(nummapa)
        else:
            log.log(u"El proceso de servicios no se aplica al ámbito rural")
        log.log(u"Proceso 'servicios' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'servicio_urbanos'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Proceso para el medio físico natural

def usodeSuelo(nummapa):
    #-----------------> USO DE SUELO<------------------------------------------

    try:

        log.log(u"Proceso 'usodeSuelo' iniciando...")

            # tabla
        rutaCl = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"                  # ruta del archivo a identificar
        capaCl = u"USO DE SUELO INEGI SERIE IV.shp"                                  # archivo a identificar
        capa_salida = u"Uso de suelo"                                                # capa a crear en el mapa
        camposCons =  [u"INFYS_0409", u"VEG_FORES"]                                    # campos a escribir en el archivo de identificación
        dAlter =  [u"USO DE SUELO", u"VEGETACION FORESTAL"]                            # descripciones de campos de archivo de identificación

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"USO DE SUELO INEGI SERIE IV"]
        rutas =  [u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI"]
        ncampo = [camposCons[0]]
        tipo = u"municipal"
        nummapa = arcpy.env.nummapa
        tit = u"USO DE SUELO INEGI SERIE IV"
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'usodeSuelo' finalizado! \n\n")
    

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'usodeSuelo'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def curvasdeNivel(nummapa):
    #----------------->CURVAS DE NIVEL<------------------------------------------

    try:

        log.log(u"Proceso 'curvasdeNivel' iniciando...")

            # mapa
        capas =  [u"Curvas de nivel"]
        rutas =  [u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"]
        tipo = u"municipal"
        ncampo =  [u"ALTURA"]
        nummapa = arcpy.env.nummapa
        tit = u"Curvas de nivel"
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'curvasdeNivel' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'curvasdeNivel'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def hidrologia(nummapa):
    #----------------->HIDROLOGÍA<------------------------------------------

    try:

        log.log(u"Proceso 'hidrologia' iniciando...")

            # mapa
        capas =  [u"Corrientes de agua", u"Cuerpos de agua"]
        rutaor = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
        rutas = [rutaor, rutaor]
        tipo = u"municipal"
        ncampo =  [u"NOMBRE", u"NOMBRE"]
        nummapa = arcpy.env.nummapa
        

            # near a corrientes de agua
        rutaorigen = rutaor + u"/"
        capa = capas[0]
        distancia = 50
        campo = u"NEAR_DIST"
        valor = -1
        n=0
        camporef = ncampo[n]
        archivo = capa + u" near"
        cantidad = 20
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # near a cuerpos de agua
        rutaorigen = rutaor + u"/"
        capa = capas[1]
        distancia = 50
        campo = u"NEAR_DIST"
        valor = -1
        n=1
        camporef = ncampo[n]
        archivo = capa + u" near"
        cantidad = 20
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tit = u"Hidrología"
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

        log.log(u"Proceso 'hidrologia' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'hidroligia'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def lineasElectricas(nummapa):
    
    #----------------->LINEAS DE TRANSMISIÓN ELECTRICA<------------------------------------------

    try:
    
        log.log(u"Proceso 'lineasElectricas' iniciando...")

            # mapa
        rutaCl = u"Y:/0_SIG_PROCESO/BASES DE DATOS/00 MEXICO/INEGI" # ruta del archivo a identificar
        capas =  [u"Linea de transmision electrica", u"Planta generadora", u"Subestacion electrica"]
        rutaor = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
        rutas = [rutaor, rutaor, rutaor]
        ncampo =  [u"TIPO", u"NOMBRE", u"NOMBRE"]       # Esta variable se usa para los rótulos de los elementos gráficos en el mapa
        tit = u"Infraestructura eléctrica de alta tensión"


            # near primera capa
        n=0
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # near segunda capa
        n=1
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # near tercera capa
        n=2
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapas

        tipo = u"estatal"
        nummapa = arcpy.env.nummapa
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

        tipo = u"municipal"
        nummapa = arcpy.env.nummapa
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'lineasElectricas' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'lineasElectricas'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def malpais(nummapa):
    #-----------------> MALPAIS<------------------------------------------

    try:

        log.log(u"Proceso 'malpais' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"      # ruta del archivo a identificar
        capaCl = u"Malpais.shp"                                          # archivo a identificar
        capa_salida = u"Malpais"                                         # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CODIGO"]             # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CODIGO DE IDENTIFICACION"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Malpais"]
        rutas = [rutaCl]
        ncampo = [camposCons[1]]                                              # campo para el rótulo
        tipo = u"estatal"                                                # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 
        tit = u"MALPAIS INEGI SERIE IV"                                  # título del mapa en el layout
        ordinal = 4                 

            # near                  
        rutaorigen = rutaCl + u"/"                                       # Ruta del archivo a analizar
        capa = capas[0]                                                 # Capa a analizar
        distancia = 1000                                                # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                                             # campo donde se guarda la distancia al sistema
        valor = -1                                                      # valor a eliminar del campo 'campo'
        n=0                 
        camporef = ncampo[n]                                            # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                                        # nombre del archivo de texto a generar
        cantidad = 20                                                   # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'malpais' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'malpais'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def pantano(nummapa):
    #-----------------> PANTANO<------------------------------------------

    try:

        log.log(u"Proceso 'pantano' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Pantano.shp" # archivo a identificar
        capa_salida = u"Pantano" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA"]   # campos a imprimi en el archivo de identidad
        dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN"] # descriptores para los campos en el archivo txt de salida
        
        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)
        
            # mapa
        capas =  [u"Pantano"]
        rutas = [rutaCl]
        ncampo = [camposCons[1]]                    # campo para el rótulo
        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        tit = u"PANTANOS INEGI SERIE IV"             # título del mapa en el layout
        ordinal = 4
        
        
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'pantano' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'pantano'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def pistadeAviacion(nummapa):
    #-----------------> PISTA DE AVIACIÓN<------------------------------------------

    try:

        log.log(u"Proceso 'pistadeAviacion' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Pista de aviacion.shp" # archivo a identificar
        capa_salida = u"Pista de aviacion" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"CONDICION", u"TIPO"] # campos a escribir en el archivo
        dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN", u"NOMBRE", u"CONDICIÓN", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Pista de aviacion"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        tit = u"PISTAS DE AVIACIÓN"                 # título del mapa en el layout
        ordinal = 5
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos

        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'pistadeAviacion' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'pistadeAviacion'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def presa(nummapa):

    #-----------------> PRESA<------------------------------------------

    try:
    
        log.log(u"Proceso 'presa' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Presa.shp" # archivo a identificar
        capa_salida = u"Presa" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"CONDICION"] # campos a escribir en el archivo
        dAlter = [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"CONDICION"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Presa"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Presa".upper()                      # título del mapa en el layout


            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)  

        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'presa' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'presa'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()




def rasgoArqueologico(nummapa):

    #-----------------> RASGO ARQUEOLOGICO<------------------------------------------

    try:

        log.log(u"Proceso 'rasgoArqueologico' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Rasgo arqueologico.shp" # archivo a identificar
        capa_salida = u"Rasgo arqueologico" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Rasgo arqueologico"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Rasgo arqueologico".upper()          # título del mapa en el layout
            
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 4
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'rasgoArqueologico' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'rasgoArqueologico'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def salina(nummapa):

    #-----------------> SALINA<------------------------------------------

    try:

        log.log(u"Proceso 'salina' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Salina.shp" # archivo a identificar
        capa_salida = u"Salina" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Salina"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Salina".upper()                      # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 3
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'salina' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'salina'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()




def viaferrea(nummapa):

    #-----------------> VIA FERREA<------------------------------------------

    try:

        log.log(u"Proceso 'Vía Ferrea' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Via ferrea.shp" # archivo a identificar
        capa_salida = u"Via ferrea" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CONDICION", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CONDICION", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Via ferrea"]
        rutas = [rutaCl]
        ncampo = [camposCons[3]]                          # campo para el rótulo
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

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'Via ferrea' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'viaferrea'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def zonaarenosa(nummapa):

    #-----------------> ZONA ARENOSA<------------------------------------------

    try:

        log.log(u"Proceso 'Zona arenosa' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar
        capaCl = u"Zona arenosa.shp" # archivo a identificar
        capa_salida = u"Zona arenosa" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CALI_REPR", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CALIDAD DE REPRESENTACION", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Zona arenosa"]
        rutas = [rutaCl]
        ncampo = [camposCons[3]]                          # campo para el rótulo
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

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'Zona arenosa' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'zonaarenosa'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
# CARTOGRAFÍA DEL INIFAP




def area_nat_protegida(nummapa):

    #-----------------> AREA NATURAL PROTEGIDA <------------------------------------------

    try:

        log.log(u"Proceso 'Areas naturales protegidas' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar
        capaCl = u"Areas naturales protegidas.shp" # archivo a identificar
        capa_salida = u"Areas naturales protegidas" # capa a crear en el mapa
        camposCons =  [u"NOMBRE", u"TIPO", u"CATEGORIA", u"FUENTE", u"SUP_DEC2", u"ESTADO"] # campos a escribir en el archivo identity
        dAlter =  [u"NOMBRE", u"TIPO", u"CATEGORÍA", u"FUENTE", u"SUPERFICIE DECRETADA", u"ESTADO"] # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Areas naturales protegidas"]
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

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        log.log(u"Proceso 'Areas naturales protegidas' finalizado! \n\n")
    
    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'area_nat_protegida'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def clima_koppen(nummapa):

    #-----------------> CLIMA <------------------------------------------

    try:

        log.log(u"Proceso 'Climas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84" # ruta del archivo a identificar
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
        
        log.log(u"'Clima' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'clima_koppen'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def clima_olgyay(nummapa):

    #-----------------> CLIMA <------------------------------------------

    try:

        log.log(u"Proceso 'Clima Olgyay' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/00 PROPIOS/CLIMA" # ruta del archivo a identificar
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
        
        log.log(u"'Clima Olgyay' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'clima_olgyay'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def cuenca(nummapa):

    #-----------------> CUENCA HIDROLOGICA <------------------------------------------

    try:

        log.log(u"Proceso 'Cuenca hidrologica' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                       # ruta del archivo a identificar
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
        
        log.log(u"'Cuenca hidrologica' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'cuenca'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def edafologia(nummapa):

    #-----------------> EDAFOLOGIA <------------------------------------------

    try:

        log.log(u"Proceso 'Edafologia' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
        capaCl = u"Edafologia.shp"                                                       # archivo a identificar
        capa_salida = u"Edafologia"                                                      # capa a crear en el mapa
        camposCons =  [u"DESCRIPCIO","SUE1","DESC_TEX","DESC_FASFI","DESC_FAQUI"]     # campos a escribir en el archivo identity
        dAlter =  [u"DESCRIPCION","CLAVE EDAFOLÓGICA","TEXTURA","FASE FÍSICA","FASE QUÍMICA"]    # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Edafologia"]                      #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
        rutas = [rutaCl]
        ncampo = [camposCons[0]]                          # campo para el rótulo de los features en el mapa
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
        
        log.log(u"'Edafologia' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'edafologia'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def humedad(nummapa):

    #-----------------> HUMEDAD DEL SUELO <------------------------------------------

    try:

        log.log(u"Proceso 'Humedad del suelo' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
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
        
        log.log(u"'Humedad del suelo' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'humedad'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def precip(nummapa):

    #-----------------> PRECIPITACION ISOYETAS <------------------------------------------

    try:

        log.log(u"Proceso 'Precipitacion isoyetas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
        capaCl = u"Precipitacion isoyetas.shp"                                           # archivo a identificar
        capa_salida = u"Precipitacion isoyetas"                                          # capa a crear en el mapa
        camposCons =  [u"PRECI_RANG"]                                                     # campos a escribir en el archivo identity
        dAlter =  [u"Rango de precipitacion (l/m2)"]                                      # descriptores para los campos en el archivo identity de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Precipitacion isoyetas"]          #capas a incluir en el mapa. puede ser una o más, pero siempre del mismo tema.
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
        
        log.log(u"'Precipitacion isoyetas' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'precip'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def subcuenca(nummapa):

    #-----------------> SUBCUENCA HIDROLÓGICA <------------------------------------------

    try:

        log.log(u"Proceso 'Subcuencas hidrologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
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
        
        log.log(u"'Subcuencas hidrologicas' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'subcuenca'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()


def subregion(nummapa):

    #-----------------> SUBREGIÓN HIDROLÓGICA <------------------------------------------

    try:

        log.log(u"Proceso 'Subregiones hidrologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"                                   # ruta del archivo a identificar
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
        
        log.log(u"'Subregiones hidrologicas' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'subregion'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()



def zonaecol(nummapa):

    #-----------------> ZONAS ECOLÓGICAS <------------------------------------------

    try:

        log.log(u"Proceso 'Zonas ecologicas' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/conabio/WGS84"               # ruta del archivo a identificar
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
        
        log.log(u"'Zonas ecologicas' finalizado! \n\n")

    except Exception as e:
        log.log(u"\n\n>> ERROR, no se pudo ejecutar 'zonaecol'")
        log.log(str(e) + u"\n\n\n\n")
        borrainn()




#========================================INICIO DEL PROCESO=============================================

# Con algunos fallos de generación de mapas, funciona correr por secciones los procesos siguientes



rutacarp()
cargalib()
db()

borrainn()
arcpy.env.nummapa = 1
nummapa = 1 # línea temporal cuando no se tiene definido el número de mapa
mapaPais(arcpy.env.nummapa)
mapaEstatal(arcpy.env.nummapa)
mapaMunicipal(arcpy.env.nummapa)

cuadroConstruccion()

#----------------------------CARTOGRAFÍA MAPAS TEMÁTICOS INEGI

servicios_urbanos(arcpy.env.nummapa)
curvasdeNivel(arcpy.env.nummapa)
hidrologia(arcpy.env.nummapa)
lineasElectricas(arcpy.env.nummapa)
malpais(arcpy.env.nummapa)
pantano(arcpy.env.nummapa)
pistadeAviacion(arcpy.env.nummapa)
presa(arcpy.env.nummapa) 
rasgoArqueologico(arcpy.env.nummapa)
salina(arcpy.env.nummapa)
usodeSuelo(arcpy.env.nummapa)
viaferrea(nummapa)
zonaarenosa(nummapa)

#----------------------------CARTOGRAFÍA INIFAP

area_nat_protegida(nummapa)
clima_koppen(nummapa)
clima_olgyay(nummapa)
cuenca(nummapa)
edafologia(nummapa)
humedad(nummapa)
precip(nummapa)
subcuenca(nummapa)
subregion(nummapa)
zonaecol(nummapa)

log.log(u"\n\n PROCESO SIG FINALIZADO!! Revisar archivo log para mayor informacion del proceso")
print (u"\n\n\n\n PROCESO SIG FINALIZADO!! \n\n No es necesario guardar el mapa.")