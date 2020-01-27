// Data generated from http://www.bikeforums.net/professional-cycling-fans/1113087-2017-tour-de-france-gpx-tcx-files.html
var elevationData =[];
// var mota = {{ entry.id_mota }}
var medida_visualiz = ''
{% for entry in Medidas %}
  var mota = {{ entry.id_mota }}
  {% if esTMP %}  // Si es temperatura accedo al campo temperatura
    var valor = '{value} ºC'
    var header_c = 'Temperatura: {point.y} ºC<br>'
    var medida_visualiz = 'Temperatura (ºC)'
    {% if entry.TMPaire %}  // Sólo si hay campo lo introduzco sino nada
      elevationData.push([{{ entry.hora|date:'h:i:sa' }},{{ entry.TMPaire }}]
    {% endif %}
  {% endif %}
  {% if esHUM %}  // Si es humedad accedo al campo humedad
    var valor = '{value} %'
    var header_c = 'Humedad: {point.y} %<br>'
    var medida_visualiz = 'Humedad (%)'
    {% if entry.HUMEDAD %}  // Sólo si hay campo lo introduzco sino nada
      elevationData.push([{{ entry.hora|date:'h:i:sa' }},{{ entry.HUMEDAD }}])
    {% endif %}
  {% endif %}
  {% if esCO %}  // Si es co2 accedo al campo co2
    var valor = '{value} ppp'
    var header_c = 'CO2: {point.y} ppp<br>'
    var medida_visualiz = 'CO2 (ppm)'
    {% if entry.CO2 %}  // Sólo si hay campo lo introduzco sino nada
      elevationData.push([{{ entry.hora|date:'h:i:sa' }},{{ entry.CO2 }}])
    {% endif %}
  {% endif %}
{% endfor %}

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
        text: 'Tablas de medidas en el edificio {{Edificio}}'
    },

    subtitle: {
        text: 'Está viendo la mota '+mota+' , medida '+medida_visualiz+'<br>'
    },

    xAxis: {
        labels: {
            format: '{value} h'
        },
        // minRange: 1,
        title: {
            text: 'Hora'
        }
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
        pointFormat: 'Hora: {point.x} h',
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
