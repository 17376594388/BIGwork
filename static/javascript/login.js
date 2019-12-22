$(function(){
	
	$("#login").click(function(e){
		e.preventDefault();
		$("#tip").text("");
		login($("#lg_username").val(),$("#lg_userpwd").val());
	})

	function login(username,userpwd){
		$.ajax({
			type:"post",
			url:"/login",
			data:{"username":username,"userpwd":userpwd},
			success:function(data){
				console.log(data);
				if(data=="300"){
					$("#tip").text("账号或密码错误");
				}
				else if(data=="307"){
					$("#tip").text("账号或密码不能为空");
				}
				else if(data=="200"){
					window.location.href='/index';
				}
			}
		});
	}

})
