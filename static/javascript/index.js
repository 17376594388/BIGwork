window.onload = function() {
    function getinfo() {
        $.ajax({
            type: "post",
            url: "/index",
            success: function(data) {
                
                var data = JSON.parse(data);
                echarts.init(document.getElementById('finish_option_sub')).setOption(option = {
                    title: {
                        text: '单选题完成情况',
                        x: 'left'
                    },
                    tooltip: {
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        textStyle: { //图例中文字的样式
                            color: '#000',
                            fontSize: 16
                        }
                    },
                    color: ['#008000', '#A9A9A9'],
                    series: {
                        type: 'pie',
                        radius: '80%',
                        //饼图中饼状部分的大小所占整个父元素的百分比
                        center: ['50%', '50%'],
                        //整个饼图在整个父元素中的位置
                        data: [{
                            name: '已完成',
                            value: data[0][0]
                        },
                        {
                            name: '未完成',
                            value: data[0][1]
                        }]
                    }
                });
                echarts.init(document.getElementById('finish_fill_sub')).setOption(option = {
                    title: {
                        text: '填空题完成情况',
                        x: 'left'
                    },
                    tooltip: {
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        textStyle: { //图例中文字的样式
                            color: '#000',
                            fontSize: 16
                        }
                    },
                    color: ['#008000', '#A9A9A9'],
                    series: {
                        type: 'pie',
                        radius: '80%',
                        //饼图中饼状部分的大小所占整个父元素的百分比
                        center: ['50%', '50%'],
                        //整个饼图在整个父元素中的位置
                        data: [{
                            name: '已完成',
                            value: data[1][0]
                        },
                        {
                            name: '未完成',
                            value: data[1][1]
                        }]
                    }
                }); 
                echarts.init(document.getElementById('finish_multioption_sub')).setOption(option = {
                    title: {
                        text: '多选题完成情况',
                        x: 'left'
                    },
                    tooltip: {
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        textStyle: { //图例中文字的样式
                            color: '#000',
                            fontSize: 16
                        }
                    },
                    color: ['#008000', '#A9A9A9'],
                    series: {
                        type: 'pie',
                        radius: '80%',
                        //饼图中饼状部分的大小所占整个父元素的百分比
                        center: ['50%', '50%'],
                        //整个饼图在整个父元素中的位置
                        data: [{
                            name: '已完成',
                            value: data[2][0]
                        },
                        {
                            name: '未完成',
                            value: data[2][1]
                        }]
                    }
                }); 
                echarts.init(document.getElementById('finish_all_sub')).setOption(option = {
                    title: {
                        text: '总体完成情况',
                        x: 'left'
                    },
                    tooltip: {
                        formatter: "{b} : {c} ({d}%)"
                    },
                    legend: {
                        textStyle: { //图例中文字的样式
                            color: '#000',
                            fontSize: 16
                        }
                    },
                    color: ['#008000', '#A9A9A9'],
                    series: {
                        type: 'pie',
                        radius: '80%',
                        //饼图中饼状部分的大小所占整个父元素的百分比
                        center: ['50%', '50%'],
                        //整个饼图在整个父元素中的位置
                        data: [{
                            name: '已完成',
                            value: data[3][0]
                        },
                        {
                            name: '未完成',
                            value: data[3][1]
                        }]
                    }
                });
                echarts.init(document.getElementById('finish_subs')).setOption(option = {
                     title: {
                text: '各种题型完成情况'
            },
            tooltip: {},
            legend: {
                data:['完成量']
            },
            legend: {
                        textStyle: { //图例中文字的样式
                            color: '#000',
                            fontSize: 16
                        }
                    },
            xAxis: {
                data: ["单选题","填空题","多选题"]
            },
            yAxis: {},
            series: [{
                name: '完成量',
                type: 'bar',
                data: [data[4][0], data[4][1], data[4][2]]
            }]
        });
    }
})
    }

    getinfo();

}