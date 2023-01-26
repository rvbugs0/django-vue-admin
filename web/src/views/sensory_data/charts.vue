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
        var chart2 = echarts.init(chart2Container, null, {
            renderer: 'canvas',
            useDirtyRect: false
        });
        this.chart2option = {
            xAxis: {},
            yAxis: {},
            series: [
                {
                    symbolSize: 20,
                    data: [
                        [10.0, 8.04],
                        [8.07, 6.95],
                        [13.0, 7.58],
                        [9.05, 8.81],
                        [11.0, 8.33],
                        [14.0, 7.66],
                        [13.4, 6.81],
                        [10.0, 6.33],
                        [14.0, 8.96],
                        [12.5, 6.82],
                        [9.15, 7.2],
                        [11.5, 7.2],
                        [3.03, 4.23],
                        [12.2, 7.83],
                        [2.02, 4.47],
                        [1.05, 3.33],
                        [4.05, 4.96],
                        [6.03, 7.24],
                        [12.0, 6.26],
                        [12.0, 8.84],
                        [7.08, 5.82],
                        [5.02, 5.68]
                    ],
                    type: 'scatter'
                }
            ]
        };

        if (address.chart2option && typeof address.chart2option === 'object') {
            chart2.setOption(address.chart2option);
        }


        // chart-3
        var chart3Container = document.getElementById('chart3Container');
        var chart3 = echarts.init(chart3Container);
        let base = +new Date(1968, 9, 3);
        let oneDay = 24 * 3600 * 1000;
        let date = [];
        let data = [Math.random() * 300];
        for (let i = 1; i < 20000; i++) {
            var now = new Date((base += oneDay));
            date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
            data.push(Math.round((Math.random() - 0.5) * 20 + data[i - 1]));
        }
        this.chart3option = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            title: {
                left: 'center',
                text: 'Large Area Chart'
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
                    name: 'Fake Data',
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
                    data: data
                }
            ]
        };

        if (address.chart3option && typeof address.chart3option === 'object') {
            chart3.setOption(address.chart3option);
        }


        // chart-4
        var chart4Container = document.getElementById('chart4Container');
        var chart4 = echarts.init(chart4Container);
        
        this.chart4option = {
  angleAxis: {},
  radiusAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu'],
    z: 10
  },
  polar: {},
  series: [
    {
      type: 'bar',
      data: [1, 2, 3, 4],
      coordinateSystem: 'polar',
      name: 'A',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    },
    {
      type: 'bar',
      data: [2, 4, 6, 8],
      coordinateSystem: 'polar',
      name: 'B',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    },
    {
      type: 'bar',
      data: [1, 2, 3, 4],
      coordinateSystem: 'polar',
      name: 'C',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    }
  ],
  legend: {
    show: true,
    data: ['A', 'B', 'C']
  }
};
        if (address.chart4option && typeof address.chart4option === 'object') {
            chart4.setOption(address.chart4option);
        }




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
    padding-top: 20px;
    background: #fff;
}

div:nth-of-type(2) {
    background: #fff;
    border-left: 1px solid #f00;
}

div:nth-of-type(3) {
    background: #fff;
    border-top: 1px solid #f00;
}

div:nth-of-type(4) {
    background: #fff;
    border-top: 1px solid #f00;
    border-left: 1px solid #f00;
}
</style>
