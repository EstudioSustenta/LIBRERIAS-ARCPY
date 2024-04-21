# -*- coding: utf-8 -*-

# ----RUTINA PARA IMPRIMIR MAPAS DE UBICACIÓN A NIVEL PAIS, ESTADO, MUNICIPIO, REGIÓN, ZONA Y SITIO


# import sys
# ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/LIBRERIA/UTILERIAS"
# sys.path.append(ruta_libreria)
import arcpy
import UTILERIAS.UTIL_JSON as UJ
import UTILERIAS.Utilerias_shp as USH
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
from estados import sustedo as rnc
import UTILERIAS.UTILERIAS_PDF as PDF
import UTILERIAS.inegi_tematicos
reload(UTILERIAS.inegi_tematicos)
import UTILERIAS.inegi_tematicos as tematicos
reload(tematicos)
import UTILERIAS.conabio_tematicos as conabio
reload(conabio)
import UTILERIAS.inegi_complementos as compl
reload (compl)

# Proceso para inicializar cuadros de diálogo
import Tkinter as tk
import tkFileDialog
root = tk.Tk()
root.withdraw()

if __name__=="__main__":
    mxd = arcpy.mapping.MapDocument('CURRENT')                   # Obtener acceso al documento actual
else:
    mxd = arcpy.mapping.MapDocument('Y:/0_SIG_PROCESO/PLANTILLA.mxd')
df = arcpy.mapping.ListDataFrames(mxd)[0]
autor = "Gustavo Martinez Velasco"
sistema="Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"
rutasimbologia="Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/"
arcpy.env.numeromapa = 1

sustitucion = rnc()

def rutacarp():
    """
    Define, mediante un cuadro de diálogo, la ruta de la carpeta donde se guardarán
    los archivos y mapas de este proceso.
    guarda la ruta en un archivo json en la misma carpeta definida.
    """
    # print("Eligiendo carpeta iniciando...")
    lista=[]

    try:
        import os
        
        # Abre un cuadro de diálogo para seleccionar una carpeta
        carp_mapas = u"Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/"
        carpeta_cliente = tkFileDialog.askdirectory(initialdir=carp_mapas, title=u"Selecciona la carpeta destino de los mapas") + "/"
        arch_log = carpeta_cliente + u"00 archivo_log.txt"
        if carpeta_cliente:         # Verifica si el usuario seleccionó una carpeta
            adbas = "{}datos_basicos.json".format(carpeta_cliente)
            if os.path.exists(adbas):
                os.remove(adbas)
            (UJ.agdicson(adbas,"carpeta_proy", carpeta_cliente))
            (UJ.agdicson(adbas,"archivo_log",arch_log))
            (UJ.agdicson(adbas,"autor",autor))
            lista.extend([arch_log,adbas])
        else:
            print(u"No se seleccionó ninguna carpeta.")
    except Exception as e:
        print(u">> Error en 'rutacarp' {}".format(e))
    # print("Elección de carpeta terminada")
    return lista
    
def dbasi(arch_log,adbas):
    import sys
    ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/LIBRERIA/UTILERIAS"
    sys.path.append(ruta_libreria)
    import datos_basicos
    reload(datos_basicos)
    from datos_basicos import datosbasicos
    # Importar el módulo desde el paquete LIBRERIA utilizando importlib
    # dbas = importlib.import_module(u"LIBRERIA.datos_basicos")
    # from datos_basicos import datosbasicos
    # global log
    # log = importlib.import_module(u"LIBRERIA.archivo_log")
    ESU.log("iniciando proceso 'datos básicos'",arch_log,presalto=2)
    datosbasicos(arch_log,adbas) # define los datos básicos del proyecto y crea el archivo txt correspondiente
    ESU.log("Proceso 'datos básicos' finalizado",arch_log)
    ESU.log("--------------INICIO DE SECCIÓN LOG--------------------------",arch_log, presalto=2)

def cargalib():
    """
    Carga las librerías necesarias para la ejecución del script
    y carga la capa 'SISTEMA' y le da formato si no existe.
    """

    ESU.log("'cargalib' iniciando...",arch_log)

    # carga la capa principal para el sistema a analizar
    valores = {
        'mxd':              mxd,
        'df':               df,
        'shapefile':        sistema,
        'nombreshape':      "SISTEMA",
        'layer':            rutasimbologia + "SISTEMA.lyr",
        'transparencia':    20,
        'campo_rotulos':    'DESCRIP',
    }
    ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
    ESU.log(USH.zoom_extent(mxd,df,"SISTEMA",over=10),arch_log)
    ESU.log("'cargalib' finalizado\n\n",arch_log)



    # nota, para poder cargar las librería y que se genere el archivo .pyc adecuadamente, cada librería debe iniciar con la línea: # -*- coding: utf-8 -*-

def cargajson(adbas):
    return UJ.lodicson(adbas)

def mapaPais(dbasicos):
    """
    Proceso para generar mapa a nivel pais
    """
    carp_cliente=dbasicos['carpeta_proy']

    try:
        ESU.log("Iniciando proceso para 'pais'",arch_log,presalto=1)
        shapefile=dbasicos['rutamapadigital'] + "GEOPOLITICOS/ESTATAL decr185.shp"
        proyecto=dbasicos['proyecto']
        valorespais = {
            'mxd': mxd,
            'df': df,
            'shapefile': shapefile,
            'nombreshape': "Estados",
            'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/ESTATAL decr185.lyr",
            'transparencia': 50,
            'campo_rotulos': "NOM_ENT",
        }
        ESU.log(USH.carga_capa_y_formatea(valorespais),arch_log)
        ESU.log(USH.zoom_extent(mxd,df,valorespais['nombreshape'],over=10),arch_log)
        ESU.log(USH.formato_layout(mxd, proyecto, 'mapa de entidades federativas'),arch_log)
        ESU.log(USH.exportar(mxd, carp_cliente,'Pais',serial=True,jpg=False),arch_log,imprimir=False)
        ESU.log("Proceso para 'pais' finalizado",arch_log,presalto=0,imprimir=False)

    except Exception as e:
        ESU.log(">>>>> ERROR en mapaPais: {}".format(e),arch_log)
        
    finally:
        ESU.log(USH.borrainn(mxd,df),arch_log,postsalto=2)
    
def mapaEstatal(dbasicos):
    """
    Proceso para generar mapa del estado del proyecto
    """
    proyecto=dbasicos['proyecto']
    estado=dbasicos['estado']
    try:
        ESU.log("Iniciando proceso para 'estatal'",arch_log,presalto=1)
        valoresestado = {
            'mxd': mxd,
            'df': df,
            'shapefile': "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/GEOPOLITICOS/ESTATAL decr185.shp",
            'nombreshape': "Edo: {}".format(estado),
            'layer': "Y:/0_SIG_PROCESO/MAPAS/SIMBOLOGIA/ESTATAL decr185.lyr",
            'transparencia': 50,
            'campo_rotulos': "NOM_ENT",
        }
        ESU.log(USH.carga_capa_y_formatea(valoresestado),arch_log)
        filtr= """ "NOM_ENT" = '{}' """.format(estado)
        ESU.log(USH.fil_expr(mxd, valoresestado['nombreshape'], filtr),arch_log)
        ESU.log(USH.zoom_extent(mxd,df,valoresestado['nombreshape'],over=0),arch_log)
        valorescaminos = {
            'mxd': mxd,
            'df': df,
            'shapefile': rednalcaminos,
            'nombreshape': "Red Vial",
            'layer': rutasimbologia + "red_vial_wgs84utm.lyr",
            'transparencia': 50,
            'campo_rotulos': None,
        }
        ESU.log(USH.carga_capa_y_formatea(valorescaminos),arch_log)
        # filtr="""("JURISDI" = 'Ags.' OR "JURISDI" = 'Fed.') AND ("TIPO_VIAL" = 'Carretera' OR "TIPO_VIAL" = 'Boulevard')"""
        filtr="""("ADMINISTRA" = 'Federal' OR "ADMINISTRA" = 'Estatal' OR"ADMINISTRA" = 'Municipal')"""
        # filtr="""("ADMINISTRA" = 'Federal.' OR "ADMINISTRA" = 'Estatal.' OR"ADMINISTRA" = 'Municipal.') AND ("TIPO_VIAL" = 'Carretera' OR "TIPO_VIAL" = 'Boulevard')"""
        ESU.log(USH.fil_expr(mxd, valorescaminos['nombreshape'], filtr),arch_log)
        valoreslocurb = {
            'mxd': mxd,
            'df': df,
            'shapefile': "{}loc_urb.shp".format(rutascince2020),
            'nombreshape': "Localidades urbanas",
            'layer': rutasimbologia + "loc_urb.lyr",
            'transparencia': 50,
            'campo_rotulos': "NOMGEO",
        }
        ESU.log(USH.carga_capa_y_formatea(valoreslocurb),arch_log)
        ESU.log(USH.formato_layout(mxd, proyecto, 'mapa del estado de {}'.format(estado)),arch_log)
        ESU.log(USH.exportar(mxd, carpeta_proy,"Mapa Estatal",serial=True),arch_log)      

    except Exception as e:
        ESU.log(">>>>> ERROR, no se pudo ejecutar 'mapaEstatal': {}".format(e),arch_log)
    finally:
        ESU.log(USH.borrainn(mxd,df),arch_log)

def mapaMunicipal(dbasicos):

    # -------------------------------------------------------------------------------
    # Proceso para generar mapa municipal

    import sys
    ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/LIBRERIA/UTILERIAS"
    sys.path.append(ruta_libreria)

    arch_log=dbasicos['archivo_log']
    print(arch_log)
    ambito=dbasicos['ambito']
    try:
        
        tab = 1
        # ambito = dbasicos['ambito']
        ESU.log("Proceso 'mapaMunicipal' iniciando...",arch_log,presalto=2,tabuladores=tab)
        ESU.log("Proceso 'mapaMunicipal' iniciando para '{}'...".format(ambito),arch_log,tabuladores=tab)

        if ambito == "Urbano":
            # proceso si el sistema es urbano
            
            import urbano_nacional
            reload(urbano_nacional)
            urbano_nacional.proyurbano(dbasicos)
            
        elif ambito == "Rural":
            import rural_nacional
            # proceso si el sistema es rural
            rural_nacional.proyrural(dbasicos)
        else:
            ESU.log(">>>>>ERROR en mapa municipal, no se ha definido 'ambito'",arch_log,tabuladores=tab,imprimir=False)

    except Exception as e:
        ESU.log(">>>>> ERROR, no se pudo ejecutar 'mapaMunicipal': {}".format(e),arch_log)
        
    finally:
        ESU.log(USH.borrainn(mxd,df),arch_log)

def cuadrodeLocalizacion(dbasicos):
    import sys
    ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/LIBRERIA/UTILERIAS"
    sys.path.append(ruta_libreria)

    import cuadro_de_localizacion
    reload(cuadro_de_localizacion)
    from cuadro_de_localizacion import dwg
    # reload(dwg)
    
    # -------------------------------------------------------------------------------
    # Proceso para generar cuadros de construcción en formato dwg
    ESU.log("Iniciando proceso para cuadro de localización",arch_log, presalto=2)

    try:
        ESU.log(dwg(dbasicos),arch_log, imprimir=False)
        ESU.log("Proceso para cuadro de localización finalizado",arch_log)

    except Exception as e:
        ESU.log(">>>>>ERROR en 'cuadrodelocalización': {}".format(e),arch_log)
    finally:
        ESU.log(USH.borrainn(mxd,df),arch_log)

def servicios_urbanos(dbasicos):
    """
    Proceso para analizar servicios cercanos al sistema (5 minutos caminando a 5 km/hr)
    """
    import sys
    ruta_libreria = u"Q:/09 SISTEMAS INFORMATICOS/GIS_PYTON/SOPORTE_GIS/LIBRERIA/UTILERIAS"
    sys.path.append(ruta_libreria)
    import servicios as serv
    reload(serv)

    ambito=dbasicos['ambito']

    minutos = 5 # Define el radio (en minutos) para el análisis
    arch_log=dbasicos['archivo_log']
    try:
        if  ambito == "Urbano":
            ESU.log(u"Iniciando proceso de servicios urbanos",arch_log)
            ESU.log(serv.servicios(dbasicos, minutos),arch_log)
        elif ambito == "Rural":
            ESU.log(u"El proceso de servicios no se aplica al ámbito rural",arch_log)
        else:
            ESU.log(u">>>>>ERROR en 'servicios_urbanos', no se ha definido 'ambito'.",arch_log)
        ESU.log(u"Proceso 'servicios' finalizado",arch_log)

    except Exception as e:
        ESU.log(u">>>>> ERROR: no se pudo ejecutar 'servicio_urbanos'. {}".format(e),arch_log)
    finally:
        ESU.log(USH.borrainn(mxd,df),arch_log)


#========================================INICIO DEL PROCESO=============================================


datos_rutacarp = rutacarp()
arch_log=datos_rutacarp[0]
adbas=datos_rutacarp[1]

dbasi(arch_log,adbas)
cargalib()
dbasicos = cargajson(adbas)

#-----definición de datos generales para todo el proyecto-----
estado=dbasicos['estado']

if estado in sustitucion:
    estadoSUS = sustitucion[estado]
else:
    estadoSUS = estado
    
# ambito=dbasicos['ambito']
carpeta_proy=dbasicos['carpeta_proy']
localidad=dbasicos['localidad']
municipio=dbasicos['municipio']
archivo_log=dbasicos['archivo_log']
colonia=dbasicos['colonia']
ambito=dbasicos['ambito']
rutascince2020 = "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/cartografia/".format(estado)
rutaconabio="Y:/GIS/MEXICO/VARIOS/conabio/WGS84/"
rutamapadigital="Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/"
rednalcaminos="Y:/GIS/MEXICO/VARIOS/INEGI/RED NACIONAL DE CAMINOS 2017/conjunto_de_datos/{0}/Caminos_RNC_{0}.shp".format(estadoSUS)
rutadatosgis="Y:/GIS/MEXICO/VARIOS/"
ESU.log(UJ.agdicson(adbas,"rednalcaminos",rednalcaminos), arch_log)
ESU.log(UJ.agdicson(adbas,"rutascince2020",rutascince2020), arch_log)
ESU.log(UJ.agdicson(adbas,"rutasimbologia",rutasimbologia), arch_log)
ESU.log(UJ.agdicson(adbas,"rutamapadigital",rutamapadigital), arch_log)
ESU.log(UJ.agdicson(adbas,"sistema","SISTEMA"), arch_log)
ESU.log(UJ.agdicson(adbas,"rutaconabio",rutaconabio), arch_log)
ESU.log(UJ.agdicson(adbas,"rutadatosgis",rutadatosgis), arch_log)
ESU.log(UJ.agdicson(adbas,"archsistema",sistema), arch_log)


dbasicos = cargajson(adbas)
dbasicos['mxd']=mxd
dbasicos['df']=df


ESU.log(USH.borrainn(mxd, df),arch_log)


# # ----------------------------MAPAS BÁSICOS

# mapaPais(dbasicos)
# mapaEstatal(dbasicos)
# mapaMunicipal(dbasicos) 
# cuadrodeLocalizacion(dbasicos)
# servicios_urbanos(dbasicos)

# # ----------------------------CARTOGRAFÍA MAPAS TEMÁTICOS INEGI (Y:\GIS\MEXICO\VARIOS\INEGI)

creajson = True
# ESU.log(tematicos.curvasdenivel(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.usodesuelo(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.hidrologia(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.lineasElectricas(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.malpais(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.pantano(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.pistadeAviacion(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.presa(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.rasgoarqueologico(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.salina(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.viaferrea(dbasicos, creajson=True),arch_log,presalto=2)
# ESU.log(tematicos.zonaarenosa(dbasicos, creajson=True),arch_log,presalto=2)

# # ----------------------------CARTOGRAFÍA librería conabio (Y:\GIS\MEXICO\VARIOS\conabio\WGS84)

# ESU.log(conabio.area_nat_protegida(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.clima_koppen(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.clima_olgyay(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.cuenca(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.edafologia(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.humedad(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.precip(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.subcuenca(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.subregion(dbasicos,creajson),arch_log,presalto=2)
# ESU.log(conabio.zonaecol(dbasicos,creajson),arch_log,presalto=2)


# ----------------------------CARTOGRAFÍA INEGI COMPLEMENTOS
if ambito == "Urbano":
    compl.denue(dbasicos,creajson)
    pass
else:
    ESU.log(u"El ambito es rural, no se ejecutó el análisis DENUE",arch_log)

# inegi_comp.analisis_manz() # el segundo parámetro de la función es para definir la distancia de análisis
ESU.log(PDF.join(carpeta_proy, "Mapas", borrar=True),arch_log,imprimir=False,presalto=1)


print (u"\n\nPROCESO SIG finalizado! \nNo es necesario guardar el mapa.")
print (u"Revisar archivo log para mayor informacion del proceso.")
