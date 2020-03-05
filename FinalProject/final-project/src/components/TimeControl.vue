<template>
  <div class="content-panel">
      <div id="time-control-chart" style="height:100%"></div>
  </div>
</template>

<script>
import 'c3/c3.css';
//import * as d3 from 'd3'
import * as c3 from 'c3'

export default {
  name: "TimeControl",
  props: {
    data_confirmed: Array,
    data_deaths: Array,
    data_recovered: Array,
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
      return (this.data_confirmed != null && this.data_deaths != null && this.data_recovered != null)
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

      const x = this.getTimePoints(this.data_confirmed, 'x')
      const y_confirmed = this.getDataPoints(this.data_confirmed, 'confirmed')
      const y_deaths = this.getDataPoints(this.data_deaths, 'deaths')
      const y_recovered = this.getDataPoints(this.data_recovered, 'recovered')


      this.width = document.getElementById('time-control-chart').offsetWidth
      this.height = document.getElementById('time-control-chart').offsetHeight

      this.chart = c3.generate({
          bindto: '#time-control-chart',
          padding: {
            top: 10
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
              x: 'x',
              columns: [
                  x,
                  y_confirmed,
                  y_deaths,
                  y_recovered,
              ],
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
                  count: 3
                }
              }
          },
          tooltip: {
            position: function(d) {
              var position = c3.chart.internal.fn.tooltipPosition.apply(this, arguments);

              self.$emit('onhover', d[0].x)
              return position;
            }
          }
      })
    },

    getTimePoints(data, label) {
      var result = [label]
      var entry = data[0]

      // Data starts at 4th col

      var count = 0
      for(var col in entry) {
        if (count < 4) {
          count += 1
          continue
        }
        result.push(new Date(col))

        count += 1
      }

      return result
    },

    getDataPoints(data, label) {
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