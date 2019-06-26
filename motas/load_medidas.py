from datetime import datetime, date, time, timedelta
import calendar

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

"""
var medidas =
{
  "ED70_1":
  {
    "1":
    {
      "CO2 (ppp)": 553.628,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.7287271, 40.45471573]
    },
    "2":
    {
      "CO2 (ppp)": 575.542,
      "TMP-aire (c)": 27.7478,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.72868991, 40.45471573]
    },
    "3":
    {
      "CO2 (ppp)": 776.035,
      "TMP-aire (c)": 23.3646,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.728652, 40.45471954]
    },
    "4":
    {
      "CO2 (ppp)": 462.749,
      "TMP-aire (c)": 24.5945,
      "HUMEDAD (%)": 22.5998,
      "ABIERTO/CERRADO": 0.0,
      'planta': 1,
      "gps": [-3.7286551, 40.45475006]
    },
    "5":
    {
      "ABIERTO/CERRADO": 0,
      "TMP-superficie (c)": 22.9343,
      'planta': 1,
      "gps": [-3.72866201, 40.45479965]
    },
    "6":
    {
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.72861505, 40.45477676]
    },
    "7":
    {
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.72861695, 40.45475388]
    },
    "8":
    {
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.72861409, 40.45472336]
    }
  },
  "FUENLABRADA":
  {
    "1":
    {
      "CO2 (ppp)": 553.628,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-3.796925, 40.277168]
    },
    "2":
    {
      "CO2 (ppp)": 575.542,
      "TMP-aire (c)": 27.7478,
      "ABIERTO/CERRADO": 0,
      'planta': 2,
      "gps": [-3.797086, 40.277256]
    },
    "3":
    {
      "CO2 (ppp)": 776.035,
      "TMP-aire (c)": 23.3646,
      "ABIERTO/CERRADO": 0,
      'planta': 3,
      "gps": [-3.797315, 40.277284]
    },
    "4":
    {
      "CO2 (ppp)": 462.749,
      "TMP-aire (c)": 24.5945,
      "HUMEDAD (%)": 22.5998,
      "ABIERTO/CERRADO": 0.0,
      'planta': 4,
      "gps": [-3.797542, 40.277281]
    }
  },
  "LECE":
  {
    "1":
    {
      "CO2 (ppp)": 553.628,
      "HUMEDAD (%)": 22.5998,
      "TMP-aire (c)": 27.7478,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-2.356121505675503, 37.09239468568795]
    },
    "2":
    {
      "CO2 (ppp)": 575.542,
      "TMP-aire (c)": 27.7478,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-2.3554321779695044, 37.092505083904555]
    },
    "3":
    {
      "CO2 (ppp)": 776.035,
      "TMP-aire (c)": 23.3646,
      "ABIERTO/CERRADO": 0,
      'planta': 1,
      "gps": [-2.3561483277703132, 37.09188805005742]
    },
    "4":
    {
      "CO2 (ppp)": 462.749,
      "TMP-aire (c)": 74.5945,
      "HUMEDAD (%)": 22.5998,
      "ABIERTO/CERRADO": 0.0,
      'planta': 1,
      "gps": [-2.3554134025056896, 37.09180931586367]
    }
  }
};
"""
