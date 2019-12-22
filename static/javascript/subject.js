$(function() {

    $("#sbm").click(function(e) {
        e.preventDefault();
        var url = window.location.pathname;
        var ans = $('input[name="ans"]:checked').val();
        console.log(url, ans);
        if (ans) {
            submitinfo(ans, url);
        }
    }) 
    $("#fill_sbm").click(function(e) {
        e.preventDefault();
        var url = window.location.pathname;
        var ans = $('#fillans').val().replace(/^\s+|\s+$/g, "");
        console.log(url, ans);
        if (ans) {
            submitinfo(ans, url);
        }
    }) 
    $("#multi_sbm").click(function(e) {
        e.preventDefault();
        var url = window.location.pathname;
        var ans = $('input[name="ans"]');
        var answer = ""
        for (k in ans) {
            if (ans[k].checked) answer += ans[k].value;
        }
        console.log(url, answer);
        if (answer) {
            submitinfo(answer, url);
        }
    }) 
    function submitinfo(ans, url) {
        $.ajax({
            type: "post",
            url: url,
            data: {
                "answer": ans
            },
            success: function(data) {
                console.log(data);
                if (data == "1") {
                    $("#judge").text("TRUE").css("color", "green");
                } else if (data == "-1") {
                    $("#judge").text("FALSE").css("color", "red");
                }
                $("#checkans").css("display", "block");
            }
        });
    }
    $("#checkans").click(function(e) {
        e.preventDefault();
        $(".answerandreason").css("display", "block");
    }) 
    $("#collect").click(function(e) {
        e.preventDefault();
        collect();
    }) 
    function collect() {
        $.ajax({
            type: "post",
            url: '/collect',
            success: function(data) {
                console.log(data);
                if (data == "310") {
                    $("#collect_tip").text("已收藏");
                } else if (data == "210") {
                    $("#collect_tip").text("收藏成功");
                }
                $("#disappare").show().delay(1500).hide(300);
            }
        });
    }
    $(".delete").click(function(e) {
        e.preventDefault();
        var id = $(this).data('id');
        deletesub(id);
    });
    function deletesub(id) {
        $.ajax({
            type: "post",
            url: '/deletesub',
            data: {
                "id": id
            },
            success: function(data) {

                //location.reload(true);
                window.location.href = '/collect_list'; //你可以跟换里面的网址，以便成功后跳转
            }
        });
    }
})