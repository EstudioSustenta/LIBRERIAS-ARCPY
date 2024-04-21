import traceback

def funcion_con_error():
    # Aquí va tu código que puede lanzar una excepción
    resultado = 1 / 0  # Genera una excepción ZeroDivisionError

def obtener_numero_de_linea():
    try:
        funcion_con_error()
    except Exception as e:
        # Obtener la traza de la pila
        traza_de_pila = traceback.extract_tb(e.__traceback__)
        # Obtener el número de línea del primer marco de la pila
        numero_de_linea = traza_de_pila[-1].lineno
        return numero_de_linea

# Llamar a la función que puede lanzar una excepción
linea_del_error = obtener_numero_de_linea()
if linea_del_error is not None:
    print("El error ocurrió en la línea:", linea_del_error)
else:
    print("No se produjo ningún error.")
