var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  console.log(this.status)
  if (this.readyState == 4 && this.status == 200) {
    var myObj = JSON.parse(this.responseText);
    document.getElementById("demo").innerHTML = myObj.name;
  }
};
xmlhttp.open("GET", "json_demo.txt", true);
xmlhttp.send();
