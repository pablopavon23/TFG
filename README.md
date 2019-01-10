# TFG
***
#### Versión1 - V.05/12/2018:
* Aplicación inicial con las plantillas cargadas
***
#### Versión2 - V.17/12/2018:
* Aplicación en la que ya se puede loguear a los usuarios predefinidos y cargar para cada uno de ellos la pagina principal correspondiente según qué permisos tengan.
***
#### Versión3 - V.18/12/2018:
* Re ordenación de las plantillas para mostrarlas de un modo más eficaz.
* Hacer las plantillas leaflet como extensiones de otras plantillas.
* Los items de los menus de slices,tables y slices hechos dinámicos.
* Ajuste parcial del iframe para importar las slices.
***
#### Versión4 - V.19/12/2018:
* Externalización de los leaflets fuera de las plantillas en JavaScript separados. Se añaden en /satic/js.
* Simplificación de las plantillas respectivas de slices, tables y maps para que sean sólo extensiones de index.html y modificar bloques sólo.
* Descubrimiento de request.user que me devuelve un objeto para saber que usuario ha realizado qué petición.  
* Los items de los menus de slices,tables y slices hechos dinámicos de un modo más eficaz, mediante el uso de loop for en html.
***
#### Versión - V.10/01/2019:
* Se consigue representar la leyenda de las medidas a representar en los mapas.
* Implantación de planos de prueba superpuestos sobre las localizaciones que se desean. Necesario comprobar como cargar los planos que se tienen en la unidad local dentro de /static/img/planos/...
* Al hacer click sobre un marker se consigue hacer zoom y visualizar los planos de los edificios.
