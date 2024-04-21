# -*- coding: utf-8 -*-

# SCRIPT PARA ANALIZAR LOS servicios IDENTIFICADOS POR EL INEGI EN EL SCINCE 2020.
# FUNCION: A NIVEL NACIONAL.

import arcpy
import UTILERIAS.ESUSTENTA_UTILERIAS as ESU
import UTILERIAS.Utilerias_shp as USH
import os

def servicios(dbasicos, minutos):
        """
        Crea mapas de los servicios urbanos para el sistema
        """
        try:
                mxd = dbasicos['mxd']
                df = dbasicos['df']
                carpeta_proy = dbasicos['carpeta_proy']
                scince = dbasicos['rutascince2020']
                arch_log = dbasicos['archivo_log']
                sistema = dbasicos['sistema']
                simbologia=dbasicos['rutasimbologia']
                proyecto=dbasicos['proyecto']
                radio = 84 * minutos
                manzanas = scince + 'manzana_localidad.shp'
                

                ESU.log('Iniciando proceso de servicios urbanos',arch_log)

                # -------------------------------------------------------------------------------
                # Proceso para generar mapa del municipio:

                # Carga capa de servicios correspondiente a la ciudad
                # capaservicios = (u"{}/servicios_p.shp".format(scince))

                carpeta_temp = carpeta_proy + '/temp/'
                if not os.path.exists(carpeta_temp):
                        os.makedirs(carpeta_temp)
                
                valclipbuff = {
                        "buffer_in" : sistema,            #capa de la que se genera el buffer
                        "distbuffer" : radio,       #radio del buffer
                        "buffer_arch" : carpeta_temp + 'buffer_arch.shp',          #nombre del archivo resultado del buffer (ruta completa)
                        "caparecortar" : manzanas,         #capa que se va a recortar (ruta completa)
                        "archivoclip" : carpeta_temp + 'archivoclip.shp',          #nombre del archivo resultado del clip (ruta completa)
                        }
                archborr = [
                        valclipbuff['buffer_arch'],
                        valclipbuff['archivoclip'],
                        ]
                ESU.log(USH.clipbuffer(valclipbuff),arch_log)
                
                #-----manzanas-----
                valores = {
                                'mxd': mxd,
                                'df': df,
                                'shapefile': manzanas,
                                'nombreshape': "Manzanas",
                                'layer': simbologia + "manzana_localidad.lyr",
                                'transparencia': 70,
                                'campo_rotulos': None,
                                }
                ESU.log(USH.carga_capa_y_formatea(valores),arch_log)

                #-----manzanas recortadas-----
                valores['shapefile']=valclipbuff['archivoclip']
                valores['nombreshape']= 'Radio {} minutos'.format(minutos)
                valores['layer']= simbologia + "manzana_localidad.lyr"
                valores['transparencia']= 40
                ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
                ESU.log(USH.zoom_extent(mxd,df,valores['nombreshape'],over=5),arch_log)

                #-----servicios punto-----
                valores['shapefile'] = scince + 'servicios_p.shp'
                valores['nombreshape'] = 'Serv. punto'
                valores['layer'] = simbologia + 'servicios_p.lyr'
                valores['transparencia'] = 20
                valores['campo_rotulos'] = 'NOMGEO'
                
                ESU.log(USH.carga_capa_y_formatea(valores),arch_log)

                #-----servicios linea-----
                valores['shapefile'] = scince + 'servicios_l.shp'
                valores['nombreshape'] = 'Serv. linea'
                valores['layer'] = simbologia + 'servicios_l.lyr'
                valores['transparencia'] = 20
                valores['campo_rotulos'] = 'NOMGEO'
                ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
                expr=u"""("NOMGEO" = 'Paso a Desnivel' OR "NOMGEO" = 'Paso Desnivel' OR "NOMGEO" = 'Puente' OR "NOMGEO" = 'Puente Peatonal' OR "NOMGEO" = 'Puente Vehicular')"""
                ESU.log(USH.fil_expr(mxd,valores['nombreshape'],expr),arch_log)

                #-----servicios area-----
                valores['shapefile'] = scince + 'servicios_a.shp'
                valores['nombreshape'] = 'Serv. area'
                valores['layer'] = simbologia + 'servicios_a.lyr'
                valores['transparencia'] = 50
                valores['campo_rotulos'] = 'NOMGEO'
                ESU.log(USH.carga_capa_y_formatea(valores),arch_log)
                expr=u"""NOT ("NOMGEO" = 'Ninguno' OR "NOMGEO" = 'No Aplica' OR "NOMGEO" = 'None' OR "NOMGEO" = 'SIN NOMBRE')"""
                ESU.log(USH.fil_expr(mxd,valores['nombreshape'],expr),arch_log)

                ESU.log(USH.formato_layout(mxd, proyecto, 'Servicios {} minutos caminando'.format(minutos)),arch_log)
                ESU.log(USH.exportar(mxd,carpeta_proy,"Servicios",serial=True),arch_log)

                ESU.log(USH.borrainn(mxd,df),arch_log)
                return "Proceso servicios ejecutado satisfactoriamente"

        except Exception as e:
                ESU.log(USH.borrainn(mxd,df),arch_log)
                return ">>>>>ERROR en 'servicios': {}".format(e)
        finally:
                for archi in archborr:
                        ESU.log(USH.borrashp(archi),arch_log)
