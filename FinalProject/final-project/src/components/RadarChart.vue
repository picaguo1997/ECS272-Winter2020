<template>
  <div class="content-panel">

    <div id="radar-chart-container-container">
      <div id="padding-container"/>
      <div id="radar-chart-container"/>
    </div>

  </div>
</template>

<script>
import RadarChart from "../js/vis/radar-chart.js";

export default {
  name: "RadarChart",
  props: {
    data1: Array,
    data2: Array,
    label1: String,
    label2: String,
    date: Date
  },
  data() {
    return {
      chart: null,
      chart_data: null,
      chart_ready: false,
      width: 0,
      height: 0
    };
  },
  computed: {
    dataReady() {
      return this.data1 != null && this.data2 != null;
    }
  },
  watch: {
    date(newVal) {
      if (newVal != null && this.chart_ready) {
        if (typeof this.chart_data[newVal.getTime()] != 'undefined') {
            this.init()
        }
      }
    },
    dataReady() {
      this.preprocessData();

      this.chart_ready = true
    }
  },
  methods: {
    init() {
      this.width = document.getElementById("radar-chart-container-container").offsetWidth;
      this.height = document.getElementById(
        "radar-chart-container-container"
      ).offsetHeight;

      const data = this.chart_data[this.date.getTime()]

      const options = {
        w: this.width / 2,
        h: this.width / 2,
        maxValue: 2,
        facet: false,
        levels: 4,
        levelScale: 0.85,
        labelScale: 0.9,
        facetPaddingScale: 2.1,
        showLevels: true,
        showLevelsLabels: true,
        showAxesLabels: true,
        showAxes: true,
        showLegend: true,
        showVertices: true,
        showPolygons: true
      };

      RadarChart.draw("#radar-chart-container", data, options);

      // set the height of the padding container so the svg is vertically centered
      var svg_height = document.getElementsByClassName('svg-vis')[0].getClientRects()[0].height
      document.getElementById("padding-container").style.height = ((this.height - svg_height) / 2) + 'px';
    },
    preprocessData() {
      this.chart_data = {};

      const timestamps = this.getTimestamps();

      for (const timestamp of timestamps) {
        // Create template for data
        this.chart_data[timestamp] = [
          {
            group: this.label1,
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
            group: this.label2,
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
        for (const article of this.data1) {
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

            this.chart_data[timestamp][0].axes[0].value += 1 +
              article["watson_analysis"]["sentiment"];
            this.chart_data[timestamp][0].axes[1].value += 1 +
              article["watson_analysis"]["sadness"];
            this.chart_data[timestamp][0].axes[2].value += 1 +
              article["watson_analysis"]["joy"];
            this.chart_data[timestamp][0].axes[3].value += 1 +
              article["watson_analysis"]["fear"];
            this.chart_data[timestamp][0].axes[4].value += 1 +
              article["watson_analysis"]["disgust"];
            this.chart_data[timestamp][0].axes[5].value += 1 +
              article["watson_analysis"]["anger"];
          }
        }
        // normalize
        this.chart_data[timestamp][0].axes[0].value /= data1_count;
        this.chart_data[timestamp][0].axes[1].value /= data1_count;
        this.chart_data[timestamp][0].axes[2].value /= data1_count;
        this.chart_data[timestamp][0].axes[3].value /= data1_count;
        this.chart_data[timestamp][0].axes[4].value /= data1_count;
        this.chart_data[timestamp][0].axes[5].value /= data1_count;

        // Process dataset2
        var data2_count = 0;
        for (const article of this.data2) {
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

            this.chart_data[timestamp][1].axes[0].value += 1 +
              article["watson_analysis"]["sentiment"];
            this.chart_data[timestamp][1].axes[1].value += 1 +
              article["watson_analysis"]["sadness"];
            this.chart_data[timestamp][1].axes[2].value += 1 +
              article["watson_analysis"]["joy"];
            this.chart_data[timestamp][1].axes[3].value += 1 +
              article["watson_analysis"]["fear"];
            this.chart_data[timestamp][1].axes[4].value += 1 +
              article["watson_analysis"]["disgust"];
            this.chart_data[timestamp][1].axes[5].value += 1 +
              article["watson_analysis"]["anger"];
          }
        }
        // normalize
        this.chart_data[timestamp][1].axes[0].value /= data2_count;
        this.chart_data[timestamp][1].axes[1].value /= data2_count;
        this.chart_data[timestamp][1].axes[2].value /= data2_count;
        this.chart_data[timestamp][1].axes[3].value /= data2_count;
        this.chart_data[timestamp][1].axes[4].value /= data2_count;
        this.chart_data[timestamp][1].axes[5].value /= data2_count;
      }
    },
    getTimestamps() {
      var timestamps = new Set();

      for (const article of this.data1) {
        timestamps.add(new Date(article["time-stamp"].split(",")[0]).getTime());
      }
      for (const article of this.data2) {
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
.svg-vis {

}
.verticesTooltip {
  
}
.level-lines {
  stroke: #979797;
  stroke-width: 1px;
}
.level-labels {
  fill: #484848;
  font-size: 8px;
}
.axis-lines {
  stroke: #979797;
  stroke-width: 1px;
}
.axis-labels {
  fill: #484848;
  font-weight: 700;
  font-size: 12px;
}
.polygon-vertices {
  fill-opacity: 0;
}
.polygon-areas {
  fill-opacity: 0;
}
.legend-tiles {
  fill-opacity: 1;
}
.legend-labels {
  font-size: 12px;
  fill: #000;
}
#radar-chart-container-container {
  height:100%;
  width:100%;
}
</style>