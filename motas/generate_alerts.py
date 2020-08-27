# Importamos los modelos:
from .models import *
# Importamos las características:
from django.conf import settings

# ------------------------------------------------------------------------------
# Funcion que recibe como argumento el tipo de medida y los datos y devuelve un boolean indicando si
# hay valores anómalos o no.
def check_medida(tipo,medidas_test):

    if tipo == 'temperatura':
        check_tipo = "TMPaire"
    elif tipo == 'dioxido':
        check_tipo = "CO2"
    elif tipo == 'humedad':
        check_tipo = "HUMEDAD"

    # Comprobamos cada medida:
    motas_alerta = []
    planta_alerta = []
    hora_alerta = []
    tipo_alerta = []

    for medidas in medidas_test:    # medidas es cada uno de los diccionarios
        current = medidas.get(check_tipo)
        if (current != None):   # Si no tenemos medida no se añade
            alert = alert_type(check_tipo,current)
            if alert:   # si hay alerta es que hay valor anomalo
                alertar = True
                mota = medidas.get('id_mota')  # cojo la mota (para enviar el correo)
                if not str(mota) in motas_alerta:  # asi me aseguro no guardar dos veces la misma mota.
                    motas_alerta.append(str(mota))   # añado la mota a la lista que enviar al correo
                    planta_alerta.append(medidas.get('planta'))
                    hora_alerta.append(medidas.get('hora'))
                    tipo_alerta.append(check_tipo)

    return alertar, motas_alerta, planta_alerta, tipo_alerta, hora_alerta

# ------------------------------------------------------------------------------
# Funcion que recibe una medida y según el tipo que sea alerta si hay valor anomalo o no.
# Los valores límite los saco de la memoria (sección 5.6)
def alert_type(type,medida):
    if type == 'TMPaire':
        if (medida < 0.0) or (medida > 70.0):
            alert_or_not = True
        else:
            alert_or_not = False
    elif type == 'CO2':
        if (medida < 100.0) or (medida > 800.0):
            alert_or_not = True
        else:
            alert_or_not = False
    elif type == 'HUMEDAD':
        if (medida < 0.0) or (medida > 100.0):
            alert_or_not = True
        else:
            alert_or_not = False

    return alert_or_not
# ------------------------------------------------------------------------------
#     """ La función aqui es devolver si hay que alertar o no"""
def check_values(medidas_test):
    # Invoco a la funcion que me indica si una medida cualquiera contiene valor anomalo o no
    alertar_TMP,motas_alerta_t,planta_alerta_t,tipo_alerta_t,hora_alerta_t = check_medida('temperatura',medidas_test)
    alertar_CO,motas_alerta_d,planta_alerta_d,tipo_alerta_d,hora_alerta_d = check_medida('dioxido',medidas_test)
    alertar_HU,motas_alerta_h,planta_alerta_h,tipo_alerta_h,hora_alerta_h = check_medida('humedad',medidas_test)

    motas_alerta = motas_alerta_t+motas_alerta_d+motas_alerta_h
    planta_alerta = planta_alerta_t+planta_alerta_d+planta_alerta_h
    tipo_alerta = tipo_alerta_t+tipo_alerta_d+tipo_alerta_h
    hora_alerta = hora_alerta_t+hora_alerta_d+hora_alerta_h

    cuerpo_mail = ''
    for x in range(0,len(motas_alerta)):
        cuerpo_mail += "Valor anómalo recogido para mota "+str(motas_alerta[x])+", ubicada en la planta: "+str(planta_alerta[x])+", sensor que mide: "+tipo_alerta[x]+". Medida tomada a las: "+str(hora_alerta[x])+"\n"

    if (not alertar_TMP) and (not alertar_CO) and (not alertar_HU):
        alertar = False
    else:
        alertar = True

    return alertar,motas_alerta,cuerpo_mail

# ------------------------------------------------------------------------------
