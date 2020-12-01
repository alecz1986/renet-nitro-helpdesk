success_perf = function(data){
    console.log(data);
  data = $(data);
  sel_in =  $('select#performer_id');
  sel_in.children().remove();
  data.children('option').appendTo(sel_in);
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

/*
tested = function(data){
    data = $(data);
    console.log(data);
}
*/

(function($){
   $(document).ready(function(){ 
    /*
    $.ajax({
          type: 'GET',
          url: 'http://helpdesk.renet.ru:8006/?age=882025',
          data: {'age': '882025'}

      });
    */
    
	$('select#performer').change(function(){
	console.log('aaa');
    group_id = $('select#performer').val();
    
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
    console.log("data us :"+$('select#performer').val());
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
