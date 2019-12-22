var start;
var id;

$(function(){

	$("#sende").click(function(e){
		e.preventDefault();
		var param=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
		if(param.test($("#sg_username").val())){
			disable();
			sendMail($("#sg_username").val());
		}
		else{
			alert("邮箱格式错误");
		}
	})

	$("#signup").click(function(e){
		e.preventDefault();
		$("#tip2").text("");
		sendinfo($("#sg_username").val(),$("#checknum").val(),$("#sg_userpwd").val(),$("#sg_userpwdagain").val());
	})

	function sendinfo(username,checknum,userpwd,userpwdagain){
		//console.log(username,checknum,userpwd,userpwdagain);
		$.ajax({
			type : "post",
			url:"/signup",
			data:{"username":username,"checknum":checknum,"userpwd":userpwd,"userpwdagain":userpwdagain},
			success:function(data){
				console.log(data);
				if(data=="301")
					$("#tip2").text("注册的邮箱与验证邮箱不一致");
				else if(data=="302")
					$("#tip2").text("验证码错误");
				else if(data=="303")
					$("#tip2").text("密码不一致");
				else if(data=="304")
					$("#tip2").text("注册邮箱已存在");
				else if(data=="308")
					$("#tip2").text("密码不能为空");
				else if(data=="200"){
					window.location.href='/index';
				}
			}
		});
	}
	
	function sendMail(address){
		$.ajax({
			type : "post",  
         	url : "/sendMail",  
         	data : {"address":address},  
         	async : false,  
         	success : function(data){  
            	if(data=="201")
            		console.log("发送成功")
            	else if(data=="306")
            		console.log("发送失败")
         	}  
		});
	}

	function disable(){
    $("#sende").attr("disabled", "disabled");
    start = Date.now();

    id = setInterval(() => {
        t = 120-parseInt((Date.now()-start)/1000);
        $("#sende").text(t+"秒后重新获取");
        if(t<=0){
           clearInterval(id);
           $("#sende").removeAttr('disabled').text('获取验证码');
        }
    }, 1000);
}



})