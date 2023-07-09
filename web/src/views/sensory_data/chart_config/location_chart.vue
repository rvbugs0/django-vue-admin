<script>
import * as VueGoogleMaps from 'vue2-google-maps';
//  key in src/main.js
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
        
    }
    , components: {
        GmapMap: VueGoogleMaps.Map,
        GmapMarker: VueGoogleMaps.Marker,
    }, methods: {
        onMarkerClick(marker) {
            alert(`Marker ${marker.title} clicked`);
            window.open(`/location_chart_detailed/#/location_chart_detailed`, '_blank');

        },
        
    }
}



</script>
<template>
    <div class="contain">
        <div class="left">
            <gmap-map ref="mapRef" :center="mapCenter" :zoom="mapZoom" style="height: 700px; width: 100%">
                <gmap-marker v-for="(marker, index) in markers" :key="index" :position="marker.position"
                    :label="marker.title" @click="onMarkerClick(marker)"></gmap-marker>
            </gmap-map>


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
    width: 100%;
    vertical-align: top;
}

.right-div {
    background-color: white;
    display: inline-block;
    width: 60%;
    overflow-y: scroll;
    /* Add this line to make it scrollable */
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