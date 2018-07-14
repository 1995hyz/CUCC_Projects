function toggle(checkboxID, toggleName) {
     var checkbox = document.getElementById(checkboxID);
     var toggle = document.getElementsByName(toggleName);
     for(var i=0;i<toggle.length;i++){
        updateToggle = checkbox.checked ? toggle[i].disabled=false : toggle[i].disabled=true;
     }
}
