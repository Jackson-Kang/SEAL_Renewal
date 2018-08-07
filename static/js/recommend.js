$(document).ready(function()
	{$('.stars').on("click", "input",function(event){
		    event.stopPropagation();
		    $(this).unbind("click");
		    var splitdata = $(this).attr("id");
		    splitdata = splitdata.split("-");
		    var starcount = splitdata[1];
		    $("#StarValue").val(starcount);
		    var object = $("[name='star']");
			$("label.star").css("background","url(/static/assets/icon/star.png) 0 -20px")
			object.each(function()
			{
				if($(this).prop("checked"))
				{
					$(this).next().css("background","url(/static/assets/icon/star.png)");
					return false;
				}

				$(this).next().css("background","url(/static/assets/icon/star.png)");
			})
		 });
 		$("div").on("click",".recommend-course-search",function()
 		{
 			$(".all_course .text").text("")
 			$("#Semester").val("")

 		});
		$("div").on("click",".homework-count",function()
		{
			var object = $(this);
			var img;
			if(object.hasClass("img-top"))
			{
				img="mid";
				$(this).removeClass("img-top");
				$(this).addClass("img-mid");
				$('[name=homework-count]').val('5');
			}
			else if(object.hasClass("img-mid"))
			{
				img="bottom";
				$(this).removeClass("img-mid");
				$(this).addClass("img-bottom");
				$('[name=homework-count]').val('1');
			}
			else if(object.hasClass("img-bottom"))
			{
				img="top";
				$(this).removeClass("img-bottom");
				$(this).addClass("img-top");

				$('[name=homework-count]').val('9');
			}

			$(this).find("img").attr("src","/static/assets/icon/"+img+".png");
		});
		$("div").on("click",".level-diff",function()
		{

			var object = $(this);
			var img;
			if(object.hasClass("img-top"))
	 		{
				img="mid";
				$(this).removeClass("img-top");
				$(this).addClass("img-mid");

	 			$('[name=level-diff]').val('5');
	 		}
	 		else if(object.hasClass("img-mid"))
	 		{
	 			img="bottom";
	 			$(this).removeClass("img-mid");
	 			$(this).addClass("img-bottom");

	 			$('[name=level-diff]').val('1');
	 		}
	 		else if(object.hasClass("img-bottom"))
	 		{
	 			img="top";
	 			$(this).removeClass("img-bottom");
	 			$(this).addClass("img-top");

	 			$('[name=level-diff]').val('9');
	 		}

	 		$(this).find("img").attr("src","/static/assets/icon/"+img+".png");
		
		});	
	 	
		$('div').on("click",".exam-method",function(event)
		{
			event.stopPropagation();
			$(".exam-method").removeClass("method-active");
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
		});
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


		$("#recommend-course-search").before("<div style='float:left; width:13%;height:100%; font-weight:bold; padding-top:7px; padding-left:10px;'>수업검색</div>");
		$("#recommend-course-search").after('<i id="course-search" \
			class="fa fa-caret-down" aria-hidden="true"></i>');
		$("div").on("change","#input-file",function()
		{
			event.stopPropagation();
			var files=$(this)[0].files;
			for(var i=0; i<files.length; i++)
			{
				
			
				$(".jubo").append("<div class='jubo-item' style='padding-left:30px;'><i  class='fa fa-download' aria-hidden='true'></i>"+files[i].name+"</div>")

			}
				
		});
		$('div').on("click","#file-input",function(e){
	        event.stopPropagation();
		
	        $('#input-file').click();

	    });


	});

$(document).ready(function(){
		$("#RecommendForm").form({
			on:'submit',
		    inline : true,
			fields:{
				Semester:{
					identifier:'Semester',
					rules:[
						{
							type : 'empty',
							prompt : '학기를 입력을 하지 않았습니다.'
						},
						{
							type : 'notExactly[0]',
							prompt : "학기가 입력되지 않았습니다."
						},
						
					]
				},
				Course:{
					identifier:'Professor',
					rules:[
						{
							type : 'empty',
							prompt : '수업이 입력되지 않았습니다.'
						}
					]
				}
			},
			templates:{
				error : function(errors)
				{
					return $("<div/>").addClass("ui red prompt label").html(errors[0])
				}
			}
		});
	});
		
