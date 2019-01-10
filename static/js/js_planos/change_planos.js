// AÑADIMOS BLOQUE PARA VISUALIZAR ARRAY DE PLANOS
/* diccionario que aloja los planos definidos por planta */
// console.log(buildingName) --> esto me imprime Clinica_Fuenlabrada
// console.log(building)  --> esto me imprime Object { plantas: 4, coordenadas: (2) […], p1: (2) […], p2: (2) […], p3: (2) […], databases: [] }
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

/* cargamos los marcadores y planos de cada edificio */
for (build in planos) {
  /* cargamos la localización de esquina izquierda, derecha y parte inferior de cada edificio */
  var point1 = L.latLng(building["p1"][0],  building["p1"][1]);
  var point2 = L.latLng(building["p2"][0],  building["p2"][1]);
  var point3 = L.latLng(building["p3"][0],  building["p3"][1]);

  /* cargamos los planos de edifiocios en el array */
  for (var i = 1; i<= building['plantas']; i++) {
    if (!buildingPlans[i]) {
      buildingPlans[i] = {}
    }
    var overlay = L.imageOverlay.rotated('http://www.lib.utexas.edu/maps/historical/newark_nj_1922.jpg', point1,point2,point3, {
      opacity: 0.9,
      interactive: false
    });
    buildingPlans[i][build] = overlay;
  };
};

/* dibujamos por defecto las primeras plantas en el mapa */
addFloors(1);
