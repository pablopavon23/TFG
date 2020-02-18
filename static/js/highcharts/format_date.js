// I need to change a date/time from 2014-08-20 15:30:00 to look like 08/20/2014 3:30 pm
// https://stackoverflow.com/questions/25275696/javascript-format-date-time
function formatDate(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear() + "  " + strTime;
}

// var d = new Date();
// var e = formatDate(d);
