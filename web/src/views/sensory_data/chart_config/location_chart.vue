<script>

import * as VueGoogleMaps from 'vue2-google-maps';

export default {
    name: "location_chart",

    data() {
        return {
            mapCenter: { lat: 32.7292117  , lng: -97.1151971}, // Default map center (San Francisco)
            mapZoom: 12, // Default map zoom level
            markerPosition: { lat: 32.7292117, lng: -97.1151971 }, // Default marker position (San Francisco)
            markerTitle:"UTA"
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
    }
}
</script>
<template>
    <div>
        <div style="z-index: 1000; width: 500px; height: 500px;">
            <gmap-map ref="mapRef" :center="mapCenter" :zoom="mapZoom" style="height: 400px; width: 100%">
                <gmap-marker :position="markerPosition" :label="markerTitle"></gmap-marker>
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
</style>