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
#### Versión5 - V.10/01/2019:
* Se consigue representar la leyenda de las medidas a representar en los mapas.
* Implantación de planos de prueba superpuestos sobre las localizaciones que se desean.
* Se cargan los planos que se tienen en la unidad local dentro de /static/img/planos/...
* Al hacer click sobre un marker se consigue hacer zoom y visualizar los planos de los edificios.
***
#### Versión6 - V.03/06/2019:
* Migración hacia Django 2.1.7 finalizada.
***
#### Versión7 - V.11/06/2019:
* Colocación de los planos correctos en edificio de Clinica_Fuenlabrada, así como ubicación correcta de las diferentes motas y sensores en el resto de edificios.
* Primeras pruebas de integración de la librería Highcharts de JavaScript para una futura representación de las medidas tomadas.
***
#### Versión8 - V.20/06/2019:
* Representación en tablas de los datos tomados aún sin conectar con la base de datos mySQL.
* Modificación de la plantilla tables.html así como de las vistas (views.py).
* Creación de un script en python que ayude a obtener las medidas de los distintos edificios.
***
#### Versión9 - V.26/06/2019:
* Representación de las gráficas con datos sobre cada mota y medida.
* Se añaden las opciones para elegir qué mota y/o medida queremos observar en las tablas y las gráficas.
* Adaptación del script creado para obtener las medidas de los edificios por existir errores al querer representar las mismas en Highcharts (JavaScript reconoce ":" de la hora como caracter reservado).
* Modificación de la apariencia de la vista de 'login'.
***
#### Versión10 - V.22/08/2019:
* Consecución del acceso a la base de datos en local que contiene las medidas tomadas en el edificio de la Clinica_Fuenlabrada.
* Se usarán dos bases de datos, una para el registro simple de usuarios y otra para conseguir los datos.
***
#### Versión11 - V.27/08/2019:
* Integración de los modelos de la base de datos de la Clinica_Fuenlabrada (tablas: clinica_fuenlabrada_1_motas, clinica_fuenlabrada_1_sensores y clinica_fuenlabrada_1_medidas).
* No son necesarias dos bases de datos, Django ofrece soporte para registro de usuarios sin necesidad de que sea SQLite la base de datos.
***
#### Versión12 - V.03/10/2019:
* Extracción de datos de la base 'Clinica_Fuenlabrada' importada desde el fichero .sql en local.
* Se comienzan a realizar las primeras pruebas extaryendo datos de la tabla 'clinica_fuenlabrada_1_motas', con el fin de estudiar la manera más eficiente de generar archivos JSON con esos datos.
***
#### Versión13 - V.07/10/2019:
* Realización de una relación de las distintas motas que se ubican en la Clinica Fuenlabrada.
* Se extraen las primeras instancias de la base de datos importante: 'clinica_fuenlabrada_1_medidas' y se consiguen generar JSON con los datos.
* Se va a estudiar si el mejor método es el de crear un repositorio en local que permita un control de versiones o únicamente obtenerlos cada un cierto tiempo.
***
#### Versión14 - V.16/10/2019:
* Se añade una pantalla para visualizar la relación de motas en cada edificio.
* Creación de funciones en 'views.py' para abstraer código.
***
#### Versión15 - V.20/10/2019:
* Generación de los JSON correctamente.
* Se introduce una lista de diccionarios del tipo {'id_mota':1,'planta':3,'sensores':2,'gps':[-3.78...,40.78...],'Tipo_medidaX':[medida1,medidaX...]} 
