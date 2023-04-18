<script>
import * as VueGoogleMaps from 'vue2-google-maps';
import * as echarts from 'echarts'
import { request } from '@/api/service'

export default {
    name: "location_chart",


    data() {
        return {
            mapCenter: { lat: 32.7292117, lng: -97.1151971 }, // Default map center (San Francisco)
            mapZoom: 12, // Default map zoom level
            markers: [{ position: { lat: 32.7292117, lng: -97.1151971 }, title: "UTA" }, { position: { lat: 32.8140177, lng: -96.9488945 }, title: "IRVING" }], // Default marker position (San Francisco)
            markerTitle: "UTA"
        };
    },
    mounted() {
        this.$refs.mapRef.$mapPromise.then((map) => {
            map.panTo({ lat: this.mapCenter.lat, lng: this.mapCenter.lng })
        })
        this.loadCharts();
    }
    , components: {
        GmapMap: VueGoogleMaps.Map,
        GmapMarker: VueGoogleMaps.Marker,
    }, methods: {
        onMarkerClick(marker) {
            alert(`Marker ${marker.title} clicked`);
            var parentDiv = document.getElementById("right");
            parentDiv.innerHTML = "";
            this.loadCharts();
        },
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
                    childDiv.style.width = "700px";
                    childDiv.style.height = "400px";

                    // Get the parent div element by id "parent"
                    var parentDiv = document.getElementById("right");

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
        <div class="left">
            <gmap-map ref="mapRef" :center="mapCenter" :zoom="mapZoom" style="height: 400px; width: 100%">
                <gmap-marker v-for="(marker, index) in markers" :key="index" :position="marker.position"
                    :label="marker.title" @click="onMarkerClick(marker)"></gmap-marker>
            </gmap-map>

            <div class="inside-left">
                <!-- content goes here -->
                <h3>Marker Description</h3>
                <br>
                <div v-for="(marker, index) in markers" :key="index">
                    <h4>Title : {{ marker.title }}</h4>

                </div>

            </div>
        </div>
        <div class="right-div" id="right">



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

.left {
    display: inline-block;
    width: 40%;
    vertical-align: top;
}

.right-div {
    background-color: white;
    display: inline-block;
    width: 60%;
    overflow-y: scroll; /* Add this line to make it scrollable */
    height: 100vh;
    vertical-align: top;
    padding-bottom: 200px;
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