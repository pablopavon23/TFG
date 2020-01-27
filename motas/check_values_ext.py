# Para trabajar con JSON:
import json
import os
# Importamos el método del views que procesa el JSON:
from .views import get_data,insert_idMota

# ------------------------------------------------------------------------------
# Funcion que recibe como argumento el tipo de medida y los datos y devuelve una lista
# indicando las motas con valor anómalo.
def check_values_ext():
    # Extraigo los datos
    medidas = get_data()
    # Extraigo la cantidad de motas que tenemos
    cant_motas = insert_idMota(medidas)

    # Comprobamos cada medida:
    muestras = []
    current = []
    for med in medidas:    # med es cada uno de los diccionarios
        # current = med.get(check_tipo)
        current_mota = med.get()
        if (current != None):   # Si no tenemos medida no se añade
            muestras.append(current)

    # Ordeno las muestras para que queden de min. valor a max. valor
    muestras = sorted(muestras)
    # Compruebo si hay (o no) alerta
    if (muestras[0] < 0.0) or (muestras[len(muestras)-1] > 50.0):
        alertar = True
    else:
        alertar = False

    return alertar
