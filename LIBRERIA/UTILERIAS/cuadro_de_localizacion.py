# -*- coding: utf-8 -*-
"""
Genera archivos dwg para el cuadro de localización del proyecto.
"""

import arcpy
import UTILERIAS.Utilerias_shp as USH
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
import os

def dwg(dbasicos):
    """
    Genera los archivos para el cuadro de construcción en formato dwg para autocad
    """
    arcpy.env.overwriteOutput = True
    valores={}
    arch_log=dbasicos['archivo_log']
    ambito=dbasicos['ambito']
    scince=dbasicos['rutascince2020']
    carpeta_proy=dbasicos['carpeta_proy']
    estado=dbasicos['estado']
    carpeta_temp = carpeta_proy + "temp/"
    archivodwg=carpeta_proy + "cuadro_de_localizacion.dwg"
    capasist="SISTEMA"

    mensaje="Reporte dwg; "
    arch_exp=[]

    mensaje += u"Carpeta temporal: "
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
        ESU.log("Iniciando libreria 'dxf'",arch_log, presalto=2, imprimir=False)
        
        def ambito_urbano():
            mensaje = "Reporte 'ambito_urbano': "
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
                mensaje += USH.clipbuffer(valores)
                if os.path.exists(archivoclip):
                    arch_exp.append(archivoclip)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
                else:
                    ESU.log(">>>>>ERROR en cuadro de localización -urbano, no se ha agregado '{}'".format(archivoclip),arch_log)
            arch_exp.append(capasist)
            datos=[arch_exp, mensaje]
            return datos

        def ambito_rural():
            mensaje = "Reporte 'ambito_rural': "
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
                    mensaje += USH.clipbuffer(valores)
                    if os.path.exists(archivoclip):
                        arch_exp.append(archivoclip)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
                    else:
                        mensaje += ">>>>>ERROR en cuadro de localización -rural, no se ha agregado '{}'. ".format(archivoclip)
                if os.path.exists(archivobuff):
                    arch_exp.append(archivobuff)    # esta línea agrega las rutas de los archivos shp que se van a exportar posteriormente a dwg
            arch_exp.append(capasist)
            datos=[arch_exp, mensaje]
            return datos

        if ambito == "Urbano":
            mensaje+= "Iniciando libreria 'ambito urbano'. "
            datos=ambito_urbano()
        elif ambito == "Rural":
            mensaje += "Iniciando libreria 'ambito rural'. "
            datos=ambito_rural()
        else:
            mensaje+= ">>>>>ERROR en cuadro de localización: no se ha definido 'ambito' adecuadamente"
            arch_exp=[]

        arch_exp= datos[0]
        mensaje += datos[1]

        archivos = ';'.join(arch_exp)
        mensaje += USH.exporta_dwg(archivodwg, archivos)

    except Exception as e:
        mensaje=">>>>>ERROR en 'cuadro de localizacion' {}".format(e)
        ESU.log(mensaje,arch_log,imprimir=True)

    finally:
        for arch in arch_exp:
                if arch != capasist:
                    arcpy.Delete_management(arch)
                    mensaje += "Se ha eliminado {}. ".format(arch)
        mensaje += "Finalizando libreria 'dxf'. "
        xmlarch = archivodwg + '.xml'
        if os.path.exists(xmlarch):
            os.remove(xmlarch)
            mensaje += "Se ha eliminado el archivo '{}'. ".format(xmlarch)
        return mensaje

if __name__ == '__main__':

    dbasicos={
        "carpeta_proy" : "Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/",
        "rutascince2020" : "Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/Aguascalientes/cartografia/",
        "archivo_log" : "Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/00 archivo_log alterno 2024-03-21 20-15-48.txt",
        "ambitourb" : "Urbano", 
        }
    dbasicos["buffer_in"]="Y:/0_SIG_PROCESO/00 GENERAL/SISTEMA.shp"
    print(dwg(dbasicos))
