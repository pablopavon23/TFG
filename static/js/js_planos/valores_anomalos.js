/* Este script nos ayuda a identificar valores anomalos y saltar la ventana de alerta */
temperaturas.sort(function(a, b){return a - b});

var min_temp = temperaturas[0];
var max_temp = temperaturas[temperaturas.length - 1];

if (min_temp < 0.0) {
  alert("La temperatura del edificio LECE es demasiado baja")
} else if (max_temp > 50.0) {
  alert("La temperatura del edificio LECE es demasiado alta")
}
