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
      if( data.error[0] == 0 ){
        window.location = "/perdio?etapa="+e
        return;
      } 

      if( data['gano']){
        window.location = "/gano"
        return;
      }
      
      $('#pregunta').text(data.pregunta)
      $('#respuestas a:eq(0)').text(data.alternativas[0][0])
      $('#respuestas a:eq(1)').text(data.alternativas[1][0])
      $('#respuestas a:eq(2)').text(data.alternativas[2][0])
      $('#respuestas a:eq(3)').text(data.alternativas[3][0])

      $('#etapa li').removeClass('active');
      $('#id_'+data.etapa[2]).addClass('active');
    }
  );
  return false;

}