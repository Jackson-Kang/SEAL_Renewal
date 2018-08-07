$(document).ready(function(){

	$("#register").click(function(){
		var agree1 = $("#agree1").val(),
			agree2 = $("#agree2").val();

		if(false==document.getElementById("agree1").checked || false==document.getElementById("agree2").checked) {
			alert("SEAL 가입을 위해서는 약관 동의가 필요합니다.");
		}
		else {
			alert("등록이 완료되었습니다.");
			document.getElementById("regform").submit();
		}
	});

		

});