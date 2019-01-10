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
