 $(document).ready(function(){
 	
 	var urldata = location.href;
    var lastIndex = urldata.lastIndexOf('/');
    var cURL = urldata.substring(lastIndex);
       $(".mdl-layout__content").on("scroll",function() { // 스크롤 이벤트가 발생할 때마다 인식

         // 스크롤이 끝에 닿음을 인식
          if ( $(this).scrollTop() + $(this).innerHeight()+1 >= $(this)[0].scrollHeight ) {

              $('#next').click();
              
          }
          
          });

  $('div').on('click',".Page",function(event){
    event.stopPropagation();

    $.ajax({ 
          url : urldata+"/"+$(this).attr("name"),
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken").val()
                },
          datatype:"json",
          type : "GET",
          async : false,
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          },
          success:function(resp){     
          			$("#next").remove();
                  $(".m-single-course-container").append(resp); 
                  $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
 	$(".open-comment").on("click",function(){
 		if($(this).hasClass("active")){
 			$(this).closest(".content").find(".hidden-content").fadeOut("slow");
 			$(this).closest(".content").find(".hidden-comment").hide();
 			$(this).closest(".content").find(".a-comment").show();
 		}
 		else{
 			var $this = $(this);
 			var a = $(this).closest(".content").find(".hidden-content");
 			$(this).closest(".content").find(".hidden-comment").show();
 			$(this).closest(".content").find(".a-comment").hide();
 			a.css("display","flex").hide().fadeIn("slow", function(){
 				$this.addClass("active");
 			});

 		}
 	})

 	
       
		}
 )