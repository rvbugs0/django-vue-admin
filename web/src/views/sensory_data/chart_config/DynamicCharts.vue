<script setup>

import { ref } from "vue";
import * as echarts from 'echarts';

import { request } from '@/api/service'

const charts = ref([])

var chartConfigObjs = []
const urlPrefix = '/api/system/chart_config/get_charts_data/'


var promise = request({
    url: urlPrefix,
    method: 'get',
    params: { page: 1, limit: 999 }
})

promise.then(function (data) {

    chartConfigObjs = data;

    // console.log(chartConfigObjs);
    chartConfigObjs.forEach(e => {

        charts.value.push(e)
        setTimeout(loadChart, 1000)

    });


});




function getOption(element) {
    let option;
    if (element.type == "line" || element.type == "area") {

        option = {
            title: {
                left: 'center',
                text: element.title
            },
            xAxis: {
                type: 'category',
                data: element.xData
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: element.yData,
                    type: 'line',
                    smooth: true

                }
            ]
        };

        if (element.type == "area") {
            option.series.forEach(e => { e.areaStyle = {} });
        }



    } else if (element.type == "pie") {

        option = {
            title: {
                left: 'center',
                text: element.title
            },

            tooltip: {
                trigger: 'item'
            },
            legend: {
                top: '5%',
                left: 'center'
            },
            series: [
                {
                    name: element.tooltipTitle,
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: 40,
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: element.data
                }
            ]
        };




    } else if (element.type == "stacked-line") {
        option = {
            title: {
                text: element.title,
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                top: '5%',
                left: 'center',

                data: element.data.map((e) => {
                    return e.name;
                })
            },
            grid: {

                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: element.xData
            },
            yAxis: {
                type: 'value'
            },
            series: element.data
        };


    } else if (element.type == "bar") {
        option = {
            title: {
                left: 'center',
                text: element.title
            },

            xAxis: {
                type: 'category',
                data: element.xData
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: element.yData,
                    type: 'bar'
                }
            ]
        };
    }
    return option;
}



function loadChart() {

    charts.value.forEach(element => {


        var chartDom = document.getElementById(element.id + '_chart');
        var myChart = ""
        if(echarts.getInstanceByDom(chartDom)){
            myChart = echarts.getInstanceByDom(chartDom);
        }else{
            myChart = echarts.init(chartDom);

        }
        
        var option = getOption(element);



        option && myChart.setOption(option);






    });

};




</script>



<template>
    <div id="chart_container">

        <div v-for="chart in charts" :id="chart.id + '_chart'"  style="height:420px;width: 560px;display: block;"
            class="chart_box"></div>





    </div>
</template>


<style scoped>
#chart_container {

    background-color: white;
    align-items: center;
    display: flex;
    flex-direction: row;
    padding: 25px;
    min-height: 100vh;
    min-width: 100%;
    color: black;
    flex-wrap: wrap;
    overflow: scroll;
    height: 800px;
    padding-bottom: 250px;
}

.chart_box {
    margin: 5px;
}
</style>