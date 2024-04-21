# -*- coding: utf-8 -*-

'''
Esta función regresa listas de valores para trabajar con datos INEGI
\n estadosact = entidades federativas
\n estorigdest = diccionario de entidades federativas con nombre de carpeta inegi
\n shapes = shapefiles SCINCE 2020
\n tablasdbf = tablas dbf asociadas a cada shapefile
'''
def estados():
    estados = [
        # 'Aguascalientes',
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

def estorigdest1():
    estOrigDest = {
            'Aguascalientes'                    : 'AGS.',
            'Baja California'                   : 'B.C.',
            'Baja California Sur'               : 'B.C.S.',
            'Campeche'                          : 'CAMP.',
            'Coahuila'                          : 'COAH.',
            'Colima'                            : 'COL.',
            'Chiapas'                           : 'CHIS.',
            'Chihuahua'                         : 'CHIH.',
            'Ciudad de Mexico'                  : 'D.F.',
            'Durango'                           : 'DGO.',
            'Guanajuato'                        : 'GTO.',
            'Guerrero'                          : 'GRO.',
            'Hidalgo'                           : 'HGO.',
            'Jalisco'                           : 'JAL.',
            'Mexico'                            : 'EDO.MEX.',
            'Michoacan de Ocampo'               : 'MICH.',
            'Morelos'                           : 'MOR.',
            'Nayarit'                           : 'NAY.',
            'Nuevo Leon'                        : 'N.L.',
            'Oaxaca'                            : 'OAX.',
            'Puebla'                            : 'PUE.',
            'Queretaro'                         : 'QRO.',
            'Quintana Roo'                      : 'Q.R.',
            'San Luis Potosi'                   : 'S.L.P.',
            'Sinaloa'                           : 'SIN.',
            'Sonora'                            : 'SON.',
            'Tabasco'                           : 'TAB.',
            'Tamaulipas'                        : 'TAMS.',
            'Tlaxcala'                          : 'TLAX.',
            'Veracruz de Ignacio de la Llave'   : 'VER.',
            'Yucatan'                           : 'YUC.',
            'Zacatecas'                         : 'ZAC.',
            }
    return estOrigDest

def sustedo():
    """
    Proporciona valores para sustituir carpetas
    en la red nacional de caminos, numeros locos y otras carpetas
    """
    sustitucion={
        "Aguascalientes"                   : "Aguascalientes",
        "Baja California"                  : "Baja California",
        "Baja California Sur"              : "Baja California Sur",
        "Campeche"                         : "Campeche",
        "Chiapas"                          : "Chiapas",
        "Chihuahua"                        : "Chihuahua",
        "Ciudad de México"                 : "Ciudad de Mexico",
        "Coahuila"                         : "Coahuila",
        "Colima"                           : "Colima",
        "Durango"                          : "Durango",
        "Guanajuato"                       : "Guanajuato",
        "Guerrero"                         : "Guerrero",
        "Hidalgo"                          : "Hidalgo",
        "Jalisco"                          : "Jalisco",
        "México"                           : "Mexico",
        "Michoacán de Ocampo"              : "Michoacan",
        "Morelos"                          : "Morelos",
        "Nayarit"                          : "Nayarit",
        "Nuevo León"                       : "Nuevo Leon",
        "Oaxaca"                           : "Oaxaca",
        "Puebla"                           : "Puebla",
        "Querétaro"                        : "Queretaro",
        "Quintana Roo"                     : "Quintana Roo",
        "San Luis Potosí"                  : "San Luis Potosi",
        "Sinaloa"                          : "Sinaloa",
        "Sonora"                           : "Sonora",
        "Tabasco"                          : "Tabasco",
        "Tamaulipas"                       : "Tamaulipas",
        "Tlaxcala"                         : "Tlaxcala",
        "Veracruz de Ignacio de la Llave"  : "Veracruz",
        "Yucatán"                          : "Yucatan",
        "Zacatecas"                        : "Zacatecas",
        }
    return sustitucion


if __name__ == "__main__":
    sust= sustedo()
    print(sust["Veracruz de Ignacio de la Llave"])