function doWork() {
  var i, j;
  var dict = {}
  for(i=8; i<11; i++){
    for(j=0; j<4; j++){
      var idString = i.toString() + '/' + j.toString()
      if (document.getElementById(idString).checked){
        dict[idString] = true
      }
      else{
        dict[idString] = false;
      }
    }
  }
  console.log(dict)
// ajax the JSON to the server
//  var json = '{"result":true, "count":42}';
  var json = JSON.stringify(dict);
  $.post("/changed_week", {data:json});
// stop link reloading the page
  event.preventDefault();
}


function confirm_change(){
  var ok = confirm('Are you sure to change the current schedule?');
  if (ok){
    doWork()
    return true;
  }
  return false;
}
