from dbfread import DBF

# Ruta al archivo DBF
archivo_dbf = "Y:/02 CLIENTES (EEX-CLI)/00 prueba impresion/02/temp/USO DE SUELO INEGI SERIE IV_temp.dbf"
n = 20

# Número de registro que deseas recuperar (ten en cuenta que los índices de los registros comienzan desde 0)
numero_registro = n - 1

# Campos que deseas recuperar
campos = ['ECOS_VEGE', 'VEG_FORES']

# Lista para almacenar los valores de los campos
valores_campos = []

# Leer el archivo DBF y encontrar el registro deseado
with DBF(archivo_dbf) as dbf:
    for i, registro in enumerate(dbf):
        if i == numero_registro:
            # Obtener los valores de los campos especificados
            for campo in campos:
                valores_campos.append(registro[campo])
            break  # Salir del bucle una vez que se encuentra el registro deseado

# Imprimir los valores de los campos
print(u"Valores de los campos 'campo1' y 'campo2' del registro", numero_registro + 1, ":", valores_campos)
