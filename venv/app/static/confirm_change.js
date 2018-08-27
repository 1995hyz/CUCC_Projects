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
  $.post("/changed_week", {data:json}).done(function(response){
    location.reload();
  });
  event.preventDefault();
}


function get_schedule_change(e){
  event = e;
  slots_dic = {}
  var i, j;
  for(i=0; i<24; i++){
    for(j=0; j<4; j++){
      var idString = i.toString() + '/' + j.toString()
      input_context = document.getElementById(idString)
      if (!input_context.disabled){
        if (input_context.value){
          slots_dic[idString] = input_context.value;
        }
        else{
          slots_dic[idString] = "";
        }
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
  $.post("/changed_schedule", {data:json}).done(function(response){
    location.reload();
  });
  event.preventDefault();
}


function get_schedule_change_operator(e, identifier){
  event = e;
  slots_dic = {}
  var i, j;
  for(i=0; i<24; i++){
    for(j=0; j<4; j++){
      var idString = i.toString() + '/' + j.toString()
      input_context = document.getElementById(idString)
      if (!input_context.disabled){
        if (input_context.value){
          slots_dic[idString] = input_context.value
        }
        else{
          slots_dic[idString] = ""
        }
      }
    }
  }
  if (identifier=='week'){
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
    $.post("/changed_schedule", {data:json}).done(function(response){
      location.reload();
    });
    event.preventDefault();
  }
  else if (identifier=='date'){
    slots_dic["date"] = document.getElementById("date_index").textContent;
    console.log(slots_dic);
    var json = JSON.stringify(slots_dic);
    $.post("/changed_date", {data:json}).done(function(response){
      location.reload();
    });
    event.preventDefault();
  }
  else{
    console.log("Shouldn't be here.")
  }
}


function get_sign_in(e){
  event = e;
  var indexes = document.getElementsByName("index");
  var i;
  slots_dic = {};
  for(i=0; i<indexes.length; i++){
    num_string = i.toString();
    slots_dic[num_string+"-signed"] = document.getElementById(num_string+"signed").value;
    slots_dic[num_string+"-replaced"] = document.getElementById(num_string+"replaced").value;
  }
  slots_dic["time"] = document.getElementById('time').textContent;
  times = slots_dic["time"].split("-")
  sub_url = times[0] + "-" + times[1] + "-" + times[2] + "/" + times[3]
  console.log(slots_dic);
  // ajax the JSON to the server
  var json = JSON.stringify(slots_dic);
  $.post("/changed_sign_in/", {data:json}).done(function(response){
    location.reload();
  });
  event.preventDefault();
}


function confirm_change(e, form_index){
  evt = e || window.event
  var ok = confirm('Are you sure to change the current schedule?');
  switch (form_index) {
    case 1:
      if (ok){
        get_schedule_change(evt);
        return true;
      }
      return false;
      break;
    case 2:
      if (ok){
        get_schedule_change_operator(evt, 'week');
        return true;
      }
      return false;
      break;
    case 3:
      if (ok){
        get_schedule_change_operator(evt, 'date');
        return true;
      }
      return false;
      break;
    case 4:
      if(ok){
        get_sign_in(evt);
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
