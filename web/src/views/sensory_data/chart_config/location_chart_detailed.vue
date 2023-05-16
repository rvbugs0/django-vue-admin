<script>
import * as VueGoogleMaps from 'vue2-google-maps';
import * as echarts from 'echarts'
import { request } from '@/api/service'

export default {
    name: "location_chart_detailed",


    data() {
        return {
        
        };
    },
    mounted() {
        
        this.loadCharts();
    }
    , components: {
        
    }, methods: {
        
        loadCharts() {
            var entities = ["sea_water_temperature_c", "ph", "dissolved_oxygen", "salinity"]
            for (var i = 0; i < entities.length; i++) {

                var promise = request({
                    url: '/api/system/chart_config/get_plain_scroll_charts/',
                    method: 'get',
                    params: { entity: entities[i] }
                });

                promise.then(function (data) {
                    
                    var element = data[0];
                    
                    var option = {
                        tooltip: {
                            trigger: 'axis',
                            position: function (pt) {
                                return [pt[0], '1%'];
                            }
                        },
                        title: {
                            left: 'center',
                            text: element.title
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
                            data: element.xData
                        },
                        yAxis: {
                            type: 'value',
                            boundaryGap: [0, '1%']
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
                                name: 'Y-value',
                                type: 'line',
                                symbol: 'none',
                                sampling: 'lttb',
                                itemStyle: {
                                    color: 'rgb(255, 70, 131)'
                                },

                                data: element.yData
                            }
                        ]
                    };
                    // Create a div element with id "child"
                    var childDiv = document.createElement("div");
                    childDiv.id = "chart_" + i;
                    childDiv.style.width = "900px";
                    childDiv.style.height = "500px";

                    // Get the parent div element by id "parent"
                    var parentDiv = document.getElementById("charts_container");

                    // Append the child div element as a child of the parent div element
                    parentDiv.appendChild(childDiv);

                    let myChart = echarts.init(childDiv)
                    myChart.setOption(option)
                })

            }


        }
    }
}



</script>
<template>
    <div class="contain">
        
        <div class="charts_container" id="charts_container">



        </div>
    </div>
</template>


<style lang="scss">
.yxtInput {
    .el-form-item__label {
        color: #49a1ff;
    }
}

.contain {
    width: 100%;
}


.charts_container {
    background-color: white;
    display: inline-block;
    width: 100%;
    overflow-y: scroll; /* Add this line to make it scrollable */
    height: 100vh;
    vertical-align: top;
    
    padding-top: 50px;
}

.inside-left {
    padding-left: 30px;
    padding-top: 10px;
    height: 100vh;
    background-color: white;
    /* styles for the inner div go here */
}
</style>