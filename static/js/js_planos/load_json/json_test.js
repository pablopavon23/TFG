var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function()
  {
    if (this.readyState == 4 &amp;&amp; this.status == 200)
    {
      var dataArray = JSON.parse(this.responseText);

      var i, j;
      var displayData = "";

      for (i in dataArray.programming_languages)
      {
        for (j in dataArray.programming_languages[i].description)
        {
          displayData += "<b>Name: </b> " + dataArray.programming_languages[i].name + "<br>";
          displayData += "<b>Designed by: </b> " + dataArray.programming_languages[i].designed_by + "<br>";
          displayData += "<b>Latest Release: </b> " + dataArray.programming_languages[i].latest_release + "<br>";
          displayData += "<b>Object Oriented: </b> " + dataArray.programming_languages[i].paradigm.object_oriented + "<br>";
          displayData += "<b>Description: </b> " + dataArray.programming_languages[i].description[j].description_data + "<br>";
          displayData += "<br><hr>";
        }
      }
    }

    document.getElementById("displayData").innerHTML = displayData;
  };

  xmlhttp.open("GET", "programmingLanguages.json", true);
  xmlhttp.send();
