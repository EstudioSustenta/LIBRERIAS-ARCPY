
# rutina para copiar y pegar en funciones para que calcule el tiempo -ver librerías existentes-


import datetime


tiempo = importlib.import_module(u"LIBRERIA.tiempo_total")
tiempoidenini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    tiempoidenfin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de librería 'identity_sistema': {}".format(tiempo.tiempo([tiempoidenini,tiempoidenfin])))

