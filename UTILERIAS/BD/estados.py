# -*- coding: utf-8 -*-

'''
Esta función regresa listas de valores para trabajar con datos INEGI
estadosact = entidades federativas
estorigdest = diccionario de entidades federativas con nombre de carpeta inegi
shapes = shapefiles SCINCE 2020
tablasdbf = tablas dbf asociadas a cada shapefile
'''
def estados():
    estados = [
        'Aguascalientes',
        # 'Baja California',
        # 'Baja California Sur',
        # 'Campeche',
        # 'Chiapas',
        # 'Chihuahua',
        # 'Ciudad de Mexico',
        # 'Coahuila',
        # 'Colima',
        # 'Durango',
        # 'Guanajuato',
        # 'Guerrero',
        # 'Hidalgo',
        # 'Jalisco',
        # 'Mexico',
        # 'Michoacan de Ocampo',
        # 'Morelos',
        # 'Nayarit',
        # 'Nuevo Leon',
        # 'Oaxaca',
        # 'Puebla',
        # 'Queretaro',
        # 'Quintana Roo',
        # 'San Luis Potosi',
        # 'Sinaloa',
        # 'Sonora',
        # 'Tabasco',
        # 'Tamaulipas',
        # 'Tlaxcala',
        # 'Veracruz de Ignacio de la Llave',
        # 'Yucatan',
        # 'Zacatecas'
    ]
    
    return estados

def estorigdest():
    estOrigDest = {
            'Aguascalientes'                    : '01_AGS',
            'Baja California'                   : '02_BC',
            'Baja California Sur'               : '03_BCS',
            'Campeche'                          : '04_CAMP',
            'Coahuila'                          : '05_COAH',
            'Colima'                            : '06_COL',
            'Chiapas'                           : '07_CHIS',
            'Chihuahua'                         : '08_CHIH',
            'Ciudad de Mexico'                  : '09_CDMX',
            'Durango'                           : '10_DGO',
            'Guanajuato'                        : '11_GTO',
            'Guerrero'                          : '12_GRO',
            'Hidalgo'                           : '13_HGO',
            'Jalisco'                           : '14_JAL',
            'Mexico'                            : '15_MEX',
            'Michoacan de Ocampo'               : '16_MICH',
            'Morelos'                           : '17_MOR',
            'Nayarit'                           : '18_NAY',
            'Nuevo Leon'                        : '19_NL',
            'Oaxaca'                            : '20_OAX',
            'Puebla'                            : '21_PUE',
            'Queretaro'                         : '22_QRO',
            'Quintana Roo'                      : '23_Q_ROO',
            'San Luis Potosi'                   : '24_SLP',
            'Sinaloa'                           : '25_SIN',
            'Sonora'                            : '26_SON',
            'Tabasco'                           : '27_TAB',
            'Tamaulipas'                        : '28_TAMS',
            'Tlaxcala'                          : '29_TLAX',
            'Veracruz de Ignacio de la Llave'   : '30_VER',
            'Yucatan'                           : '31_YUC',
            'Zacatecas'                         : '32_ZAC',
            }
    return estOrigDest

def shapes():
    shapes = [
        'ageb_urb',
        'eje_vial',
        'estatal',
        'loc_rur',
        'loc_urb',
        'manzana',
        'municipal',
        'servicios_a',
        'servicios_l',
        'servicios_p',
            ]
    return shapes

def tablasdbf():
    
    tablasdbf = [
    'caracteristicas_economicas.dbf',
    'discapacidad.dbf',
    'educacion.dbf',
    'etnicidad.dbf',
    'fecundidad.dbf',
    'hogares_censales.dbf',
    'migracion.dbf',
    'mortalidad.dbf',
    'poblacion.dbf',
    'religion.dbf',
    'servicios_de_salud.dbf',
    'situacion_conyugal.dbf',
    'vivienda.dbf'
               ]
    return tablasdbf

