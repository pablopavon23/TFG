// Data generated from http://www.bikeforums.net/professional-cycling-fans/1113087-2017-tour-de-france-gpx-tcx-files.html
var elevationData =[];
{% for entry in Medidas %}
  {% if entry.TMPaire %}  // Sólo si hay campo lo introduzco sino nada
  elevationData.push([{{ entry.horajs }},{{ entry.TMPaire }}])
  {% endif %}
{% endfor %}

console.log(elevationData)

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
        text: 'Elige otro edificio o mota si lo deseas'
    },

    xAxis: {
        labels: {
            format: '{value} h'
        },
        minRange: 1,
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
            format: '{value} ºC'
        }
    },

    tooltip: {
        headerFormat: 'Temperatura: {point.y} ºC<br>',
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
