import { GoogleCharts } from 'google-charts';
import name_iso_lookup from '../util/name_iso_lookup'
import getDates from '../util/utils'
import * as d3 from 'd3'

class PerformantMapVis {
    constructor(data, html_root, dimensions) {
        this.data = data
        this.html_root = html_root
        this.dimensions = dimensions

        this.preprocessed_data = []

        this.start_date = '1/22/20'
        this.end_date = '2/24/20'

        this.init()
    }

    init() {
        this.preprocess_data()
        const filtered_data = this.filter_data(0)

        // setup the map
        GoogleCharts.load(this.draw_map(filtered_data, this.html_root), {
            'packages': ['geochart'],
            'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
        })
    }

    filter_data(timestamp) {
        return this.preprocessed_data[timestamp]
    }

    preprocess_data() {
        // get all the dates in the dataset
        var dates = getDates(this.start_date, this.end_date)

        // for each date, create an array entry
        dates.forEach(date => {

            // group incidents in countries at a specific date
            var date_data = d3.nest()
                .key(d => { return d['Country/Region'] })
                .rollup(row => {
                    return d3.sum(row, d => {
                        return d[date]
                    })
                })
                .entries(this.data)

            var date_data_array = []

            date_data_array.push(['Country', 'Log_Cases'])

            // add data country names' ISO codes, calculate the logged value
            date_data.forEach(row => {
                var id = name_iso_lookup[row.key]
                //row.cases = row.value
                var logged_cases = Math.log(1 + row.value)

                date_data_array.push([id, logged_cases])
            });

            this.preprocessed_data.push(date_data_array)
        })
    }

    draw_map(data, html_root) {
        return function () {
            var table_data = GoogleCharts.api.visualization.arrayToDataTable(data)
            var options = {}

            var chart = new GoogleCharts.api.visualization.GeoChart(document.getElementById(html_root))

            chart.draw(table_data, options)
        }
    }
}

export default PerformantMapVis