$(document).ready(function(){

	$("#check").click(function(){
		var username = $("#username").val();

		if(username == ""){
			$('#username').css("border", "2px solid red");
			$('#username').css("box-shadow", "0 0 3px red");
			alert("Please fill in the username.");
		}
		else{
			$.post("registerconfirm.php", {username1: username}, function(data){
				if(data == 0){
					$('#username').css({"border": "2px solid red", "box-shadow":"0 0 3px red"});
					alert('사용 불가능한 아이디입니다.');
				}
				else if(data == 1){
					$('#username').css("border", "2px solid #ccc");
					$('#username').css("box-shadow", "0 0 3px #ccc");
					alert('사용 가능한 아이디입니다.');
				}
				else{
					alert(data);
				}
			});
		}
	});

	$("#register").click(function(){
		var username = $("#username").val(),
			password = $("#password").val(),
			repassword = $("#repassword").val(),
			email = $("#email").val();

		if(username == "" || password == "" || repassword == "" || email == ""){
			$('input[type="text"], input[type="password"]').css("border", "2px solid red");
			$('input[type="text"], input[type="password"]').css("box-shadow", "0 0 3px red");
			alert("Please fill in the fields.");
			return false;
		}
		else if(password != repassword){
			$('input[type="text"], input[type="password"]').css("border", "2px solid #ccc");
			$('input[type="text"], input[type="password"]').css("box-shadow", "0 0 3px #ccc");
			$('#repassword').css("border", "2px solid red");
			$('#repassword').css("box-shadow", "0 0 3px red");
			alert("Password is different.");
			return false;
		}
		else if(/^[a-zA-Z0-9- ]*$/.test(username) == false || /^[a-zA-Z0-9- ]*$/.test(password) == false){
			$('input[type="text"], input[type="password"]').css("border", "2px solid #ccc");
			$('input[type="text"], input[type="password"]').css("box-shadow", "0 0 3px #ccc");
			alert('Do not contain illegal characters.');
			return false;
		}
		else{
			$.post("register.php", {username1: username, password1: password, email1: email}, function(data){
				if(data == 0){
					alert("Registration failed");
				}
				else{
					alert(data);
					window.location.href = "../Confirm"
					return true;
				}
			});
		}
	});

	

});