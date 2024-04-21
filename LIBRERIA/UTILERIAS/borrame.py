


def curvasdeNivel(nummapa):
    #----------------->CURVAS DE NIVEL<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:

        log.log(repet,u"Proceso 'curvasdeNivel' iniciando...")

            # mapa
        capas =  [u"Curvas de nivel"]
        rutas =  [u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"]
        tipo = u"municipal"
        ncampo =  [u"ALTURA"]
        nummapa = arcpy.env.nummapa
        tit = "Curvas de nivel"
        tit_unicode = tit.decode('utf-8')

        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit_unicode, ordinal)
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'curvasdeNivel'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'curvasdeNivel' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet -1

def hidro():

    #----------------->HIDROLOGÍA<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:

        log.log(repet,u"Proceso 'hidrología' iniciando...")

            # mapa
        capas =  [u"Corrientes de agua", u"Cuerpos de agua"]
        # capas =  [u"Cuerpos de agua"]
        rutaor = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
        rutas = [rutaor, rutaor]
        # rutas = [rutaor]
        tipo = u"municipal"
        ncampo =  [u"NOMBRE", u"NOMBRE"]
        # ncampo =  [u"NOMBRE"]

        nummapa = arcpy.env.nummapa
        

            # near a corrientes de agua
        n=0
        rutaorigen = rutaor + u"/"
        capa = capas[n]
        distancia = 200
        campo = u"NEAR_DIST"
        valor = -1
        camporef = ncampo[n]
        archivo = capa + u" near"
        cantidad = 20
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)
        n = n + 1

            # near a cuerpos de agua
        rutaorigen = rutaor + u"/"
        capa = capas[n]
        distancia = 50
        campo = u"NEAR_DIST"
        valor = -1
        camporef = ncampo[n]
        archivo = capa + u" near"
        cantidad = 20
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tit = u"Hidrología"
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'hidrología'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'hidrología' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def lineasElectricas(nummapa):
    
    #----------------->LINEAS DE TRANSMISIÓN ELECTRICA<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:
    
        log.log(repet,u"Proceso 'lineasElectricas' iniciando...")

            # mapa
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capas =  [u"Linea de transmision electrica", u"Planta generadora", u"Subestacion electrica"]
        rutaor = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"
        rutas = [rutaor, rutaor, rutaor]
        ncampo =  [u"TIPO", u"NOMBRE", u"NOMBRE"]       # Esta variable se usa para los rótulos de los elementos gráficos en el mapa
        tit = u"Infraestructura eléctrica de alta tensión"


            # near primera capa
        n=0
        rutaorigen = rutaor + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # near segunda capa
        n=1
        rutaorigen = rutaor + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # near tercera capa
        n=2
        rutaorigen = rutaor + u"/"                   # Ruta del archivo a analizar
        capa = capas[n]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapas

        tipo = u"estatal"
        nummapa = arcpy.env.nummapa
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

        tipo = u"municipal"
        nummapa = arcpy.env.nummapa
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'lineasElectricas'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'lineasElectricas' finalizado!...\n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def malpais(nummapa):
    #-----------------> MALPAIS<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:

        log.log(repet,u"Proceso 'malpais' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84"      # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Malpais.shp"                                          # archivo a identificar
        capa_salida = u"Malpais"                                         # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CODIGO"]             # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CODIGO DE IDENTIFICACION"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Malpais"]
        rutas = [rutaCl]
        ncampo = [camposCons[1]]                                              # campo para el rótulo
        tipo = u"estatal"                                                # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 
        tit = u"MALPAIS INEGI SERIE IV"                                  # título del mapa en el layout
        ordinal = 4                 

            # near                  
        rutaorigen = rutaCl + u"/"                                       # Ruta del archivo a analizar
        capa = capas[0]                                                 # Capa a analizar
        distancia = 1000                                                # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                                             # campo donde se guarda la distancia al sistema
        valor = -1                                                   # valor a eliminar del campo 'campo'
        n=0                 
        camporef = ncampo[n]                                            # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                                        # nombre del archivo de texto a generar
        cantidad = 20                                                   # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'malpais'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'malpais' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def pantano(nummapa):
    #-----------------> PANTANO<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")

    try:

        log.log(repet,u"Proceso 'pantano' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Pantano.shp" # archivo a identificar
        capa_salida = u"Pantano" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA"]   # campos a imprimi en el archivo de identidad
        dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN"] # descriptores para los campos en el archivo txt de salida
        
        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)
        
            # mapa
        capas =  [u"Pantano"]
        rutas = [rutaCl]
        ncampo = [camposCons[1]]                    # campo para el rótulo
        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        tit = u"PANTANOS INEGI SERIE IV"             # título del mapa en el layout
        ordinal = 4
        
        
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'pantano'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'pantano' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def pistadeAviacion(nummapa):
    #-----------------> PISTA DE AVIACIÓN<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")


    try:

        log.log(repet,u"Proceso 'pistadeAviacion' iniciando...")

            # tabla
        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Pista de aviacion.shp" # archivo a identificar
        capa_salida = u"Pista de aviacion" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"CONDICION", u"TIPO"] # campos a escribir en el archivo
        dAlter = [u"IDENTIFICADOR GEOGRÁFICO", u"CLAVE DE IDENTIFICACIÓN", u"NOMBRE", u"CONDICIÓN", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Pista de aviacion"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        tit = u"PISTAS DE AVIACIÓN"                 # título del mapa en el layout
        ordinal = 5
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos

        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'pistadeAviacion'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'pistadeAviacion' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def presa(nummapa):

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    #-----------------> PRESA<------------------------------------------

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:
    
        log.log(repet,u"Proceso 'presa' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Presa.shp" # archivo a identificar
        capa_salida = u"Presa" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"CONDICION"] # campos a escribir en el archivo
        dAlter = [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"CONDICION"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Presa"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Presa".upper()                      # título del mapa en el layout


            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)  

        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        
    
    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'presa'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'presa' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def rasgoArqueologico(nummapa):

    #-----------------> RASGO ARQUEOLOGICO<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'rasgoArqueologico' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Rasgo arqueologico.shp" # archivo a identificar
        capa_salida = u"Rasgo arqueologico" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            # mapa
        capas =  [u"Rasgo arqueologico"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Rasgo arqueologico".upper()          # título del mapa en el layout
            
            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 4
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'rasgoArqueologico'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'rasgoArqueologico' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def salina(nummapa):

    #-----------------> SALINA<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'salina' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Salina.shp" # archivo a identificar
        capa_salida = u"Salina" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"NOMBRE", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"NOMBRE", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Salina"]
        rutas = [rutaCl]
        ncampo = [camposCons[2]]                          # campo para el rótulo
        tit = u"Salina".upper()                      # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 3
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'salina'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'salina' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def viaferrea(nummapa):

    #-----------------> VIA FERREA<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Vía Ferrea' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Via ferrea.shp" # archivo a identificar
        capa_salida = u"Via ferrea" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CONDICION", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CONDICION", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        # idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Via ferrea"]
        rutas = [rutaCl]
        ncampo = [camposCons[3]]                          # campo para el rótulo
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                       # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'viaferrea'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))

    log.log(repet,u"Proceso 'Via ferrea' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

def zonaarenosa(nummapa):

    #-----------------> ZONA ARENOSA<------------------------------------------

    arcpy.env.repet = arcpy.env.repet + 1
    repet = arcpy.env.repet

    tiempo_mapa_ini = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    

    try:

        log.log(repet,u"Proceso 'Zona arenosa' iniciando...")

            # tabla

        rutaCl = u"Y:/GIS/MEXICO/VARIOS/INEGI/Mapa Digital 6/WGS84" # ruta del archivo a identificar (sin el slash final)
        capaCl = u"Zona arenosa.shp" # archivo a identificar
        capa_salida = u"Zona arenosa" # capa a crear en el mapa
        camposCons =  [u"GEOGRAFICO", u"IDENTIFICA", u"CALI_REPR", u"TIPO"] # campos a escribir en el archivo
        dAlter =  [u"IDENTIFICADOR GEOGRAFICO", u"CLAVE DE IDENTIFICACION", u"CALIDAD DE REPRESENTACION", u"TIPO"] # descriptores para los campos en el archivo txt de salida

        idproy.idproy(rutaCl, capaCl, capa_salida, camposCons, dAlter)

            
        capas =  [u"Zona arenosa"]
        rutas = [rutaCl]
        ncampo = [camposCons[3]]                          # campo para el rótulo
        tit = capa_salida                           # título del mapa en el layout

            # near 
        rutaorigen = rutaCl + u"/"                   # Ruta del archivo a analizar
        capa = capas[0]                             # Capa a analizar
        distancia = 1000                            # Distancia a realizar el análisis en km (incluye cualquier elemento que esté a esa distancia)
        campo = u"NEAR_DIST"                         # campo donde se guarda la distancia al sistema
        valor = -1                                  # valor a eliminar del campo 'campo'
        n=0
        camporef = ncampo[n]                        # campo de referencia (para agregar a la descripción del archivo)
        archivo = capa + u" near"                    # nombre del archivo de texto a generar para proceso 'near'
        cantidad = 20                               # cantidad de registros más cercanos
        nearexp.nearproceso(rutaorigen, capa, distancia, campo, valor, camporef, archivo, cantidad)

            # mapa
        tipo = u"nacional"                           # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 0
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal) 

        tipo = u"estatal"                            # código para el nivel de representación
        nummapa = arcpy.env.nummapa                 # consecutivo para el número de mapa en el nombre del archivo
        ordinal = 5
        cliptema.clipt(rutas, capas, tipo, ncampo, nummapa, tit, ordinal)
        

    except Exception as e:
        log.log(repet,u"\n\n>> ERROR, no se pudo ejecutar 'zonaarenosa'")
        log.log(repet,str(e) + u"\n\n\n\n")
        borrainn.borrainn()

    tiempo_mapa_fin = datetime.datetime.now().strftime(u"%Y-%m-%d %H:%M:%S")
    log.log(repet,u"tiempo total de mapa '{}': {}".format(tit,tiempo.tiempo([tiempo_mapa_ini,tiempo_mapa_fin])))
    
    log.log(repet,u"Proceso 'Zona arenosa' finalizado! \n\n")

    arcpy.env.repet = arcpy.env.repet - 1

