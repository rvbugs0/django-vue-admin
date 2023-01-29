<template>
    <div class="container" style="background-color: white;min-width: 100%;min-height: 100%;">

        <div id="chart1Container"></div>
        <div id="chart3Container"></div>
        <div id="chart4Container"></div>
        <div id="chart2Container"></div>

    </div>




</template>
  
<script>
import * as echarts from '../static/echarts.min'
const urlPrefix = '/api/system/sensory_data/'
import { request } from '@/api/service'
import { copyFileSync } from 'fs'
export default {
    name: 'sensory_charts',
    data() {
        return {
            chart1results: [],
            chart2results: []

        }

    },
    methods: {

    }, mounted() {
        var address = this;

        // chart-1
        var chart1Container = document.getElementById('chart1Container');
        var chart1 = echarts.init(chart1Container, null, {
            renderer: 'canvas',
            useDirtyRect: false
        });
        this.chart1option = {
            title: {
                text: 'Month vs Average Sea water Temp. (deg. C)',
                left: 'center'
            },
            xAxis: {
                type: 'category',
                data: []
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [],
                    type: 'line'
                }
            ]
        };
        this.chart1results = []
        request({ url: urlPrefix + 'get_average_temperatures/', method: 'get', }).then(function (finalRes) {

            address.chart1results = finalRes;

            for (var i in finalRes) {
                address.chart1option.xAxis.data.push(finalRes[i].month);

                address.chart1option.series[0].data.push(finalRes[i].average_temp);
            }
            if (address.chart1option && typeof address.chart1option === 'object') {
                chart1.setOption(address.chart1option);
            }


        });


        // chart-2
        var chart2Container = document.getElementById('chart2Container');
        var chart2 = echarts.init(chart2Container);
        this.chart2option = {
            title: {
                text: 'Month vs Average Salinity',
                left: 'center'
            },
            dataset: [
                {
                    dimensions: ['month', 'salinity', 'index'],
                    source: [
                    ]
                },
                {
                    transform: {
                        type: 'sort',
                        config: { dimension: 'index', order: 'asc' }
                    }
                }
            ],
            xAxis: {
                type: 'category',
                axisLabel: { interval: 0, rotate: 30 }
            },
            yAxis: {},
            series: {
                type: 'bar',
                encode: { x: 'month', y: 'salinity' },
                datasetIndex: 1
            }
        };
        this.chart2results = []
        request({ url: urlPrefix + 'get_average_salinity/', method: 'get', }).then(function (finalRes) {


            for (var i in finalRes) {
                address.chart2option.dataset[0].source.push([finalRes[i].month, finalRes[i].average_salinity, i]);

            }
            address.chart2results = address.chart2option.dataset[0].source;
            if (address.chart2option && typeof address.chart2option === 'object') {

                chart2.setOption(address.chart2option);
            }
            // console.log(address.chart2results);
            // console.log(address.chart2option.dataset[0].source);


        });


        // chart-3  
        var chart3Container = document.getElementById('chart3Container');
        var chart3 = echarts.init(chart3Container);
        let base = +new Date(1968, 9, 3);
        let oneDay = 24 * 3600 * 1000;
        let date = [];
        let chart3data = [];
        this.chart3option = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            title: {
                left: 'center',
                text: 'Date v. Salinity'
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: date
            },
            yAxis: {
                type: 'value',
                boundaryGap: [0, '100%']
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 0,
                    end: 10
                },
                {
                    start: 0,
                    end: 10
                }
            ],
            series: [
                {
                    name: 'Salinity',
                    type: 'line',
                    symbol: 'none',
                    sampling: 'lttb',
                    itemStyle: {
                        color: 'rgb(255, 70, 131)'
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {
                                offset: 0,
                                color: 'rgb(255, 158, 68)'
                            },
                            {
                                offset: 1,
                                color: 'rgb(255, 70, 131)'
                            }
                        ])
                    },
                    data: chart3data
                }
            ]
        };

        this.chart3results = []
        request({ url: urlPrefix + '', method: 'get', }).then(function (finalRes) {

            finalRes = finalRes.data.data;
            address.chart3results = finalRes;

            for (var i in finalRes) {
                
                chart3data.push(finalRes[i].salinity);
                
                date.push(finalRes[i].date_recorded);

            }
            if (address.chart3option && typeof address.chart3option === 'object') {

                chart3.setOption(address.chart3option);
            }


        });


        // chart-4
        var chart4Container = document.getElementById('chart4Container');
        var chart4 = echarts.init(chart4Container);

        this.chart4option = {            
            title: {
                left: 'center',
                text: 'Month v. Average pH'
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: []
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [],
                    type: 'line',
                    areaStyle: {}
                }
            ]
        };
        this.chart4results = []
        request({ url: urlPrefix + 'get_average_ph/', method: 'get', }).then(function (finalRes) {

            address.chart4results = finalRes;

            for (var i in finalRes) {
                address.chart4option.xAxis.data.push(finalRes[i].month);

                address.chart4option.series[0].data.push(finalRes[i].average_ph);
            }
            if (address.chart4option && typeof address.chart4option === 'object') {
                chart4.setOption(address.chart4option);
            }


        });





        window.addEventListener('resize', chart1.resize);
        window.addEventListener('resize', chart2.resize);
        window.addEventListener('resize', chart3.resize);
        window.addEventListener('resize', chart4.resize);
    }

}



</script>

<style scoped>
* {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}

html,
body {
    height: 100%;
    width: 100%;
}

div {
    width: 50%;
    height: 50%;
    float: left;
}

div:nth-of-type(1) {
    padding-top: 10px;
    background: #fff;
}

div:nth-of-type(2) {
    background: #fff;
    border-left: 1px solid #f00;
}

div:nth-of-type(3) {
    padding-top: 10px;
    background: #fff;
    border-top: 1px solid #f00;
}

div:nth-of-type(4) {
    padding-top: 10px;
    background: #fff;
    border-top: 1px solid #f00;
    border-left: 1px solid #f00;
}
</style>

