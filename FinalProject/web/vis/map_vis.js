class MapVis {
    constructor(data, html_root, dimensions) {
        this.data = data
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        // map settings
        this.accessToken = 'pk.eyJ1IjoibHVrYXNtYXhpbSIsImEiOiJjazcyYXVuZjQwMGNkM21wb2tobDl5cXVuIn0._VW3qQdxkxWyN2vj6vXOvA'
        this.minZoom = 2
        this.maxZoom = 6
        this.centerPoint = [41.9028, 12.4964]
        //this.mapBounds = new L.LatLngBounds([-383, 1], [1, 511]),

        this.init()
    }

    init() {
        var map = L.map(this.html_root).setView(this.centerPoint, this.minZoom)

        L.tileLayer('https://api.mapbox.com/styles/v1/lukasmaxim/ck72h8cr40cts1imo4e0ujcms/tiles/{z}/{x}/{y}?access_token=' + this.accessToken, {
            //attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            minZoom: this.minZoom,
            maxZoom: this.maxZoom,
            //bounds: this.mapBounds,
            //noWrap: true,
            tileSize: 512,
            zoomOffset: -1,
        }).addTo(map)

        L.geoJson(statesData).addTo(map)

    }
}