<template>
    <div id="map-content-panel" class="content-panel">
      <div>
          <div id="map-container"></div>
      </div>
  </div>
</template>

<script>
import MapVis from '../js/vis/map_vis.js'

export default {
    name: 'Map',
    props: {
        data: Array,
        date: Date
    },
    data() {
        return {
            map_vis: null,
            map_vis_dimensions: {
                width: 0,
                height: 0,
                margin: { left: 150, right: 20, top: 20, bottom: 50 }
            },
        }
    },
    computed: {
        dataReady() {
            return (this.data != null && this.date != null)
        }
    },
    mounted() {
        this.init()
    },
    watch: {
        dataReady() {
            this.map_vis.init(this.data, this.date)
        },
        date(newVal) {
            this.update(newVal)
        }
    },
    methods: {
        init() {
            this.map_vis_dimensions.width = document.getElementById('map-content-panel').offsetWidth - 30
            this.map_vis_dimensions.height = document.getElementById('map-content-panel').offsetHeight

            this.map_vis = new MapVis('map-container', this.map_vis_dimensions)
        },
        update(value) {
            if (this.map_vis != null) {
                this.map_vis.update(value)
            }
        },
    },
}
</script>

<style>
    #map-container path {
        stroke-width:0.3px; /* control the countries borders width */
        stroke:#d0d0d0; /* choose a color for the border */
    }
</style>