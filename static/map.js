//document.getElementById('downloadLink').click();

$('input[type="checkbox"]').on('change', function() {
   $('input[type="checkbox"]').not(this).prop('checked', false);
   for_turtle = document.getElementById('turtle');
   if (for_turtle.checked){
      localStorage.setItem("turtle", "selected");
   } else{localStorage.setItem("turtle", "notSelected");}

});

if (!document.onload){
   onLoad__();
}

function onLoad__(){
   document.getElementById('loading2').classList.toggle('invisibility');
   //document.getElementById('loading3').classList.toggle('invisibility');
   //document.getElementById('loading_box_').classList.toggle('invisibility');

}

function loading_(){
   document.getElementById('loading2').classList.remove('invisibility');
   //document.getElementById('loading3').classList.remove('invisibility');
   //document.getElementById('loading_box_').classList.remove('invisibility');

}

element = document.getElementsByName("uploadFile");
element.addEventListener("click",download_());


function download_(){
for(let i = 1; i<9; i++){
   if(document.getElementById(String(i))){
      document.getElementById(String(i)).click();
   }

}
}

