<template>
  <div id="app">
    <StatusBar title="COVID-19 News & Spread"/>
    <div class="main-content">
      <Map :data="covid_confirmed" :date="hover_date" style="grid-area: map"/>
      <!--
      <TwitterFeed :data="twitter" :date="date" style="grid-area: side1"/>
      <NewsFeed :data="news" :date="date" style="grid-area: side2"/>
      -->
      <!--<WordCloud :data="null" style="grid-area: cloud"/>-->
      <TimeControl 
      :data_confirmed="covid_confirmed" 
      :data_deaths="covid_deaths" 
      :data_recovered="covid_recovered"
      :data_news="news"
      @onselected="(date) => { this.selected_date = date }"
      @onhover="(date) => { this.hover_date = date }"
      style="grid-area: control"/>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'

import StatusBar from './components/StatusBar.vue'
//import WordCloud from './components/WordCloud.vue'
import Map from './components/Map.vue'
import TimeControl from './components/TimeControl.vue'
//import TwitterFeed from './components/TwitterFeed.vue'
//import NewsFeed from './components/NewsFeed.vue'

export default {
  name: 'App',
  components: {
    StatusBar,
    //WordCloud,
    Map,
    TimeControl,
    //TwitterFeed,
    //NewsFeed
  },
  data() {
    return {
      selected_date: null,
      hover_date: null,
      twitter: null,
      news: null,
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
    this.selected_date = null
    this.hover_date = null

    d3.json('/data/twitter.json')
      .then((data) => {
        this.twitter = data.tweets
      })

    d3.json('/data/news.json')
      .then((data) => {
        this.news = data
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

.main-content {
  display: grid;
  grid-template-columns: 0fr 1.5fr 1.5fr 0.75fr 0fr;
  grid-template-rows: 0 0 95vh;
  grid-template-areas: 
  ". main main . ."
  ". main main cloud ."
  ". control control map .";
  grid-column-gap: 10px;
  grid-row-gap: 15px;
  padding: 0px 0 0 0;
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
