var start;
var id;

$(function(){
	
	$("#sendfb").click(function(e){
		e.preventDefault();
		var param=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
		if(param.test($("#fb_username").val())){
			disabled();
			sendFBMail($("#fb_username").val());
		}
		else{
			alert("邮箱格式错误");
		}
	})

	$("#findback").click(function(e){
		e.preventDefault();
		$("#tip3").text("").css("color","red");
		sendFBinfo($("#fb_username").val(),$("#fb_checknum").val(),$("#fb_userpwd").val(),$("#fb_userpwdagain").val())
	})

	function sendFBMail(address){
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

	function sendFBinfo(username,checknum,newpwd,newpwdagain){
		$.ajax({
			type : "post",
			url:"/findback",
			data:{"username":username,"checknum":checknum,"newpwd":newpwd,"newpwdagain":newpwdagain},
			success:function(data){
				console.log(data);
				if(data=="301")
					$("#tip3").text("此邮箱与验证邮箱不一致");
				else if(data=="302")
					$("#tip3").text("验证码错误");
			    else if(data=="303")
					$("#tip3").text("密码不一致");
				else if(data=="305")
					$("#tip3").text("邮箱不存在");
				else if(data=="202")
					$("#tip3").text("修改成功").css("color","green");
				else if(data=="308")
					$("#tip3").text("密码不能为空");
			}
		});
	}

	function disabled(){
		$("#sendfb").attr("disabled", "disabled");
    	start = Date.now();

    	id = setInterval(() => {
        t = 120-parseInt((Date.now()-start)/1000);
        $("#sendfb").text(t+"秒后重新获取");
        if(t<=0){
           clearInterval(id);
           $("#sendfb").removeAttr('disabled').text('获取验证码');
        }
    }, 1000);
	}

})