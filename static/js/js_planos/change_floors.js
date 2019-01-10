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
