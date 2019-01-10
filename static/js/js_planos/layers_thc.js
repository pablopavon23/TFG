// AÑADIMOS BLOQUE PARA REPRESENTAR LOS LAYERS DE TEMPERATURA, C02 Y HUMEDAD
/* generamos los layers de medidas */
var tmp_aire = L.layerGroup();
var co2 = L.layerGroup();
var humedad = L.layerGroup();

/* agrupamos las layers de medidas en un mismo grupo */
var overlays = {
    "Temperatura": tmp_aire,
    "CO2": co2,
    "Humedad": humedad
};

L.control.layers(overlays).addTo(map);
