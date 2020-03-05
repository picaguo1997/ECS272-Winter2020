import { GoogleCharts } from 'google-charts';
import name_iso_lookup from '../util/name_iso_lookup'
import * as d3 from 'd3'

class MapVis {
    constructor(html_root, dimensions) {
        this.data = null
        this.html_root = html_root
        this.dimensions = dimensions


        this.preprocessed_data = {}
        this.filtered_data = [['Country', 'Log_Cases']]
        
        this.chart = null

        // TODO: minValue, maxValue are hardcoded
        this.map_options = {
            colorAxis: {minValue: 0, maxValue: 11, colors: ['#fff', 'rgb(31, 119, 180)']},
            backgroundColor: 'transparent',
            datalessRegionColor: 'transparent',
            legend: 'none',
            width: dimensions.width,
            height: dimensions.height
        }

        this.ready = false

        // setup the map
        GoogleCharts.load(() => {
            this.draw_map()
        }, {
            'packages': ['geochart'],
            'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
        })
    }

    init(data, date) {
        this.data = data
        this.preprocess_data()
        this.filtered_data = this.filter_data(date)
        this.ready = true
    }

    update(date) {
        if (!this.ready) {
            return
        }

        this.filtered_data = this.filter_data(date)

        this.draw_map()
    }

    filter_data(timestamp) {
        if (typeof this.preprocessed_data[timestamp] == 'undefined') {
            return this.filtered_data
        }

        return this.preprocessed_data[timestamp]
    }

    preprocess_data() {
        this.preprocessed_data = {}
        var entry = this.data[0]

        // Data starts at 4th col

        var count = 0
        for(var col in entry) {
            if (count < 4) {
                count += 1
                continue
            }
            this.preprocessed_data[new Date(col)] = []

            count += 1
        }

        for(var date in this.preprocessed_data) {
            // group incidents in countries at a specific date
            var date_data = d3.nest()
                .key(d => { return d['Country/Region'] })
                .rollup(row => {
                    return d3.sum(row, d => {
                        const dt = new Date(date)
                        const col_name = (dt.getMonth()+1) + '/' + dt.getDate() + '/' + dt.getFullYear().toString().substr(-2)

                        return d[col_name]
                    })
                })
                .entries(this.data)

                var date_data_array = [['Country', 'Log_Cases']]
                // add data country names' ISO codes, calculate the logged value
                date_data.forEach(row => {
                    var id = name_iso_lookup[row.key]
                    //row.cases = row.value
                    var logged_cases = Math.log(1 + row.value)
                    
                    logged_cases > 0 ? date_data_array.push([id, logged_cases]) : null
                });

                this.preprocessed_data[date] = date_data_array
        }

        //######################################################

        /*

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

            date_data_array.push(['Country', 'Log_Cases', ])

            // add data country names' ISO codes, calculate the logged value
            date_data.forEach(row => {
                var id = name_iso_lookup[row.key]
                //row.cases = row.value
                var logged_cases = Math.log(1 + row.value)
                
                logged_cases > 0 ? date_data_array.push([id, logged_cases]) : null
            });

            this.preprocessed_data.push(date_data_array)
        })

        */
    }

    draw_map() {
        var table_data = GoogleCharts.api.visualization.arrayToDataTable(this.filtered_data)



        if (this.chart == null) {
            this.chart = new GoogleCharts.api.visualization.GeoChart(document.getElementById(this.html_root))
        }

        this.chart.draw(table_data, this.map_options)
    }
}

export default MapVis