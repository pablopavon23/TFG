/* Obtenemos las claves de nuestro objeto con Object.keys para sacar el nombre de Clinica_Fuenlabrada*/
buildingName = Object.keys(planos)[2];
var building = planos[buildingName];
/* Declaramos el punto con las coordenadas */
var coords = L.latLng(building["coordenadas"][0],  building["coordenadas"][1]);


// AÑADIMOS BLOQUE PARA REPRESENTAR EL PUNTO DENTRO DEL MAPA
var map = new L.Map('map', {
        center: coords,
        zoom: 10
});
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',maxZoom: 20}).addTo(map);
L.control.scale().addTo(map);


// AÑADIMOS EL MARKER
var marker = L.marker(coords,{draggable: true}).addTo(map).bindPopup(buildingName + '<br> Plantas: ' + building['plantas']);


// AÑADIMOS LA POSIBILIDAD DE HACER ZOOM HACIENDO CLICK EN EL MARKER
/* Hace zoom en el edifio al seleccionar su marker */
function onClick(e) {
    map.setView(e.latlng, 19);
};
marker.on('click', onClick);
