import os

carpeta_base = 'Y:/GIS/MEXICO/VARIOS/INEGI/CENSALES/SCINCE 2020'
extension_a_eliminar = '.lock'

def eliminar_archivos_lock(ruta_carpeta):
    for ruta_actual, _, archivos in os.walk(ruta_carpeta):
        for archivo in archivos:
            if archivo.endswith(extension_a_eliminar):
                ruta_completa = os.path.join(ruta_actual, archivo)
                os.remove(ruta_completa)
                print("Archivo eliminado: {}".format(ruta_completa))

eliminar_archivos_lock(carpeta_base)
