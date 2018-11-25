
$(document).ready(function()
{

  $('div').on('click',".Page",function(event){
    event.stopPropagation();
    $(this).unbind("click");
    $.ajax({ 
          url : "/Page/"+$(this).attr("name"),
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
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
                  $(".course-page").append(resp); 
                  $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
  $('div').on('click',".CPage",function(event){
    event.stopPropagation();
    $(this).unbind("click");

    var category = $("#category").val();
    var major= $("#major").val();
    var ordered=$("#ordered").val();
    $.ajax({ 
          url : "/CPage/"+$(this).attr("name"),
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
                  'category':category,
                  'major':major,
                  'ordered':ordered,
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
                  $(".course-page").append(resp); 
                  $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              // alert(xhr.status); //오류코드
              // alert(error); //오류내용

              } 
         });

    });
   $('div').on('click',".SPage",function(event){
    event.stopPropagation();
    $(this).unbind("click");
    $.ajax({ 
          url : "/SPage/"+$(this).attr("name"),
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
                  'search':$("[name=search]").val() 
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
                  $(".search-page").append(resp); 
                  $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
   $('div').on('click',".MPage",function(event){
    event.stopPropagation();
    $(this).unbind("click");
    $.ajax({ 
          url : "/MyCourse/"+$(this).attr("name"),
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
                 
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
                 if($("body").find(".course-page").length!=0)
                  {
                    $(".course-page").html(resp); 

                  }
                  else if($("body").find(".search-page").length!=0)
                  { 
                   $(".search-page").html(resp); 

                  }
                   $('span.starvalue').starvalue();
            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
   $('div').on('click',".mycourse",function(event){
    event.stopPropagation();
    $(this).unbind("click");
    $.ajax({ 
          url : "/MyCourse/",
          data : {
                  'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
                  
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
                  if($("body").find(".course-page").length!=0)
                  {
                    $(".course-page").html(resp); 

                  }
                  else if($("body").find(".search-page").length!=0)
                  { 
                   $(".search-page").html(resp); 

                  }
                   $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
  $("div").on("click",".course-item",function()
  {
    event.stopPropagation();
    $(this).unbind("click");
    location.href=$(this).attr("link");
  })
  $(".mdl-layout__content").on("scroll",function() { // 스크롤 이벤트가 발생할 때마다 인식

         // 스크롤이 끝에 닿음을 인식
          if ( $(this).scrollTop() + $(this).innerHeight()+1 >= $(this)[0].scrollHeight ) {

              $('#next').click();
              
          }
          
          });


      
 })