# -*- coding: utf-8 -*-

from dbfread import DBF

def recuperacamposdbf(archivo_dbf, campos, FIDS):
    diccionario = []
    for FID in FIDS:
        try:
            if not isinstance(FID, int):
                FID = 0

            valores_campos = {}

            codificaciones = {
                "conjunto_de_datos/denue_wgs84z13.dbf": "latin-1",
                "USO DE SUELO INEGI SERIE IVCopy.dbf": "ISO-8859-1",
            }

            for codigo in codificaciones:
                if codigo in archivo_dbf:
                    codificacion = codificaciones[codigo]
                    break
                else:
                    codificacion = 'utf-8'

            with DBF(archivo_dbf, encoding=codificacion) as dbf:
                for i, registro in enumerate(dbf):
                    if i == FID:
                        valores_campos['FID'] = FID
                        for campo in campos:
                            if campo in dbf.field_names:
                                resultado = registro[campo]
                                if isinstance(resultado, (float, int)):
                                    resultado = str(resultado)
                                valores_campos[campo] = resultado
                            else:
                                valores_campos[campo] = ">>>>>ERROR, No existe en archivo DBF"
                        break
                diccionario.append(valores_campos)
        except Exception as e:
            return ">>>>>ERROR ejecutando 'recuperacamposdbf' {}.".format(e)
    return diccionario

def cant_de_registros(archivo):
    try:

        # Contador para el número de registros
        numero_de_registros = 0

        # Leer el archivo DBF y contar los registros
        with DBF(archivo) as dbf:
            for _ in dbf:
                numero_de_registros += 1
        return numero_de_registros
    except:
        return 1000000
    
    from dbfread import DBF

def obtener_distancias(archivo_dbf,codificacion):
    
    """
    Función para obtener un diccionario con el número de registro como clave
    y el valor del campo 'distancia' como valor para todos los registros
    de un archivo DBF.

    Args:
    - archivo_dbf: Ruta del archivo DBF.

    Returns:
    - Un diccionario con el número de registro como clave y el valor del campo 'distancia' como valor.
    """
    distancias = {}
    try:
        with DBF(archivo_dbf, encoding=codificacion) as dbf:
            for i, registro in enumerate(dbf):
                distancias[i] = registro.get('distancia', 'Valor no disponible')
    except Exception as e:
        print("Error al leer el archivo DBF:", e)
    return distancias



if __name__=="__main__":

    # Ruta al archivo DBF
    archivo_dbf = "Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84/USO DE SUELO INEGI SERIE IVCopy.dbf"
    # Campos que deseas recuperar
    campos = ['CVE_UNION', 'ECOS_VEGE', 'DESVEG', 'FORMACION', 'HECTARES', 'CVE_FAO', 'VEG_FORES', 'INFYS_0409', 'Sup_ha', 'Sup_hasa']

    resultados = recuperacamposdbf(archivo_dbf)
    print(resultados)
