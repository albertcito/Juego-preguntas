$(document).ready(inicio);

function inicio(){

  $("#respuestas").on( "click","a", verificaOpcion);
  $("#porciento").click(porciento);
  $("#otra_pregunta").click(otra_pregunta);

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
        //alert("perdio")
        window.location = "/perdio?etapa="+e
        return;
      } 

      if( data['gano']){
        window.location = "/gano"
        return;
      }
      
      $('#pregunta').text(data.pregunta)
      $('#pregunta').attr('rel',data.id_pregunta)
      $('#respuestas')
        .html('')
        .append('<a  href="javascrip:;" class="btn btn-primary">'+data.alternativas[0][0]+'</a> ')
        .append('<a  href="javascrip:;" class="btn btn-warning">'+data.alternativas[1][0]+'</a> ')
        .append('<a  href="javascrip:;" class="btn btn-info">'+data.alternativas[2][0]+'</a> ')
        .append('<a  href="javascrip:;" class="btn btn-success">'+data.alternativas[3][0]+'</a> ')

      $('#etapa li').removeClass('active');
      $('#id_'+data.etapa[2]).addClass('active');
    }
  );
  return false;

}

function porciento(){
    
    boton = this.remove();
    p = $('#pregunta').attr('rel');

    $.getJSON('/_porciento', {
        id_pregunta: p
      }, function(data) {
           $('#respuestas')
            .html('')
            .append('<a  href="javascrip:;" class="btn btn-primary">'+data.alternativas[0]+'</a> ')
            .append('<a  href="javascrip:;" class="btn btn-warning">'+data.alternativas[1]+'</a> ')
      }
    );
}

function otra_pregunta(){
    boton = this.remove();
    p = $('#pregunta').attr('rel');
    e = $('#etapa li.active').attr('rel')

    $.getJSON('/_otra_pregunta', {
        id_pregunta: p,
        no_etapa:e
      }, function(data) {
           
          $('#pregunta').text(data.pregunta)
          $('#pregunta').attr('rel',data.id_pregunta)
          $('#respuestas')
            .html('')
            .append('<a  href="javascrip:;" class="btn btn-primary">'+data.alternativas[0][0]+'</a> ')
            .append('<a  href="javascrip:;" class="btn btn-warning">'+data.alternativas[1][0]+'</a> ')
            .append('<a  href="javascrip:;" class="btn btn-info">'+data.alternativas[2][0]+'</a> ')
            .append('<a  href="javascrip:;" class="btn btn-success">'+data.alternativas[3][0]+'</a> ')
          }
    );
}
