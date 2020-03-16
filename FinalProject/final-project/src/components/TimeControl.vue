<template>
  <div class="content-panel">
      <div id="time-control-chart" style="height:100%"></div>
  </div>
</template>

<script>
import 'c3/c3.css';
import * as d3 from 'd3'
import * as c3 from 'c3'

export default {
  name: "TimeControl",
  props: {
    data_confirmed: Array,
    data_deaths: Array,
    data_recovered: Array,
    data_news1: Array,
    data_news2: Array,
    label_news1: String,
    label_news2: String,
  },
  data() {
      return {
          chart: null,
          selected_date: null,
          hover_date: null,
          width: 0,
          height: 0,
          measurements: null,
      }
  },
  computed: {
    dataReady() {
      return (this.data_confirmed != null && this.data_deaths != null && this.data_recovered != null && this.data_news1 != null && this.data_news2 != null)
    }
  },
  watch: {
      dataReady(newVal) {
        if (newVal == true) {
          this.init()
        }
      }
  },
  methods: {
    init() {
      this.preprocessData()

      var self = this

      const x1 = this.getDates(this.getNewsTimestamps(this.data_news1), 'x1', new Date('2020/01/01'))
      const x2 = this.getDates(this.getInfectionTimestamps(this.data_confirmed), 'x2', new Date('2020/01/01'))

      const y_news1 = this.getNewsDataPoints(this.data_news1, this.label_news1, new Date('2020/01/01'))
      const y_news2 = this.getNewsDataPoints(this.data_news2, this.label_news2, new Date('2020/01/01'))

      const y_confirmed = this.getInfectionDataPoints(this.data_confirmed, 'confirmed')
      const y_deaths = this.getInfectionDataPoints(this.data_deaths, 'deaths')
      const y_recovered = this.getInfectionDataPoints(this.data_recovered, 'recovered')


      this.width = document.getElementById('time-control-chart').offsetWidth
      this.height = document.getElementById('time-control-chart').offsetHeight

      this.chart = c3.generate({
          bindto: '#time-control-chart',
          padding: {
            top: 10,
          },
          size: {
            height: this.height,
            //width: this.width,
          },
          data: {
              selection: {
                enabled: true,
                grouped: true,
                multiple: false,
              },
              onselected: (d) => {
                if (this.selected_date == null || d.x.getTime() != this.selected_date.getTime()) {
                  this.selected_date = d.x
                  this.$emit('onselected', d.x)
                }
              },
              onunselected: () => {
                this.selected_date = null
                this.$emit('onunselected')
              },
              color: (color, d) => {
                if (!d.id || (d.id != this.label_news1 && d.id != this.label_news2)) {
                  return color
                }

                let val = -1

                if (d.id == this.label_news1) {
                  val = this.measurements[d.x.getTime()][0].axes[0].value / 2
                }

                if (d.id == this.label_news2) {
                  val = this.measurements[d.x.getTime()][1].axes[0].value / 2
                }

                // console.log(val)

                return d3.interpolateRdBu(val)
              },
              xs: {
                [this.label_news1]: 'x1',
                [this.label_news2]: 'x1',
                confirmed: 'x2',
                deaths: 'x2',
                recovered: 'x2',
              },
              axes: {
                [this.label_news1]: 'y2',
                [this.label_news2]: 'y2',
                confirmed: 'y',
                deaths: 'y',
                recovered: 'y'
              },
              columns: [
                  x1,
                  x2,
                  y_confirmed,
                  y_deaths,
                  y_recovered,
                  y_news1,
                  y_news2,
              ],         
              types: {
                [this.label_news1]: 'bar',
                [this.label_news2]: 'bar',
                confirmed: 'spline',
                deaths: 'spline',
                recovered: 'spline'
              },
              labels: true,
          },
          axis: {
              x: {
                  type: 'timeseries',
                  tick: {
                      rotate: -45,
                      format: '%m-%d'
                  }
              },
              y: {
                min: 0,
                padding: 0,
                tick: {
                  count: 3,
                  format: d3.format('d')
                }
              },
              y2: {
                show: true,
              }
          },
          tooltip: {
            position: function(d) {
              var position = c3.chart.internal.fn.tooltipPosition.apply(this, arguments);

              if (self.hover_date == null || self.hover_date.getTime() != d[0].x.getTime()) {
                self.hover_date = d[0].x
                self.$emit('onhover', d[0].x)
              }

              return position;
            }
          }
      })

      const container = document.getElementById('time-control-chart')
      
      new ResizeObserver(() => {
          this.chart.internal.selectChart.style('max-height', 'none')
          this.height = document.getElementById('time-control-chart').offsetHeight
          setTimeout(() => { this.chart.resize({height: this.height}) }, 100)
      }).observe(container)

      
    },

    getDates(timestamps, label, after) {
      timestamps = Array.from(timestamps)
      timestamps.sort()

      var result = [label]
      for(var timestamp of timestamps) {

        var date = new Date(timestamp)

        if (date.getTime() < after.getTime()) {
          continue
        }

        result.push(date)
      }

      return result
    },

    getNewsTimestamps(data) {
      var timestamps = new Set()

      for(var article of data){
        timestamps.add(new Date(article['time-stamp'].split(',')[0]).getTime())
      }

      return timestamps
    },

    getInfectionTimestamps(data) {
      var timestamps = new Set()
      var entry = data[0]

      // Data starts at 4th col

      var count = 0
      for(var col in entry) {
        if (count < 4) {
          count += 1
          continue
        }
        timestamps.add(new Date(col).getTime())

        count += 1
      }

      return timestamps
    },

    getNewsDataPoints(data, label, after) {
      var timestamps = {}

      for(var article of data) {
        var timestamp = new Date(article['time-stamp'].split(',')[0]).getTime()

        if (timestamp < after.getTime()) {
          continue
        }

        if (typeof timestamps[timestamp] == 'undefined') {
          timestamps[timestamp] = 0
        }

        timestamps[timestamp] += 1
      }

      var sorted = Object.keys(timestamps).sort()
      var result = [label]

      for(var key of sorted) {
        result.push(timestamps[key])
      }

      return result
    },

    getInfectionDataPoints(data, label) {
      var result = [label]

      // Data starts at 4th col

      for(var entry of data) {
        var count = 0
        for(var col in entry) {
          if (count < 4) {
            count += 1
            continue
          }

          if (typeof result[count-3] == 'undefined') {
            result[count-3] = 0
          }

          result[count-3] += parseInt(entry[col])

          count += 1
        }
      }
      
      return result
    },
    preprocessData() {
      this.measurements = {};

      const timestamps = this.getTimestamps();

      for (const timestamp of timestamps) {
        // Create template for data
        this.measurements[timestamp] = [
          {
            group: this.label_news1,
            axes: [
              { axis: "sentiment", value: 0 },
              { axis: "sadness", value: 0 },
              { axis: "joy", value: 0 },
              { axis: "fear", value: 0 },
              { axis: "disgust", value: 0 },
              { axis: "anger", value: 0 }
            ]
          },
          {
            group: this.label_news2,
            axes: [
              { axis: "sentiment", value: 0 },
              { axis: "sadness", value: 0 },
              { axis: "joy", value: 0 },
              { axis: "fear", value: 0 },
              { axis: "disgust", value: 0 },
              { axis: "anger", value: 0 }
            ]
          }
        ];

        // Process dataset1
        var data1_count = 0;
        for (const article of this.data_news1) {
          if (
            timestamp == new Date(article["time-stamp"].split(",")[0]).getTime()
          ) {
              if (typeof article["watson_analysis"] == 'undefined') {
                  continue
              }
            if (isNaN(article["watson_analysis"]["sentiment"])) {
                  continue
              }
            
            data1_count += 1;

            this.measurements[timestamp][0].axes[0].value += 1 +
              article["watson_analysis"]["sentiment"];
            this.measurements[timestamp][0].axes[1].value += 1 +
              article["watson_analysis"]["sadness"];
            this.measurements[timestamp][0].axes[2].value += 1 +
              article["watson_analysis"]["joy"];
            this.measurements[timestamp][0].axes[3].value += 1 +
              article["watson_analysis"]["fear"];
            this.measurements[timestamp][0].axes[4].value += 1 +
              article["watson_analysis"]["disgust"];
            this.measurements[timestamp][0].axes[5].value += 1 +
              article["watson_analysis"]["anger"];
          }
        }
        // normalize
        this.measurements[timestamp][0].axes[0].value /= data1_count;
        this.measurements[timestamp][0].axes[1].value /= data1_count;
        this.measurements[timestamp][0].axes[2].value /= data1_count;
        this.measurements[timestamp][0].axes[3].value /= data1_count;
        this.measurements[timestamp][0].axes[4].value /= data1_count;
        this.measurements[timestamp][0].axes[5].value /= data1_count;

        // Process dataset2
        var data2_count = 0;
        for (const article of this.data_news2) {
          if (
            timestamp == new Date(article["time-stamp"].split(",")[0]).getTime()
          ) {

                // TODO these checks are not necessary with new dataset
                if (typeof article["watson_analysis"] == 'undefined') {
                  continue
              }
              if (isNaN(article["watson_analysis"]["sentiment"])) {
                  continue
              }

            data2_count += 1;

            this.measurements[timestamp][1].axes[0].value += 1 +
              article["watson_analysis"]["sentiment"];
            this.measurements[timestamp][1].axes[1].value += 1 +
              article["watson_analysis"]["sadness"];
            this.measurements[timestamp][1].axes[2].value += 1 +
              article["watson_analysis"]["joy"];
            this.measurements[timestamp][1].axes[3].value += 1 +
              article["watson_analysis"]["fear"];
            this.measurements[timestamp][1].axes[4].value += 1 +
              article["watson_analysis"]["disgust"];
            this.measurements[timestamp][1].axes[5].value += 1 +
              article["watson_analysis"]["anger"];
          }
        }
        // normalize
        this.measurements[timestamp][1].axes[0].value /= data2_count;
        this.measurements[timestamp][1].axes[1].value /= data2_count;
        this.measurements[timestamp][1].axes[2].value /= data2_count;
        this.measurements[timestamp][1].axes[3].value /= data2_count;
        this.measurements[timestamp][1].axes[4].value /= data2_count;
        this.measurements[timestamp][1].axes[5].value /= data2_count;
      }
    },
    getTimestamps() {
      var timestamps = new Set();

      for (const article of this.data_news1) {
        timestamps.add(new Date(article["time-stamp"].split(",")[0]).getTime());
      }
      for (const article of this.data_news2) {
        timestamps.add(new Date(article["time-stamp"].split(",")[0]).getTime());
      }

      timestamps = Array.from(timestamps);
      timestamps.sort();

      return timestamps;
    }
  }
};
</script>

<style>


.c3 .c3-chart-bars path {
  fill-opacity: 0.5;
}
.c3 .c3-axis path, .c3 .c3-axis line {
  stroke: #3f3f3f;
}
.c3 .c3-axis text {
  stroke: #3f3f3f;
  fill: #3f3f3f;
  font-weight: 100;
  font-size: 11px;
}
.c3 .c3-legend-item text {
  stroke: #3f3f3f;
  fill: #3f3f3f;
  font-weight: 100;
  font-size: 11px;
}
.c3 .c3-tooltip {
  color: #3f3f3f;
  font-weight: 100;
  font-size: 11px;
}

 /* .c3-texts .c3-texts-confirmed {
  fill: white;
  fill-opacity: 0;
} */
</style>