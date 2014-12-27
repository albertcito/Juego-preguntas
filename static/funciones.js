$(document).ready(inicio);

function inicio(){

  $("#respuestas a").on( "click", verificaOpcion);
}
function verificaOpcion(){
 
  r = this.text.trim();
  e = $('#etapa li.active').attr('rel')

  $.getJSON('/_verificar_respuesta', {
      respuesta: r,
      etapa: e
    }, function(data) {

      //si error
      if( data.result[0] == 0 ){
        alert('perdió')
        //redireccionar
        return;
      } 

      console.log(data.result.length)
      if( data.result.length == 1 ){
        alert("Gano")
        return;
      }
      
      $('#pregunta').text(data.result[2])
      $('#respuestas a:eq(0)').text(data.result[3][0][0])
      $('#respuestas a:eq(1)').text(data.result[3][1][0])
      $('#respuestas a:eq(2)').text(data.result[3][2][0])
      $('#respuestas a:eq(3)').text(data.result[3][3][0])

      $('#etapa li').removeClass('active');
      $('#id_'+data.result[1][2]).addClass('active');
    }
  );
  return false;

}