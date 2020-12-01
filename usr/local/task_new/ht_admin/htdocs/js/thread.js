success_perf = function(data){
  data = $(data);
  sel_in =  $('select#performer_id');
  sel_in.children().remove();
  data.children('option').appendTo(sel_in);
};
testa = function(data){
  data = $(data);
  console.log(data.text());
};
success_message = function(data){
  data = $(data);
  phone =  data.children('phone').text();
  if (phone != '') {
	$("input[name='phone']").val(phone);
  };
};
success_comment = function(data){
  data = $(data);
  $('textarea#message').val("");
  $('input#send').removeAttr('checked');
  sms = data.children('sms').text();
  $('textarea#sms').val(sms);
  $('textarea#message').val(data.children('textarea').val());
  send = data.children('send').text();
  $('input#send').val(0);
  if (send == '1'){
  	$('input#send').attr('checked', 1);
  	$('input#send').val(1);

  }
  $('div#inst').children().remove();
  data.children('pre#comment').appendTo($('div#inst'));
};

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;
                        
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
                                
        if (sParameterName[0] === sParam) {
	    return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

(function($){
 $(document).ready(function(){
    if (window.location.search.indexOf('id=') > -1 && $('#importance').length > 0 ) {
	//console.log('make request for check: '+getUrlParameter('id') );
	
	$.ajax({
          type: 'GET',
          url: '/importance.php',
          data: {'id': getUrlParameter('id')},
          success: function(data) {
            if(data != ''){
    		$("#importance").val(data);
    	    }
          }
	});
	
	
    }
	
	
	$('select#performer').change(function(){
    group_id = $('select#performer').val();
    $.ajax({
          type: 'POST',
          url: '/perf',
          data: {'id':group_id},
          success: success_perf,

      });
  });
	$('select#title_id').change(function(){
    task_id = $('select#title_id').val();
    th_id = $('input[id="se.id"]').val()
    if (th_id == undefined){th_id=0}
    $.ajax({
          type: 'POST',
          url: '/comment',
          data: {'task_id':task_id,
	  	thread_id:th_id},
          success: success_comment
      });
  });
  if ($('div#perf').text()){
    group_id = $('select#performer').val();
    $.ajax({
          type: 'POST',
          url: '/perf',
          data: {'id':group_id, 'perf_id':$('div#perf').text()},
          success: success_perf
      });
  };
  if ($('select#title_id').val()){
    $.ajax({
          type: 'POST',
          url: '/comment',
          data: {'task_id':$('select#title_id').val()},
          success: success_comment
      });
  };
  $('input#send').click(function() {
    if ($('input#send').val() == 1) {$('input#send').val(0)}
    else {$('input#send').val(1)}
  });
  $("input[name='phone']").mask("(999) 999-9999");
  if ($("input[name='phone']").val()== ''){
    $('textarea#message').change(function(){
      $.ajax({
          type: 'POST',
          url: '/message',
          data: {'message':$('textarea#message').val()},
          success: success_message,

      });
    });
  }

 });
})(jQuery);
