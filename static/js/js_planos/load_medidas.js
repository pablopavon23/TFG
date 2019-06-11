// AÑADIMOS BLOQUE PARA VISUALIZAR ARRAY DE LAYERS DE MEDIDAS
var gradiente = {
  0.0:    '#0000FF',
  0.125:  '#007FFF',
  0.25:   '#00FFFF',
  0.375:  '#00FF7F',
  0.5:    '#00FF00',
  0.625:  '#3B7317',
  0.75:   '#FFFF00',
  0.875:  '#FF7F00',
  1.0:    '#FF0000'
};

// para alojar las medidas de cada variable tomadas y buscar valors anomalos
var temperaturas = [];
var humedades = [];
var dioxis = [];

/* diccionario con el conjunto de medidas */
var medidasLayers = {}

/* genera un diccionario con array de medida vacias */
function generateMeasuresLayer (floor) {
  var tmppoints = []
  var co2points = []
  var humedadpoints = []

  var floorLayer = {}
  floorLayer['tmp'] = tmppoints;
  floorLayer['co2'] = co2points;
  floorLayer['humedad'] = humedadpoints

  return floorLayer
};

/* añadimos a los heatmaps las medidas correspondientes a la planta */
function addMeasuresLayer (floor) {
  var heat = L.heatLayer(medidasLayers[floor]['tmp'], {maxZoom: 20, max: 40, radius: 25, blur: 15, minOpacity: 0.2, gradient: gradiente}).addTo(tmp_aire);
  heat = L.heatLayer(medidasLayers[floor]['co2'], {maxZoom: 20, max: 800, radius: 25, blur: 15, minOpacity: 0.2, gradient: gradiente}).addTo(co2);
  heat = L.heatLayer(medidasLayers[floor]['humedad'], {maxZoom: 20, max: 100, radius: 25, blur: 15, minOpacity: 0.2, gradient: gradiente}).addTo(humedad);
}

/* borramos todas las medidas de los heatmaps */
function removeMeasuresLayer (floor) {
  tmp_aire.clearLayers()
  co2.clearLayers()
  humedad.clearLayers()
}

/* carga las medidas y las aloja en el diccionario medidasLayers */
 for (var dbIndex in medidas) {
   var db = medidas[dbIndex];
   for (var motaId in db) {
     mota = db[motaId];
     if (!medidasLayers[mota['planta']]) {
       medidasLayers[mota['planta']] = generateMeasuresLayer(mota['planta']);
     };

     if (mota["TMP-aire (c)"]) {
       temperaturas.push(mota["TMP-aire (c)"])
       var arr1 = [mota["gps"][1], mota["gps"][0], mota["TMP-aire (c)"]]
       medidasLayers[mota['planta']]['tmp'].push(arr1)
     }
     if (mota["CO2 (ppp)"]) {
       dioxis.push(mota["CO2 (ppp)"])
       var arr2 = [mota["gps"][1], mota["gps"][0], mota["CO2 (ppp)"]]
       medidasLayers[mota['planta']]['co2'].push(arr2)
     }
     if (mota["HUMEDAD (%)"]) {
       humedades.push(mota["HUMEDAD (%)"])
       var arr3 = [mota["gps"][1], mota["gps"][0], mota["HUMEDAD (%)"]]
       medidasLayers[mota['planta']]['humedad'].push(arr3)
     }

     console.log("TEMperatura: "+temperaturas)

   };
};

/* cargamos por defecto las medidas de la primera planta */
addMeasuresLayer(1);
