<template>
        <div class="container" style="padding-top:32px;background-color: white;min-width: 100%;min-height: 100%;">
            <div id="container" style="height: 320px; width: 480px;"></div>
        </div>



</template>
  
<script>
import * as echarts from '../static/echarts.min'
const urlPrefix = '/api/system/weatherinfo/'
import { request } from '@/api/service'
export default {
    name: 'chartview',
    data() {
        return {
            results: []
        }

    },
    methods: {

    }, mounted() {

        var dom = document.getElementById('container');
        var myChart = echarts.init(dom, null, {
            renderer: 'canvas',
            useDirtyRect: false
        });

        this.option = {
            title: {
                text: 'Month vs Average Temperature in Degree Celcius',
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

        this.results = []
        var address = this;
        request({ url: urlPrefix + 'get_average_temperatures/', method: 'get', }).then(function (finalRes) {

            address.results = finalRes;

            for (var i in finalRes) {
                address.option.xAxis.data.push(finalRes[i].month);

                address.option.series[0].data.push(finalRes[i].average_temp);
            }
            if (address.option && typeof address.option === 'object') {
                myChart.setOption(address.option);
            }


        });

        window.addEventListener('resize', myChart.resize);
    }

}



</script>


