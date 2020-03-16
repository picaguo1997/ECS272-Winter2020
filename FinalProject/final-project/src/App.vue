<template>
  <div id="app">
    
    <!-- <StatusBar title="COVID-19 News & Spread"/> -->
    <div id="main" class="main-content main-content-collapsed">
        <RadarChart style="grid-area: radar" 
        :data1="news_us"
        :data2="news_china"
        label1="US"
        label2="China"
        :date="selected_date"
        />
      <Map :data="covid_confirmed" :date="hover_date" style="grid-area: map"/>
      <!--
      <TwitterFeed :data="twitter" :date="date" style="grid-area: side1"/>
      -->
      <!-- TODO only shows US news -->
      <NewsFeed id='side-area' :data="news_us" :date="hover_date" style="grid-area: side; display: none"/>
      <RegionDetail style="grid-area: us"/>
      <RegionDetail style="grid-area: cn"/>
      <!--<WordCloud :data="null" style="grid-area: cloud"/>-->
      <TimeControl 
      :data_confirmed="covid_confirmed" 
      :data_deaths="covid_deaths" 
      :data_recovered="covid_recovered"
      :data_news1="news_us"
      :data_news2="news_china"
      label_news1="US News"
      label_news2="Chinese News"
      @onselected="onTimeControlDateSelected"
      @onunselected="onTimeControlDateUnSelected"
      @onhover="(date) => { this.hover_date = date }"
      style="grid-area: control"/>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'

// import StatusBar from './components/StatusBar.vue'
//import WordCloud from './components/WordCloud.vue'
import Map from './components/Map.vue'
import TimeControl from './components/TimeControl.vue'
//import TwitterFeed from './components/TwitterFeed.vue'
import NewsFeed from './components/NewsFeed.vue'
import RadarChart from './components/RadarChart.vue'
import RegionDetail from './components/RegionDetail.vue'

export default {
  name: 'App',
  components: {
    // StatusBar,
    //WordCloud,
    Map,
    TimeControl,
    RegionDetail,
    //TwitterFeed,
    NewsFeed,
    RadarChart
  },
  data() {
    return {
      selected_date: null,
      hover_date: null,
      twitter: null,
      news_us: null,
      news_china: null,
      covid_confirmed: null,
      covid_deaths: null,
      covid_recovered: null,
    }
  },
  watch: {
    date() {
      console.log(this.date)
    }
  },
  created() {
    //TODO DEBUG ONLY
    setTimeout(() => (this.selected_date = new Date()), 1500)

    this.selected_date = null
    this.hover_date = null

    d3.json('/data/twitter.json')
      .then((data) => {
        this.twitter = data.tweets
      })

    d3.json('/data/news_us.json')
      .then((data) => {
        this.news_us = data
      })

    d3.json('/data/news_china.json')
      .then((data) => {
        this.news_china = data
      })

    d3.csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
      .then((data) => {
        this.covid_confirmed = data
      })
    d3.csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
      .then((data) => {
        this.covid_deaths = data
      })
    d3.csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
      .then((data) => {
        this.covid_recovered = data
      })
  },
  methods: {
    onTimeControlDateSelected(date) {
      this.selected_date = date
      document.getElementById('main').classList.add('main-content-collapsed')
      document.getElementById('side-area').style.display = 'none'
      document.getElementById('main-area').style.display = 'block'
    },
    onTimeControlDateUnSelected() {
      document.getElementById('main').classList.remove('main-content-collapsed')
      document.getElementById('side-area').style.display = 'block'
      document.getElementById('main-area').style.display = 'none'
    }
  }
}
</script>

<style>
body {
  background-color: #05192B;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #FFF;
  margin-top: 0px;
}

h1 {
  font-size: 2em;
}

h2 {
  font-size: 1.5em;
}

h3 {
  font-size: 1.2em;
}

#main {
  transition: all 2s linear;
  -webkit-transition: all 2s linear;
  -moz-transition: all 2s linear;
}

.main-content {
  display: grid;
  grid-template-columns: 0fr 1.5fr 1.5fr 600px 0fr;
  grid-template-rows: 60vh 34vh;
  grid-template-areas: 
  ". control control side ."
  ". control control map .";
  grid-column-gap: 10px;
  grid-row-gap: 15px;
  padding: 0px 0 0 0;
}

.main-content-collapsed {
  grid-template-areas: 
  ". radar us us ."
  ". radar cn cn ."
  ". control control map .";
  grid-template-rows: 30vh 30vh 34vh;
}

.content-panel {
  display: inline-block;
  padding: 10px;
  background-color: #242A3D;
  border-radius: 4px;
  -webkit-box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
}

</style>
