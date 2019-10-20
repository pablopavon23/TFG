from datetime import datetime, date, time, timedelta
import calendar
# Importamos el módulo predefinido para creacón de ficheros JSON:
import json
import os
# Importamos los modelos:
from .models import *

# Para el caso del EDIFICIO70 del Ciemat y de la PSA(Plataforma Solar de Almeria) nos inventamos las medidas
def get_medidas(edificio):
    # medidas = [1,1,2,3] # Simple total
    medidas = []    # Inicializo sino: UnboundLocalError: local variable 'medidas' referenced before assignment

    medidas_ED_70 = [
      {
        "CO2": 553.628,
        "TMPaire": 23.8965,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.7287271, 40.45471573],
        "mota": 1,
        "hora": time(10,30,0),  # Asigna 10h 30m 0s
        "horajs": 10.30
      },
      {
        "CO2": 575.542,
        "TMPaire": 27.7478,
        "HUMEDAD": 42.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72868991, 40.45471573],
        "mota": 3,
        "hora": time(11,30,0),
        "horajs": 11.30
      },
      {
        "CO2": 776.035,
        "TMPaire": 23.3646,
        "HUMEDAD": 35.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.728652, 40.45471954],
        "mota": 2,
        "hora": time(12,15,0),
        "horajs": 12.15
      },
      {
        "CO2": 462.749,
        "TMPaire": 24.5945,
        "HUMEDAD": 22.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.7286551, 40.45475006],
        "mota": 1,
        "hora": time(12,30,0),
        "horajs": 12.30
      },
      {
        "TMPsuperficie": 22.9343,
        "HUMEDAD": 50.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72866201, 40.45479965],
        "mota": 2,
        "hora": time(13,00,0),
        "horajs": 13.00
      },
      {
        "CO2": 301.749,
        "TMPaire": 20.5945,
        "HUMEDAD": 65.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72861505, 40.45477676],
        "mota": 1,
        "hora": time(13,30,0),
        "horajs": 13.30
      },
      {
        "CO2": 462.749,
        "TMPaire": 24.5945,
        "HUMEDAD": 22.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72861695, 40.45475388],
        "mota": 3,
        "hora": time(15,00,0),
        "horajs": 15.00
      },
      {
        "CO2": 162.749,
        "TMPaire": 35.5945,
        "HUMEDAD": 75.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72861409, 40.45472336],
        "mota": 2,
        "hora": time(16,30,0),
        "horajs": 16.30
      },
      {
        "CO2": 575.542,
        "TMPaire": 27.7478,
        "HUMEDAD": 60.5998,
        "ABIERTOCERRADO": 0,
        'planta': 1,
        "gps": [-3.72868991, 40.45471573],
        "mota": 4,
        "hora": time(18,00,0),
        "horajs": 18.00
      }
    ]
    medidas_Clinica_Fuenlabrada = 2
    medidas_LECE = 3

    if (edificio == "tables_ED_70") or (edificio == "slices_ED_70"):
        medidas = medidas_ED_70
    elif (edificio == "tables_Clinica_Fuenlabrada") or (edificio == "slices_Clinica_Fuenlabrada"):
        medidas = medidas_Clinica_Fuenlabrada
    elif (edificio == "tables_Lece") or (edificio == "slices_Lece"):
        medidas = medidas_LECE

    return medidas

# ---------------------------------------------------------------------------------------------------------

def get_CF_info():
    # A modo de prueba saco la información
    todas_motas = ClinicaFuenlabrada1Motas.objects.all()

    i = 0
    dicts = []
    while i < len(todas_motas):
        dict = {}
        dict['id'] = todas_motas[i].id_mota
        dict['planta'] = planta_mota(todas_motas[i].id_mota)
        dict['sensores'] = todas_motas[i].num_sensores
        lista_sensores = ClinicaFuenlabrada1Sensores.objects.filter(id_mota=todas_motas[i].id_mota) # Busco los sensores asociados a esa mota
        dict['tipsen'] = list(lista_sensores)
        dicts.append(dict)
        i += 1

    return dicts

# ---------------------------------------------------------------------------------------------------------

# Funcion que me ayuda a poder meter un datetime en un JSON:
def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

# ---------------------------------------------------------------------------------------------------------

def get_medidas_true():
    # Hago una query a la tabla de mi base de datos donde estan las medidas:
    # todas_medidas = ClinicaFuenlabrada1Medidas.objects.all() -- Cuidado porque esto podría estar ejecutandose la vida
    ultimas_medidas = ClinicaFuenlabrada1Medidas.objects.all()[:10]

    # Llamo a la funcion que me carga la relacion de motas para saber que tipos de sensor tiene cada mota:
    motas_rel = get_CF_info()

    """
    Ahora tengo que hacer un procedimiento que:
    1. Busque en ClinicaFuenlabrada1Medidas.objects.filter(id_mota=X).filter(tipo_medida=XXX).order_by('hora')[:10]
    2. Luego necesito:
        - id_mota, que la iré cogiendo de motas_rel con un bucle
        - tipo_medida, que tendré que conseguir buscando para una id_mota en motas_rel los tipos de medidas que tiene
    """
    medidas_definitivas = []
    for dicts in motas_rel:
        idm = dicts['id']
        current_dic = {} # aqui guardo el diccionario acutal que luego inserto en la lista
        current_dic['id_mota'] = idm    # tambien me valdria dicts['id']
        current_dic['planta'] = dicts['planta']
        current_dic['sensores'] = dicts['sensores']
        current_dic['gps'] = gps_mota(idm)
        # print("Los diccionarios son: "+str(dicts))
        med_types = []
        for tipo in dicts['tipsen']:
            if not tipo.tipo_medida in med_types:
                current_med = []    # me sirve para luego meter cada medida
                tip_actual = tipo.tipo_medida
                # print("El tipo ahora es: "+str(tip_actual))
                med_types.append(tip_actual)
                # Ahora ya obtengo para esa mota sus diferentes tipos de medidas
                med_actual = ClinicaFuenlabrada1Medidas.objects.filter(id_mota=idm).filter(tipo_medida=tip_actual).order_by('hora')[:2]
                # print("La medida actual es: "+str(med_actual))
                """
                Voy a hacer aqui la prueba de meterlo en el JSON:
                Meto algo del estilo:
                [
                {'id_mota':1,'planta':3,'sensores':2,'gps':[-3.78...,40.78...],'HUMEDAD (%)':[15 objects],'TMP-aire (c)': [15 objects]},
                otro diccionario,
                otro,
                ...
                Lo primero ya lo tengo arriba solo me queda 'HUMEDAD (%)':[15 objects],'TMP-aire (c)': [15 objects] o lo que sea
                El object ese de lo unico que quiero de ahi es medida y hora.
                ]
                """
                # med_actual es una serie de QuerySet, debo acceder al campo medida de cada uno.
                for medidas in med_actual:
                    current_med.append(medidas.medida)

                current_dic[tip_actual] = current_med    # Esto añade: 'HUMEDAD (%)':[15 objects])

        print("LA MOTA "+str(idm)+" :TIENES: "+str(med_types))
        # Añado ese diccionario a la lista
        medidas_definitivas.append(current_dic)

    # Hago el JSON que contiene los datos de medidas.
    generate_json("medidas.json",medidas_definitivas)


    test = 1
    # Ahora vamos a parsear la QuerySet e introducir la info en el JSON:
    meds = []
    for medida in ultimas_medidas:
        med = {}
        # print("Ahi va el idesensor: "+str(medida.id_sensor))
        med['idsen'] = medida.id_sensor
        # print("Ahí va la tipo de medida: "+str(medida.tipo_medida))
        med['tipmed'] = medida.tipo_medida
        med['idmota'] = medida.id_mota
        med['med'] = medida.medida
        # print("Ahi va la hora: "+str(medida.hora))  # Esto me imprime: 2018-05-08 15:18:00+00:00
        # print("La hora de medida es: "+str(hora_medida))
        med['hora'] = medida.hora
        meds.append(med)

    # Generamos el archivo JSON que contiene la información de la relacion de motas:
    # generate_json("relacion.json",meds)

    return test

# ---------------------------------------------------------------------------------------------------------

def generate_json(file_name,info_dicts):
    # dir = 'C:/Pruebas'  # También es válido 'C:\\Pruebas' o r'C:\Pruebas' -- Esto por si quiero meterlo en un directorio distinto al que me encuentro
    dir = '/home/ppp23/Escritorio/TFG/data'
    # file_name = "data.json"

    # with open(file_name, 'w') as file:
    with open(os.path.join(dir, file_name), 'w') as file: #-- Esto por si quiero meterlo en un directorio distinto al que me encuentro
        json.dump(info_dicts, file, default=myconverter)

# ---------------------------------------------------------------------------------------------------------

# Recibe como argumento el id_mota y según este podemos decir en qué planta está:
def planta_mota(mota):

    if mota in [13,18]:
        planta = 1
    elif mota in [12,14]:
        planta = 2
    elif mota in [1,2,3,5,6,7,15]:
        planta = 3
    elif mota in [8,9,10,11,16,17]:
        planta = 4
    else:
        planta = "no data"

    return planta

# ---------------------------------------------------------------------------------------------------------

# Recibe como argumento el id_mota y según este podemos decir en qué coordenadas tiene:
# Se podria sustituir por un diccionario creo, al igual que el de la planta.
def gps_mota(mota):

    if mota == 1:
        gps = [-3.7973980744918094,40.277264074863325]
    elif mota == 2:
        gps = [-3.796926005621316,40.277124106016885]
    elif mota == 3:
        gps = [-3.7973263254056633,40.277321167285066]
    elif mota == 5:
        gps = [-3.796928017273842,40.277049210358825]
    elif mota == 6:
        gps = [-3.797550960372604,40.27708277013147]
    elif mota == 7:
        gps = [-3.796976967647737,40.277301522572856]
    elif mota == 8:
        gps = [-3.797379969547677,40.277267348802354]
    elif mota == 9:
        gps = [-3.7969575215968234,40.27713249590113]
    elif mota == 10:
        gps = [-3.7975536425734617,40.277079496013215]
    elif mota == 11:
        gps = [-3.7968971718938747,40.27729681586601]
    elif mota == 12:
        gps = [-3.79707486829426,40.27713965824617]
    elif mota == 13:
        gps = [-3.7973776226223492,40.27726356322137]
    elif mota == 14:
        gps = [-3.797374605270221,40.27725445708464]
    elif mota == 15:
        gps = [-3.797331689784727,40.277073561654646]
    elif mota == 16:
        gps = [-3.7969903786510883,40.277270418288424]
    elif mota == 17:
        gps = [-3.797427578755986,40.277092183247134]
    elif mota == 18:
        gps = [-3.796971603319321,40.2771160230848]
    else:
        gps = []

    return gps
