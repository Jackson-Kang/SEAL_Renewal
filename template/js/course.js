 $(document).ready(function(){
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

	}
 )
 $(document).ready(function()
{
  
	var urldata = location.href;
    var lastIndex = urldata.lastIndexOf('/');
    var cURL = urldata.substring(lastIndex);
       
  $('div').on('click',".Page",function(event){
    event.stopPropagation();
    $(this).unbind("click");
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
                  $(".single-course-evaluation-container").html(resp); 
                  $('span.starvalue').starvalue();

            },
            error: function(xhr, option, error){
              alert(xhr.status); //오류코드
              alert(error); //오류내용

              } 
         });

    });
 
})