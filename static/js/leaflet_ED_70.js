/* Obtenemos las claves de nuestro objeto con Object.keys para sacar el nombre de ED_70*/
buildingName = Object.keys(planos)[0];
var building = planos[buildingName];
/* Declaramos el punto con las coordenadas */
var coords = L.latLng(building["coordenadas"][0],  building["coordenadas"][1]);

/* -------------------------------------------------------------------------- */

// AÑADIMOS BLOQUE PARA REPRESENTAR EL PUNTO DENTRO DEL MAPA
var map = new L.Map('map', {
        center: coords,
        zoom: 10
});
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',maxZoom: 20}).addTo(map);
L.control.scale().addTo(map);

/* -------------------------------------------------------------------------- */

// AÑADIMOS EL MARKER
var marker = L.marker(coords,{draggable: true}).addTo(map).bindPopup(buildingName + '<br> Plantas: ' + building['plantas'] + '<br>Más info: <a href="http://www.ciemat.es/">CIEMAT</a>');

/* -------------------------------------------------------------------------- */

// AÑADIMOS LA POSIBILIDAD DE HACER ZOOM HACIENDO CLICK EN EL MARKER
/* Hace zoom en el edifio al seleccionar su marker */
function onClick(e) {
    map.setView(e.latlng, 19);
};
marker.on('click', onClick);

/* -------------------------------------------------------------------------- */

// AÑADIMOS EL ÚNICO PLANO QUE TENEMOS PARA EL EDIFICIO 70:
/* cargamos la localización de esquina izquierda, derecha y parte inferior de cada edificio */
var point1 = L.latLng(building["p1"][0],  building["p1"][1]);
var point2 = L.latLng(building["p2"][0],  building["p2"][1]);
var point3 = L.latLng(building["p3"][0],  building["p3"][1]);

var overlay = L.imageOverlay.rotated('http://www.lib.utexas.edu/maps/historical/newark_nj_1922.jpg', point1,point2,point3, {
  opacity: 0.9,
  interactive: false
}).addTo(map);
