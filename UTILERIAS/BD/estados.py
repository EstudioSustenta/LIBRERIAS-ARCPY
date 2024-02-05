# -*- coding: utf-8 -*-

'''
Esta función regresa las entidades federativas activas para trabajar con otras librerías
'''
def estadosact():
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
