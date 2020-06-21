// Data generated from http://www.bikeforums.net/professional-cycling-fans/1113087-2017-tour-de-france-gpx-tcx-files.html
var elevationData =[];
for (entry in Medidas){
  var mota = entry.id_mota;
  if (esTMP){
     var valor = '{value} ºC';
     var header_c = 'Temperatura: {point.y} ºC<br>';
     var medida_visualiz = 'Temperatura (ºC)';
      if (entry.TMPaire){
        console.log('La fecha es:  '+entry.hora);
        var msec = Date.parse(entry.hora);
        var d = new Date(msec);
        var valid_date = Date.UTC(d.getFullYear(),d.getMonth(),d.getDate(),d.getHours(),d.getMinutes(),d.getSeconds());
        // Tengo que poner el +1 porque me coge mal el mes.
        var footer_c = 'Fecha: '+d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
        console.log('La fecha despues es: '+d);
        elevationData.push([valid_date, entry.TMPaire]);
      }   // Sólo si hay campo lo introduzco sino nada
  }   // Si es temperatura accedo al campo temperatura
  if (esHUM){
     var valor = '{value} %';
     var header_c = 'Humedad: {point.y} %<br>';
     var medida_visualiz = 'Humedad (%)';
      if (entry.HUMEDAD){
        console.log('La fecha es:  '+entry.hora);
        var msec = Date.parse(entry.hora);
        var d = new Date(msec);
        var valid_date = Date.UTC(d.getFullYear(),d.getMonth(),d.getDate(),d.getHours(),d.getMinutes(),d.getSeconds());
        // Tengo que poner el +1 porque me coge mal el mes.
        var footer_c = 'Fecha: '+d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
        console.log('La fecha despues es: '+d);
        elevationData.push([valid_date, entry.HUMEDAD]);
      }   // Sólo si hay campo lo introduzco sino nada
  }   // Si es humedad accedo al campo humedad
  if (esCO){
     var valor = '{value} ppp';
     var header_c = 'CO2: {point.y} ppp<br>';
     var medida_visualiz = 'CO2 (ppm)';
      if (entry.CO2){
        console.log('La fecha es:  '+entry.hora);
        var msec = Date.parse(entry.hora);
        var d = new Date(msec);
        var valid_date = Date.UTC(d.getFullYear(),d.getMonth(),d.getDate(),d.getHours(),d.getMinutes(),d.getSeconds());
        // Tengo que poner el +1 porque me coge mal el mes.
        var footer_c = 'Fecha: '+d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
        console.log('La fecha despues es: '+d);
        elevationData.push([valid_date, entry.CO2]);
      }   // Sólo si hay campo lo introduzco sino nada
  }   // Si es co2 accedo al campo co2
}

// Now create the chart
Highcharts.chart('container', {

chart: {
  type: 'area',
    zoomType: 'x',
    panning: true,
    panKey: 'shift',
    scrollablePlotArea: {
    minWidth: 600
  }
},

title: {
  text: 'Tablas de medidas en el edificio '+Edificio
},

subtitle: {
  text: 'Está viendo la mota '+mota+' , medida '+medida_visualiz+'<br>'
},

xAxis: {
  type: 'datetime',
  // labels: {
  // 	format: '{value} h'
  // },
  // minRange: 24,
  title: {
    text: 'Hora'
  },
},

yAxis: {
  startOnTick: true,
    endOnTick: false,
    maxPadding: 0.35,
    title: {
    text: null
  },
    labels: {
    format: valor
  }
},

tooltip: {
  headerFormat: header_c,
  pointFormat: footer_c,
    shared: true
},

legend: {
  enabled: false
},

series: [{
  data: elevationData,
    lineColor: Highcharts.getOptions().colors[1],
    color: Highcharts.getOptions().colors[2],
    fillOpacity: 0.5,
    name: 'Elevation',
    marker: {
    enabled: false
  },
    threshold: null
}]

});
