var map = L.map('map').setView([37.0915,-2.3562],15);
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',maxZoom: 18}).addTo(map);
L.control.scale().addTo(map);
L.marker([37.0915,-2.3562],{draggable: true}).addTo(map)


// -----------------------------------------------------------------------------
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

// -----------------------------------------------------------------------------
// AÑADIMOS BLOQUE PARA CAMBIAR PLANTAS
var floors = L.control({position: 'bottomleft'});
var pisoActual = 1;
var pisoMin = 1;
var pisoMax = 4;

/* cambia los planos y medidas al aumentar la planta de visualizacion */
function subirPlanta() {
  if (pisoActual < pisoMax) {
    removeFloors(pisoActual);
    removeMeasuresLayer();
    pisoActual++;
    addMeasuresLayer(pisoActual)
    addFloors(pisoActual);
    floors.addTo(map);
  }
};

/* cambia los planos y medidas al disminuar la planta de visualizacio */
function bajarPlanta() {
  if (pisoActual > pisoMin) {
    removeFloors(pisoActual);
    removeMeasuresLayer();
    pisoActual--;
    addMeasuresLayer(pisoActual);
    addFloors(pisoActual);
    floors.addTo(map);
  }
};

/* genera el div para cambiar entre plantas */
floors.onAdd = function (map, medida) {
  var div = L.DomUtil.create('div', 'leaflet-control-zoom leaflet-bar leaflet-control'),
    labels = [];

  div.innerHTML =
  "<a class='leaflet-control-zoom-in' href='#' title='subir planta' onclick='subirPlanta();'>+</a>" +
  "<a class='leaflet-control-zoom-in'>" + pisoActual + '</a>' +
  "<a class='leaflet-control-zoom-out' href='#' title='bajar planta' onclick='bajarPlanta();'>-</a>";

  return div;
};
floors.addTo(map);

// -----------------------------------------------------------------------------
// AÑADIMOS BLOQUE PARA VISUALIZAR LEYENDA DE MEDIDAS
/* determina el color de la leyenda */
function getColor(d) {
  return d > 8 ? '#FF0000' :
         d > 7 ? '#FF7F00' :
         d > 6 ? '#FFFF00' :
         d > 5 ? '#3B7317' :
         d > 4 ? '#00FF00' :
         d > 3 ? '#00FF7F' :
         d > 2 ? '#00FFFF' :
         d > 1 ? '#007FFF' :
                 '#0000FF';
}

/* variable para la leyenda por defecto muestra temperatura */
var legend = L.control({position: 'bottomright', 'medida':'Temperatura'});

/* genera los indices de la leyenda */
legend.onAdd = function (map, medida) {
  indices = {
    'Temperatura': [0, 5, 10, 15, 20, 25, 30, 35, 40],
    'Humedad': [0, 10, 20, 30, 40, 50, 60, 70, 80],
    'CO2': [0, 100, 200, 300, 400, 500, 600, 700, 800]
  }
  tipos = {
    'Temperatura': 'Tmp (ºC)',
    'Humedad': 'Humedad (%)',
    'CO2': 'CO2 (ppm)'
  }

  /* carga los indices en funcion de la naturaleza de medida */
  var div = L.DomUtil.create('div', 'info legend'),
    grades = indices[legend.options['medida']],
    labels = [];

  /* añade los indices a la leyenda */
  div.innerHTML = '<h4>' + tipos[legend.options['medida']] + '<br></h4>';
  for (var i = 0; i < grades.length; i++) {
    div.innerHTML +=
      '<i style="background:' + getColor(i + 1) + '"></i> ' +
      grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
  }
  return div;
};

/* añade la leyenda por defectp */
legend.addTo(map);

/* cambia la leyenda en funcion del layer escogido */
map.on('baselayerchange', function(e) {
  legend.options['medida'] = e['name']
  legend.addTo(map);
});

// -----------------------------------------------------------------------------
// AÑADIMOS BLOQUE PARA VISUALIZAR ARRAY DE PLANOS
/* diccionario que aloja los planos definidos por planta */
var buildingPlans = {}

/* quita los planos de las plantas correspondiente */
function removeFloors (floor) {
  for (var plans in buildingPlans[floor]) {
    map.removeLayer(buildingPlans[floor][plans]);
  };
};

/* dibuja los planos de la planta correspondiente */
function addFloors (floor) {
  for (var plans in buildingPlans[floor]) {
    map.addLayer(buildingPlans[floor][plans]);
  };
};

/* hace zoom en el edifio al seleccionar su marker */
function onClick(e) {
    map.setView(e.latlng, 20);
};

/* cargamos los marcadores y planos de cada edificio */
for (buildingName in planos) {
  building = planos[buildingName]

  /* cargamos longitud & latitud de cada edificio */
  var point1 = L.latLng(building["p1"][0],  building["p1"][1]),
      point2 = L.latLng(building["p2"][0],  building["p2"][1]),
      point3 = L.latLng(building["p3"][0],  building["p3"][1]);

  /* colocamos un marcador para localizar los edificios */
  var marker1 = L.marker(point1, {draggable: false} ).addTo(map).bindPopup(buildingName + '<br> Plantas: ' + building['plantas']),
      marker2 = L.marker(point2, {draggable: false} ),//.addTo(map),
      marker3 = L.marker(point3, {draggable: false} );//.addTo(map);

  marker1.on('click', onClick);

  var	bounds = new L.LatLngBounds(point1, point2).extend(point3);

  /* cargamos los planos de edifiocios en el array */
  for (var i = 1; i<= building['plantas']; i++) {
    if (!buildingPlans[i]) {
      buildingPlans[i] = {}
    }
    var overlay = L.imageOverlay.rotated('img/planos/' + buildingName + '_p' + i + '.jpg', point1, point2, point3, {
      opacity: 0.9,
      interactive: false
    });
    buildingPlans[i][buildingName] = overlay;
  };
};

/* dibujamos por defecto las primeras plantas en el mapa */
addFloors(1);

// -----------------------------------------------------------------------------
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
      var arr1 = [mota["gps"][1], mota["gps"][0], mota["TMP-aire (c)"]]
      medidasLayers[mota['planta']]['tmp'].push(arr1)
    }
    if (mota["CO2 (ppp)"]) {
      var arr2 = [mota["gps"][1], mota["gps"][0], mota["CO2 (ppp)"]]
      medidasLayers[mota['planta']]['co2'].push(arr2)
    }
    if (mota["HUMEDAD (%)"]) {
      var arr3 = [mota["gps"][1], mota["gps"][0], mota["HUMEDAD (%)"]]
      medidasLayers[mota['planta']]['humedad'].push(arr3)
    }

  };
};

/* cargamos por defecto las medidas de la primera planta */
addMeasuresLayer(1);
