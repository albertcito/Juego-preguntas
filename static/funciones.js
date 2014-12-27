$(document).ready(inicio);
e = 5000;
function inicio(){

  $("#respuestas a").on( "click", verificaOpcion);
}
function verificaOpcion(){
 
  r = this.text.trim();

  $.getJSON('/_verificar_respuesta', {
      respuesta: r,
      etapa: e
    }, function(data) {
      console.log(data)
    }
  );
  return false;

}