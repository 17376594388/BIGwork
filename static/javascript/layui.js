layui.use('layer', function() {
    var $ = layui.jquery,
        layer = layui.layer;
        
    var active = {
        offset: function(othis) {
            var type = othis.data('type'),
                id=othis.data('id'),
                text = othis.text();
            getsubmit(id,type);
        }
    };

    $('#layerDemo .layui-btn').on('click', function() {
        var othis = $(this),
            method = othis.data('method');othis
        active[method] ? active[method].call(this, othis) : '';
    });
});

function getsubmit(subid,type1){
    $.ajax({
        type:"post",
        url:'/collect_list',
        data:{"subid":subid},
        success:function(data){
            console.log(data);
            if(data.ID<1000){
                layer.open({
                    type: 1,
                    offset: type1 //具体配置参考：http://www.layui.com/doc/modules/layer.html#offset
                        ,
                    id: 'layerDemo' + type1 //防止重复弹出
                        ,
                    area:["500px","400px"],
                    content: '<div style="width:90%;height:50%;margin:0 auto;margin-top: 10%;word-wrap: break-word;">'+
                    '<div style="padding: 2px 2px;">' + data.ID +' . '+data.text+ '</div>'+
                    '<div style="padding: 2px 2px;">A.' + data.ansA + '</div>'+
                    '<div style="padding: 2px 2px;">B.' + data.ansB + '</div>'+
                    '<div style="padding: 2px 2px;">C.' + data.ansC + '</div>'+
                    '<div style="padding: 2px 2px;">D.' + data.ansD + '</div>'+
                    '<br></br>'+
                    '<div style="padding: 2px 2px;">已选择:' + data.useran + '</div>'+
                    '<div style="padding: 2px 2px;">正确答案:' + data.ans + '</div>'+
                    '<div style="padding: 2px 2px;">解释:' + data.reason + '</div>'+
                    '</div>',
                    btn: '关闭',
                    btnAlign: 'c' //按钮居中
                        ,
                    shade: 0 //不显示遮罩
                        ,
                    yes: function() {
                        layer.closeAll();
                    }
                });
            }
            else if(data.ID<2000){
                layer.open({
                    type: 1,
                    offset: type1 //具体配置参考：http://www.layui.com/doc/modules/layer.html#offset
                        ,
                    id: 'layerDemo' + type1 //防止重复弹出
                        ,
                    area:["500px","400px"],
                    content: '<div style="width:90%;height:50%;margin:0 auto;margin-top: 10%;word-wrap: break-word;">'+
                    '<div style="padding: 2px 2px;">' + data.ID +' . '+data.text+ '</div>'+
                    '<br></br>'+
                    '<div style="padding: 2px 2px;">已填写:' + data.useran + '</div>'+
                    '<div style="padding: 2px 2px;">正确答案:' + data.ans + '</div>'+
                    '<div style="padding: 2px 2px;">解释:' + data.reason + '</div>'+
                    '</div>'
                    ,
                    btn: '关闭',
                    btnAlign: 'c' //按钮居中
                        ,
                    shade: 0 //不显示遮罩
                        ,
                    yes: function() {
                        layer.closeAll();
                    }
                });
            }
            else if(data.ansE==''){
                layer.open({
                    type: 1,
                    offset: type1 //具体配置参考：http://www.layui.com/doc/modules/layer.html#offset
                        ,
                    id: 'layerDemo' + type1 //防止重复弹出
                        ,
                    area:["500px","400px"],
                    content: '<div style="width:90%;height:50%;margin:0 auto;margin-top: 10%;word-wrap: break-word;">'+
                    '<div style="padding: 2px 2px;">' + data.ID +' . '+data.text+ '</div>'+
                    '<div style="padding: 2px 2px;">A.' + data.ansA + '</div>'+
                    '<div style="padding: 2px 2px;">B.' + data.ansB + '</div>'+
                    '<div style="padding: 2px 2px;">C.' + data.ansC + '</div>'+
                    '<div style="padding: 2px 2px;">D.' + data.ansD + '</div>'+
                    '<br></br>'+
                    '<div style="padding: 2px 2px;">已选择:' + data.useran + '</div>'+
                    '<div style="padding: 2px 2px;">正确答案:' + data.ans + '</div>'+
                    '<div style="padding: 2px 2px;">解释:' + data.reason + '</div>'+
                    '</div',
                    btn: '关闭',
                    btnAlign: 'c' //按钮居中
                        ,
                    shade: 0 //不显示遮罩
                        ,
                    yes: function() {
                        layer.closeAll();
                    }
                });
            }
            else{
                layer.open({
                    type: 1,
                    offset: type1 //具体配置参考：http://www.layui.com/doc/modules/layer.html#offset
                        ,
                    id: 'layerDemo' + type1 //防止重复弹出
                        ,
                    area:["500px","400px"],
                    content: '<div style="width:90%;height:50%;margin:0 auto;margin-top: 10%;word-wrap: break-word;">'+
                    '<div style="padding: 2px 2px;">' + data.ID +' . '+data.text+ '</div>'+
                    '<div style="padding: 2px 2px;">A.' + data.ansA + '</div>'+
                    '<div style="padding: 2px 2px;">B.' + data.ansB + '</div>'+
                    '<div style="padding: 2px 2px;">C.' + data.ansC + '</div>'+
                    '<div style="padding: 2px 2px;">D.' + data.ansD + '</div>'+
                    '<div style="padding: 2px 2px;">E.' + data.ansE + '</div>'+
                    '<br></br>'+
                    '<div style="padding: 2px 2px;">已选择:' + data.useran + '</div>'+
                    '<div style="padding: 2px 2px;">正确答案:' + data.ans + '</div>'+
                    '<div style="padding: 2px 2px;">解释:' + data.reason + '</div>'+
                    '</div>',
                    btn: '关闭',
                    btnAlign: 'c' //按钮居中
                        ,
                    shade: 0 //不显示遮罩
                        ,
                    yes: function() {
                        layer.closeAll();
                    }
                });
            }
        }
    });
}