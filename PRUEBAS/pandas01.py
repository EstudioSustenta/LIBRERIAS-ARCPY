import pandas as pd
from dbfread import DBF

archtr1 = "cpv2020_manzana_viviendaCopy"
estado = 'Yucatán'
archivo1 = u"Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020/{}/tablas/{}.dbf".format(estado,archtr1)
expresion = "[VIV4_R] + [VIV5_R]"

valores = {'archivo1' : archivo1,
           'campo' : "marg_vi",
           'tipo' : 'FLOAT',
           'precision' : 3,
           'long' : "",
           'expresion' : expresion,
           'tipoexp' : "VB",
           'bloquecodigo' : ""
           }

def calc_camp_compl(valores):
    archivo = valores['archivo1'.encode('latin-1')]
    print("ARCHIVO >>> " + valores['archivo1'])
    table = DBF(archivo, encoding='latin-1')
    df = pd.DataFrame(iter(table))

    # Función personalizada para aplicar a las columnas 'pob1' y 'pob2'
    def nueva_columna(row):
        # Verifica si ambas columnas son mayores que -1
        if row['pob1'] > -1 and row['pob2'] > -1:
            return row['pob1'] + row['pob2']
        else:
            return None  # O cualquier valor predeterminado que desees para los casos en que no se cumpla la condición

    # Aplica la función a las columnas 'pob1' y 'pob2' para crear la nueva columna 'nueva_columna'
    df['nueva_columna'] = df.apply(nueva_columna, axis=1)

    return df
