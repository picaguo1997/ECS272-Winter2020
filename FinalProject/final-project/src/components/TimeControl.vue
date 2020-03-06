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
    data_news: Array,
  },
  data() {
      return {
          chart: null,
          selected_date: null,
          hover_date: null
      }
  },
  computed: {
    dataReady() {
      return (this.data_confirmed != null && this.data_deaths != null && this.data_recovered != null && this.data_news != null)
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
      var self = this

      const x1 = this.getDates(this.getNewsTimestamps(this.data_news), 'x1', new Date('2020/01/01'))
      const x2 = this.getDates(this.getInfectionTimestamps(this.data_confirmed), 'x2', new Date('2020/01/01'))

      const y_news = this.getNewsDataPoints(this.data_news, 'news', new Date('2020/01/01'))
      console.log(y_news)

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
            width: this.width,
          },
          data: {
              selection: {
                enabled: true,
                grouped: true,
                multiple: false,
              },
              onselected: (d) => {
                if (d.x != this.selected_date) {
                  this.$emit('onselected', d.x)
                }
              },
              xs: {
                news: 'x1',
                confirmed: 'x2',
                deaths: 'x2',
                recovered: 'x2',
              },
              axes: {
                news: 'y2',
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
                  y_news
              ],         
              types: {
                news: 'bar',
                confirmed: 'spline',
                deaths: 'spline',
                recovered: 'spline'
              },
          },
          axis: {
              x: {
                  type: 'timeseries',
                  tick: {
                      format: '%Y-%m-%d'
                  }
              },
              y: {
                min: 0,
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

      console.log(label)

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
  }
};
</script>

<style>
.c3 .c3-chart-bars path {
  fill-opacity: 0.5;
}
.c3 .c3-axis path, .c3 .c3-axis line {
  stroke: #fff;
}
.c3 .c3-axis text {
  stroke: #fff;
  fill: #fff;
  font-weight: 100;
  font-size: 11px;
}
.c3 .c3-legend-item text {
  stroke: #fff;
  fill: #fff;
  font-weight: 100;
  font-size: 11px;
}
.c3 .c3-tooltip {
  color: #333;
  font-weight: 100;
  font-size: 11px;
}
</style>