var map = L.map('map').setView([37.0915,-2.3562],15);
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',maxZoom: 18}).addTo(map);
L.control.scale().addTo(map);
L.marker([37.0915,-2.3562],{draggable: true}).addTo(map)
