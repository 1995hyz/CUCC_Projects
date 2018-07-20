function doWork(e) {
  event = e
  var i, j;
  var dict = {}
  for(i=0; i<24; i++){
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
  switch (document.getElementById("week_index").textContent) {
    case "Tuesday":
      dict["week"] = 1;
      break;
    case "Wednesday":
      dict["week"] = 2;
      break;
    case "Thursday":
      dict["week"] = 3;
      break;
    case "Friday":
      dict["week"] = 4;
      break;
    case "Saturday":
      dict["week"] = 5;
      break;
    case "Sunday":
      dict["week"] = 6;
      break;
    default:
      dict['week'] = 0;
  }
  console.log(dict);
// ajax the JSON to the server
  var json = JSON.stringify(dict);
  $.post("/changed_week", {data:json});
  //event.preventDefault();
}


function get_schedule_change(e){
  event = e;
  slots_dic = {}
  var i, j;
  for(i=0; i<24; i++){
    for(j=0; j<4; j++){
      var idString = i.toString() + '/' + j.toString()
      input_context = document.getElementById(idString)
      if (input_context.value){
        slots_dic[idString] = input_context.value
      }
      else{
        slots_dic[idString] = ""
      }
    }
  }
  switch (document.getElementById("week_index").textContent) {
    case "Tuesday":
      slots_dic["week"] = 1;
      break;
    case "Wednesday":
      slots_dic["week"] = 2;
      break;
    case "Thursday":
      slots_dic["week"] = 3;
      break;
    case "Friday":
      slots_dic["week"] = 4;
      break;
    case "Saturday":
      slots_dic["week"] = 5;
      break;
    case "Sunday":
      slots_dic["week"] = 6;
      break;
    default:
      slots_dic['week'] = 0;
  }
  console.log(slots_dic);
// ajax the JSON to the server
  var json = JSON.stringify(slots_dic);
  $.post("/changed_schedule", {data:json});
  //event.preventDefault();
}


function confirm_change(e, form_index){
  evt = e || window.event
  var ok = confirm('Are you sure to change the current schedule?');
  switch (form_index) {
    case 1:
      if (ok){
        get_schedule_change(evt);
        console.log("wow");
        return true;
      }
      return false;
      break;
    default:
      if (ok){
        doWork(evt);
        return true;
      }
      return false;
  }
}
