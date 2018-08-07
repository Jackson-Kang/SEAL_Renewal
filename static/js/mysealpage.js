$(document).ready(function()
{
  $('div').on('click','.course_delete',function(event){
        event.stopPropagation();
        $(this).unbind("click");
        var confirm1 = window.confirm("이 강의를 삭제하시겠습니까?");
        if(!confirm1)
          return;

        
        $.ajax({ 
              url : "/MyPage/DeleteCourse/",
              data : {
                'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
                  'id':$(this).parent().attr("id")
              },
              
              datatype:"json",
              type : "POST",
              async:true,
              success:function(resp){     
                location.reload();
              },
                error: function(xhr, option, error){
                  alert(xhr.status); //오류코드
                  alert(error); //오류내용
              } 
            
          });
    });
$('div').on('click','.course_edit',function(event){
	event.stopPropagation();
	alert("수정 기능은 현재 버그 수정중입니다.\n조금만 기다려주세요.");
/*
        event.stopPropagation();
          $(this).unbind("click");
          var form = $("<form></form>");
          form.attr("method","POST");
          form.attr("action","/MyPage/UpdateRedirectCourse/");
            var inputdata ={
              'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
              'id': $(this).parent().attr("id"),
              
            }
            var input; 
            for(key in inputdata)
            {
              input= document.createElement("input");
              input.name =key;
              input.value=inputdata[key];
              input.type="hidden";
              form.append(input);
            }
            $("body").append(form);
            form.submit();    
*/
    });

    $("div").on("click",".open-comment",function()
    { 
      event.stopPropagation();
      var position = $(this).prev()
      var prevthis = $(this)
      prevthis.html("<p>접기</p>")
      $(position).slideDown("slow",function()
      {
        prevthis.removeClass("open-comment");
        prevthis.addClass("close-comment");
        
      });
    
    })
    $("div").on("click",".close-comment",function()
    { 
      event.stopPropagation();
      var position = $(this).prev()
      var prevthis = $(this)
      prevthis.html("<p>상세 더보기</p>")
      $(position).slideUp("slow",function()
      {
        prevthis.removeClass("close-comment");
        prevthis.addClass("open-comment");
        
      });

    })
    
    $('form').on('click', '#changebtn4',function(){
      var newnick = $('#Nickname').val();
      if(newnick.length >= 2 && newnick.length <= 10){
        if( newnick.indexOf(" ") !== -1 ){
          alert("잘못된 입력입니다");
        }
        else{
        //connect to DB at here
          $.ajax(
          {
            url : "/MyPage/NickNameChange/",
            data : {  
              'Nickname' : $('#Nickname').val(),
               'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
            },
            type : "POST",
            success:function(resp){  
              alert('Successfully changed!');
              location.reload();
              } ,
            error: function(xhr, option, error){
              alert('중복되는 닉네임이 존재합니다'); //오류내용
            }
            });

          }
      }
      else {
        alert('닉네임은 2자 이상 10자 이하로 사용해야 합니다');
      }
      });
  })
  
