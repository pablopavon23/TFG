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

    get_medidas_true()

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

    # Ahora vamos a parsear la QuerySet e introducir la info en el JSON:
    meds = []
    for medida in ultimas_medidas:
        med = {}
        print("Ahi va el idesensor: "+str(medida.id_sensor))
        med['idsen'] = medida.id_sensor
        print("Ahí va la tipo de medida: "+str(medida.tipo_medida))
        med['tipmed'] = medida.tipo_medida
        med['idmota'] = medida.id_mota
        med['med'] = medida.medida
        print("Ahi va la hora: "+str(medida.hora))  # Esto me imprime: 2018-05-08 15:18:00+00:00
        # print("La hora de medida es: "+str(hora_medida))
        med['hora'] = medida.hora
        meds.append(med)

    # Generamos el archivo JSON que contiene la información requerida:
    generate_json(meds)

# ---------------------------------------------------------------------------------------------------------

def generate_json(info_dicts):
    # dir = 'C:/Pruebas'  # También es válido 'C:\\Pruebas' o r'C:\Pruebas' -- Esto por si quiero meterlo en un directorio distinto al que me encuentro
    dir = '/home/ppp23/Escritorio/TFG/data'
    file_name = "data1.json"

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
