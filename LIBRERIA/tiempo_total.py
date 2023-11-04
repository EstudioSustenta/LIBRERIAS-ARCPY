from datetime import datetime

def tiempo(tiempos):

    try:

        # Convertir cadenas de tiempo a objetos datetime
        tiempo_inicial = datetime.strptime(tiempos[0], "%Y-%m-%d %H:%M:%S")
        tiempo_final = datetime.strptime(tiempos[1], "%Y-%m-%d %H:%M:%S")

        # Calcular la diferencia de tiempo
        diferencia_tiempo = tiempo_final - tiempo_inicial

        # print("La diferencia de tiempo es: {}".format(diferencia_tiempo))

        return(diferencia_tiempo)

    except Exception as e:
        print (str(e))