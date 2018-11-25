$(document).ready(function()

	{	
		if($("[name=CourseComment]").attr("data") !="" || $("[name=CourseComment]").attr("data")  != "undefined"){
			var data =$("[name=CourseComment]").attr("data");
			data = data.replace(/<(\/?)p>/gi,"");
			data = data.replace(/(<br>)|(<br \/>)/gi,"\n");
			$("[name=CourseComment]").val(data);
			
		}

		$('.rate').on("click", "input",function(event){
		    event.stopPropagation();
		    $(this).unbind("click");
		    
		    $("#StarValue").val($(this).val());
		 });
 		$("div").on("click",".recommend-course-search",function()
 		{
 			$(".all_course .text").text("")
 			$("#Semester").val("")

 		})
		$("div").on("click",".homework-count",function(event)
		{
			event.stopPropagation();
			var object = $(this);
			var img;
			$(".homework-count").removeClass("top-grade2");
			$(".homework-count").removeClass("middle-grade2");
			$(".homework-count").removeClass("bottom-grade2");
			$(".homework-count").addClass("normal-grade2");
			if($(this).text() == "상") {$(this).addClass("top-grade2"); $('[name=homework-count]').val('9'); $(this).removeClass("normal-grade2");}
			else if($(this).text() == "중"){ $(this).addClass("middle-grade2"); $('[name=homework-count]').val('5'); $(this).removeClass("normal-grade2");}
			else if($(this).text() == "하"){ $(this).addClass("bottom-grade2"); $('[name=homework-count]').val('1'); $(this).removeClass("normal-grade2");}
			
		});
		$("div").on("click",".level-diff",function(event)
		{
			event.stopPropagation();
			$(".level-diff").removeClass("top-grade2");
			$(".level-diff").removeClass("middle-grade2");
			$(".level-diff").removeClass("bottom-grade2");
			$(".level-diff").addClass("normal-grade2");
			if($(this).text() == "상") {
				$(this).addClass("top-grade2");
				$('[name=level-diff]').val('9');
				$(this).removeClass("normal-grade2");
			}
			else if($(this).text() == "중"){ 
				$(this).addClass("middle-grade2");
				$('[name=level-diff]').val('5');
				$(this).removeClass("normal-grade2");
			}
			else if($(this).text() == "하") 
			{
				$(this).addClass("bottom-grade2");
				$('[name=level-diff]').val('1');	
				$(this).removeClass("normal-grade2");
			}

		});	
	 	
		$('div').on("click",".exam-method",function(event)
		{
			event.stopPropagation();
			$(".exam-method").removeClass("method-active");
			$("[name='paper_value[]']").val("0");
			if($(this).hasClass("method-active"))
			{
				$(this).removeClass('method-active');
				$(this).next().val("0");
			}
			else 
			{
				$(this).addClass("method-active");
				$(this).next().val($(this).attr("value"));
			}

		});
		$('div').on("click",".course-method",function()
		{
			event.stopPropagation();

			if($(this).hasClass("method-active"))
			{
				$(this).removeClass('method-active');
				$(this).next().val("0");
			}
			else 
			{
				$(this).addClass("method-active");
				$(this).next().val($(this).attr("value"));
			}
		    
		});

		$("div").on("click",".eac-item",function()
		{
			event.stopPropagation();
			$("[name=Professor]").val($(this).find('.item-professor').text())
			$("[name=Code]").val($(this).find('.item-code').text())
			$("[name=CourseName]").val($(this).find('.item-coursename').text())
			$.ajax({ 
					url : "/Course-Semester/",
					data : {
					'Professor': $("[name=Professor]").val(),
					'Code': $("[name=Code]").val(),
					'CourseName':  $("[name=CourseName]").val(),
					'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val()
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
						$('.menu').html(" ");
						for(var i=0; i<resp.length;i++)
						{
							$(".menu").append('<div class="item semester_item" data-value="'+resp[i].Semester+'">'+resp[i].Semester+'</div>')
						} 

					},
					error: function(xhr, option, error){
						alert(xhr.status); //오류코드
						alert(error); //오류내용
					} 
			});	 	

		});
		$("div").on("click",".semester_item",function()
		{
			$("#Semester").val($(this).attr("data-value"))
		})
		var options = {
			  url: function(phrase) {
			    return "/CourseSearchList/";
			  },


			   getValue: function(element) {
			    return element.CourseName;
			  },
			  list: {	
			    match: {
					enabled: true
				},
				maxNumberOfElements: 8
			  },
			  ajaxSettings:{
			  	dataType: "json",
			    method: "GET",
			 	data:{
			 	}
			   
			  },
			  preparePostData: function(data) {
			  
			    data.phrase = $("#recommend-course-search").val();
			    data.csrfmiddlewaretoken=$("[name=csrfmiddlewaretoken]").val();
			    return data;
			  },
			  template: {
				type: "custom",
				method: function(value, item) {
					return "<div style='display:flex; padding:3 0 3 0;'><p class='item-coursename' style='width:50%; margin:0px;'>" + value+ "</p><p class='item-professor' style='margin:0px;'>"+item.Professor+"</p><p class='item-code' style='display:none;'>"+item.Code+"</p></div>"
				}
			  },
					
			  requestDelay: 400
		};

		$("#recommend-course-search").easyAutocomplete(options);
		$('.easy-autocomplete').css("width","100%");


		
		$("#recommend-course-search").after('<i style="position:absolute; top:25%; right:25px; font-size:25px;" id="course-search" \
			class="fa fa-caret-down" aria-hidden="true"></i>');
		$("div").on("change","#input-file",function()
		{
			event.stopPropagation();
			var files=$(this)[0].files;
			for(var i=0; i<files.length; i++)
			{
				
			
				$(".jubo").append("<div class='jubo-item' style='padding-left:30px;'><i  class='fa fa-download' aria-hidden='true'></i>"+files[i].name+"</div>")

			}
				
		})
		$('div').on("click","#file-input",function(e){
	        event.stopPropagation();
		
	        $('#input-file').click();

	    });


	});

// $(document).ready(function(){
// 		$("#RecommendForm").form({
// 			on:'submit',
// 		    inline : true,
// 			fields:{
// 				Semester:{
// 					identifier:'Semester',
// 					rules:[
// 						{
// 							type : 'empty',
// 							prompt : '학기를 입력을 하지 않았습니다.'
// 						},
// 						{
// 							type : 'notExactly[0]',
// 							prompt : "학기가 입력되지 않았습니다."
// 						},
						
// 					]
// 				},
// 				Course:{
// 					identifier:'Professor',
// 					rules:[
// 						{
// 							type : 'empty',
// 							prompt : '수업이 입력되지 않았습니다.'
// 						}
// 					]
// 				}
// 			},
// 			templates:{
// 				error : function(errors)
// 				{
// 					return $("<div/>").addClass("ui red prompt label").html(errors[0])
// 				}
// 			}
// 		})
// 	})
		