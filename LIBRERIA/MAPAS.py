# -*- coding: utf-8 -*-

# ----RUTINA PARA IMPRIMIR MAPAS DE UBICACIÓN A NIVEL PAIS, ESTADO, MUNICIPIO, REGIÓN, ZONA Y SITIO

import arcpy
import sys
import importlib
# import codecs
import datetime  # Importar módulo para obtener fecha y hora
fechahora = (str(datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S"))).replace(":", "-")
arcpy.env.fechahora = fechahora # Define variable global para usar en los nombres de los archivos generados en el proceso de generación de mapas y datos complementarios.

# Proceso para inicializar cuadros de diálogo
import Tkinter as tk
import tkFileDialog
root = tk.Tk()
root.withdraw()

# Agrega la ruta del paquete al path de Python

ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS"
sys.path.append(ruta_libreria)

arcpy.env.mxd = arcpy.mapping.MapDocument("CURRENT")                   # Obtener acceso al documento actual
mxd = arcpy.env.mxd
arcpy.env.df = arcpy.mapping.ListDataFrames(mxd)[0]
df = arcpy.env.df
arcpy.env.layout = u"Layout"

arcpy.env.repet = 0
repet = arcpy.env.repet


def rutacarp():

    print("Eligiendo carpeta iniciando...")

    try:
        print("Eligiendo carpeta")
        # Abre un cuadro de diálogo para seleccionar una carpeta
        carp_mapas = u"Y:/02 CLIENTES (EEX-CLI)"
        carpeta_cliente = tkFileDialog.askdirectory(initialdir=carp_mapas, title=u"Selecciona la carpeta destino de los mapas") + u"/"
        arcpy.env.carp_cliente = carpeta_cliente
        arcpy.env.archivolog = carpeta_cliente + u"00 archivo_log " + fechahora + u".txt"          # define una variable de entorno con el nombre del archivo log.
        print("arcpy.env.archivolog: " + arcpy.env.archivolog)

        # Verifica si el usuario seleccionó una carpeta
        if carpeta_cliente:
            print(u"Ruta de la carpeta seleccionada: " + carpeta_cliente)
            
        else:
            print(u"No se seleccionó ninguna carpeta.")
    except Exception as e:
        print(u">> Error en 'rutacarp'")
    print("Elección de carpeta terminada")

    

# Preliminares
def db():

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    # Importar el módulo desde el paquete LIBRERIA utilizando importlib
    global log
    dbas = importlib.import_module(u"LIBRERIA.datos_basicos")
    log = importlib.import_module(u"LIBRERIA.archivo_log")
    
    dbas.datosbasicos() # define los datos básicos del proyecto y crea el archivo txt correspondiente
    log.log(repet,u"\n\n\n")
    log.log(repet,u"--------------INICIO DE SECCIÓN LOG \--------------------------")
    log.log(repet,u"\n")
    log.log(repet,u"Proceso 'datos básicos' finalizado\n")

    arcpy.env.repet = arcpy.env.repet - 1

def cargalib():

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    log = importlib.import_module(u"LIBRERIA.archivo_log")

    log.log(repet,u"'cargalib' iniciando...")

    global act_rot
    global borrainn
    global ccapas
    global conabio
    global dwgs
    global exportma
    global filtro
    global formato
    global inegi_tematicos
    global renombra
    global rural
    global servicios
    global simbologia
    global tiempo
    global transp
    global urbano
    global z_extent

    act_rot = importlib.import_module(u"LIBRERIA.activa_rotulos")            #carga el script para activar y desactivar los rótulos de una capa  -----> funciones:
    borrainn = importlib.import_module(u"LIBRERIA.borrainn")
    ccapas = importlib.import_module(u"LIBRERIA.cargar_capas")               #carga el script de carga y remoción de capas  -----> funciones: carga_capas(ruta_arch, nombres_capas), remover_capas(capas_remover)
    conabio = importlib.import_module(u"LIBRERIA.conabio")
    dwgs = importlib.import_module(u"LIBRERIA.cuadro_de_localizacion")
    exportma = importlib.import_module(u"LIBRERIA.exportar_mapas")           #carga el script para exportar mapas a pdf y jpg
    filtro = importlib.import_module(u"LIBRERIA.filtro")                     #carga el script para aplicar filtros a una capa
    formato = importlib.import_module(u"LIBRERIA.formato")                   #carga el script para aplicar formato a layout
    inegi_tematicos = importlib.import_module(u"LIBRERIA.inegi_tematicos")
    renombra = importlib.import_module(u"LIBRERIA.renombrar_capa")           #carga el script para cambiar el nombre a capas
    rural = importlib.import_module(u"LIBRERIA.rural_nacional")              # ejecuta rutina de zonas rurales
    servicios = importlib.import_module(u"LIBRERIA.servicios")
    simbologia = importlib.import_module(u"LIBRERIA.simbologia_lyr")         #carga el script para aplicar simbología a capas
    tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")
    transp = importlib.import_module(u"LIBRERIA.aplica_transparencia")       #carga el script para aplicar transparencia a capas
    urbano = importlib.import_module(u"LIBRERIA.urbano_nacional")            # ejecuta rutina de zonas urbanas
    z_extent = importlib.import_module(u"LIBRERIA.zoom_extent")              #carga el script para aplicar zoom extent a una capa

    # reload(ctrlcapa)
    # reload(ccapas)
    # reload(ctrlgrup)
    # reload(exportma)
    # reload(filtro)
    # reload(formato)
    # reload(simbologia)
    # reload(z_extent)
    # reload(act_rot)
    # reload(buff_cl)
    # reload(transp)
    # reload(renombra)
    # reload(urbano)
    # reload(rural)
    # reload(dwgs)
    # reload(servicios)
    # reload(cliptema)
    # reload(idproy)
    # reload(nearexp)
    # reload(log)
    # reload(leyenda)
    # reload(tiempo)
    # reload(conabio)
    # reload(borrainn)
    # reload(inegi_tematicos)

    ccapas.cargar(u"Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp")
    simbologia.aplica_simb(u"SISTEMA")
    transp.transp(u"SISTEMA",50)
    act_rot.activar_rotulos("SISTEMA","DESCRIP")
    z_extent.zoom_extent(arcpy.env.layout, u"SISTEMA")

    log.log(repet,u"'cargalib' finalizado\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

    # nota, para poder cargar las librería y que se genere el archivo .pyc adecuadamente, cada librería debe iniciar con la línea: # -*- coding: utf-8 -*-



def mapaPais(nummapa):

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet
    

    try:

        log.log(repet,u"Proceso 'mapaPais' iniciando...")

        # -------------------------------------------------------------------------------
        # Proceso para generar mapa a nivel pais
        
        nombre_capa = u"ESTATAL decr185"
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        act_rot.activar_rotulos(nombre_capa,"NOM_ENT")
        z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
        simbologia.aplica_simb(nombre_capa)
        formato.formato_layout(u"UBICACIÓN A NIVEL PAÍS")
        r_dest = arcpy.env.carp_cliente
        nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" pais"
        nnomb = u"Entidades Federativas"
        renombra.renomb(nombre_capa, nnomb)
        exportma.exportar(r_dest,nombarch)
        ccapas.remover_capas(nnomb)
        arcpy.env.nummapa = nummapa + 1

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'mapaPais'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()
    
    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(u"Mapa País",tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'mapaPais' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def mapaEstatal(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para generar mapa estatal

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet    

    try:


        log.log(repet,u"Proceso 'mapaEstatal' iniciando...")

        nombre_capa = u"MUNICIPAL CENSO 2020 DECRETO 185"
        ruta_arch = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS"
        ruta_arch1 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/" + arcpy.env.estado + u"/cartografia"
        nombre_capa1 = u"manzana_localidad"
        ccapas.carga_capas(ruta_arch, nombre_capa)
        filtr= "\"NOM_ENT\" = '{}'".format(arcpy.env.estado)
        filtro.fil_expr(nombre_capa, filtr)
        z_extent.zoom_extent(arcpy.env.layout, nombre_capa)
        simbologia.aplica_simb(nombre_capa)
        formato.formato_layout(u"UBICACIÓN A NIVEL ESTADO")
        act_rot.activar_rotulos(nombre_capa,"NOM_MUN")
        ccapas.carga_capas(ruta_arch1, u"red nacional de caminos")
        simbologia.aplica_simb(u"red nacional de caminos")
        transp.transp(u"red nacional de caminos",50)
        ccapas.carga_capas(ruta_arch1, nombre_capa1)        # carga las manzanas del estado correspondiente.
        simbologia.aplica_simb(nombre_capa1)
        r_dest = arcpy.env.carp_cliente
        nombarch = arcpy.env.proyecto + u" " + str(nummapa) + u" estado"
        nnomb = u"Municipios " + arcpy.env.estado
        renombra.renomb(nombre_capa, nnomb)
        renombra.renomb(u"manzana_localidad", u"Manzanas urbanas")
        exportma.exportar(r_dest,nombarch)
        ccapas.remover_capas(nnomb)
        ccapas.remover_capas(u"Manzanas urbanas")
        ccapas.remover_capas(u"red nacional de caminos")
        arcpy.env.nummapa = nummapa + 1
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'mapaEstatal'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(u"Ubicación a nivel estado",tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'mapaEstatal' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def mapaMunicipal(nummapa):

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa municipal

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet    

    try:

        log.log(repet,u"Proceso 'mapaMunicipal' iniciando...")
        log.log(repet,u"Ámbito urbano: " + arcpy.env.ambito + u" para mapa municipal")

        if arcpy.env.ambito != "Rural":
            # proceso si el sistema es urbano
            urbano.purbano(nummapa)

            # 
        else:
            # proceso si el sistema es rural
            rural.prural(nummapa)

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'mapaMunicipal'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(u"Mapa municipal",tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'mapaMunicipal' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def cuadrodeLocalizacion():
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de construcción en formato dwg

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:

        log.log(repet,u"Proceso 'cuadrodeLocalizacion' iniciando...")
        
        dwgs.dxf()
        log.log(repet,u"Proceso 'cuadrodeLocalizacion' finalizado! \n\n")

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'cuadrodeLocalizacion'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de proceso '{}': {}".format(u"Archivos dxf",tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'cuadrodeLocalizacion' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def servicios_urbanos(nummapa):
    # -------------------------------------------------------------------------------
    # Proceso para analizar servicios cercanos al sistema (5 minutos caminando a 5 km/hr)

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'servicios' iniciando...")

        if  arcpy.env.ambito != "Rural":
            # proceso si el sistema es urbano
            log.log(repet,u"Iniciando proceso de servicios urbanos")
            servicios.servicios(nummapa)
        else:
            log.log(repet,u"El proceso de servicios no se aplica al ámbito rural")
        log.log(repet,u"Proceso 'servicios' finalizado! \n\n")

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'servicio_urbanos'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(u"Servicios urbanos",tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'servicios' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1



#========================================INICIO DEL PROCESO=============================================


rutacarp()
tiempoprocini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
db()
cargalib()

borrainn.borrainn()
arcpy.env.nummapa = 1
nummapa = 1 # línea temporal cuando no se tiene definido el número de mapa

# # ----------------------------MAPAS BÁSICOS

# mapaPais(arcpy.env.nummapa)
# mapaEstatal(arcpy.env.nummapa)
# mapaMunicipal(arcpy.env.nummapa)
# cuadrodeLocalizacion()
# servicios_urbanos(arcpy.env.nummapa)

# # ----------------------------CARTOGRAFÍA MAPAS TEMÁTICOS INEGI (Y:\GIS\MEXICO\VARIOS\INEGI)

# inegi_tematicos.curvasdeNivel(arcpy.env.nummapa)
# inegi_tematicos.hidrologia(arcpy.env.nummapa)
# inegi_tematicos.lineasElectricas(arcpy.env.nummapa)
# inegi_tematicos.malpais(arcpy.env.nummapa)
# inegi_tematicos.pantano(arcpy.env.nummapa)
# inegi_tematicos.pistadeAviacion(arcpy.env.nummapa)
# inegi_tematicos.presa(arcpy.env.nummapa) 
# inegi_tematicos.rasgoArqueologico(arcpy.env.nummapa)
# inegi_tematicos.salina(arcpy.env.nummapa)
# inegi_tematicos.usodeSuelo(arcpy.env.nummapa)
# inegi_tematicos.viaferrea(arcpy.env.nummapa)
# inegi_tematicos.zonaarenosa(arcpy.env.nummapa)

# # ----------------------------CARTOGRAFÍA librería conabio (Y:\GIS\MEXICO\VARIOS\conabio\WGS84)

# conabio.area_nat_protegida(arcpy.env.nummapa)
# conabio.clima_koppen(arcpy.env.nummapa)
# conabio.clima_olgyay(arcpy.env.nummapa)
# conabio.cuenca(arcpy.env.nummapa)
# conabio.edafologia(arcpy.env.nummapa)
# conabio.humedad(arcpy.env.nummapa)
# conabio.precip(arcpy.env.nummapa)
# conabio.subcuenca(arcpy.env.nummapa)
# conabio.subregion(arcpy.env.nummapa)
# conabio.zonaecol(arcpy.env.nummapa)


log.log(repet,u"FIN DE PROCESO")
tiempoprocfin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
log.log(repet,u"tiempo total de proceso de mapas: {}".format(tiempo.tiempo([tiempoprocini,tiempoprocfin])))

print (u"\n\n\n\nPROCESO SIG finalizado! \nNo es necesario guardar el mapa.")
print (u"Revisar archivo log para mayor informacion del proceso.")