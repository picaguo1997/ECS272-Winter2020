<template>
  <div id="app">
    <!-- <StatusBar title="COVID-19 News & Spread"/> -->
    <div id="main" class="main-content main-content-collapsed">
      <div style="grid-area: title">
        <b-button 
        @click="toggleView"
        size="is-medium"
        icon-left="window-maximize" 
        style="float:right; margin: 20px">{{view_maximized ? 'Overview' : 'Full View'}}</b-button>
        <h1 id="title" style="margin: 20px">COVID-19 News Coverage Analysis</h1>
      </div>
        <RadarChart style="grid-area: radar" 
        class="main-area"
        :data1="news_us"
        :data2="news_china"
        label1="US"
        label2="China"
        :date="date"
        />
      <Map :data="covid_confirmed" :date="date" style="grid-area: map"/>
      <!--
      <TwitterFeed :data="twitter" :date="date" style="grid-area: side1"/>
      -->
      <NewsFeedMixed id='side-area'
      :news1="news_us"
      :news2="news_china"
      :date="date"
      style="grid-area: side; display: none"/>
      <RegionDetail 
      :data="word_us" 
      :date="date"
      :news="news_us" 
      label="us" 
      style="grid-area: us" 
      class="main-area"/>
      <RegionDetail 
      :data="word_china" 
      :date="date" 
      :news="news_china"
      label="china" 
      style="grid-area: cn" 
      class="main-area"/>
      <!--<WordCloud :data="null" style="grid-area: cloud"/>-->
      <TimeControl
      :data_confirmed="covid_confirmed"
      :data_deaths="covid_deaths"
      :data_recovered="covid_recovered"
      :data_news1="news_us"
      :data_news2="news_china"
      label_news1="US News"
      label_news2="Chinese News"
      :after="new Date('01/10/2020')"
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
import Map from './components/Map.vue'
import TimeControl from './components/TimeControl.vue'
//import TwitterFeed from './components/TwitterFeed.vue'
import NewsFeedMixed from './components/NewsFeedMixed.vue'
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
    NewsFeedMixed,
    RadarChart
  },
  data() {
    return {
      view_maximized: true,
      selected_date: null,
      hover_date: null,
      twitter: null,
      news_us: null,
      news_china: null,
      word_us: null,
      word_china: null,
      covid_confirmed: null,
      covid_deaths: null,
      covid_recovered: null,
    }
  },
  computed: {
    date() {
      return this.selected_date == null ? this.hover_date : this.selected_date
    }
  },
  created() {
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

    d3.json('/data/western_wordcloud.json')
      .then((data) => {
        this.word_us = data
      })

    d3.json('/data/eastern_wordcloud.json')
      .then((data) => {
        this.word_china = data
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
  mounted() {
        document.getElementById('side-area').style.display = 'none'
        document.getElementsByClassName('main-area').forEach(element => {
          element.style.display = 'block'
        })
        //document.getElementById('main').classList.add('main-content-collapsed')
  },
  methods: {
    toggleView() {
      if (!this.view_maximized) {

        document.getElementById('side-area').style.display = 'none'
        document.getElementsByClassName('main-area').forEach(element => {
          element.style.display = 'block'
        })
        document.getElementById('main').classList.add('main-content-collapsed')
      } else {

        document.getElementById('side-area').style.display = 'block'
        document.getElementsByClassName('main-area').forEach(element => {
          element.style.display = 'none'
        })
        document.getElementById('main').classList.remove('main-content-collapsed')
      }

      this.view_maximized = !this.view_maximized
    },
    onTimeControlDateSelected(date) {
      this.selected_date = date
      // document.getElementById('main').classList.add('main-content-collapsed')
      // document.getElementById('side-area').style.display = 'none'
      // document.getElementsByClassName('main-area').forEach(element => {
      //   element.style.display = 'block'
      // })
    },
    onTimeControlDateUnSelected() {
      this.selected_date = null
      // document.getElementById('main').classList.remove('main-content-collapsed')
      // document.getElementById('side-area').style.display = 'block'
      // document.getElementsByClassName('main-area').forEach(element => {
      //   element.style.display = 'none'
      // })
    }
  }
}
</script>

<style>
body {
  background-color: #ECECEC;
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
  grid-template-columns: 0fr 2fr 1.5fr 600px 0fr;
  grid-template-rows: 7vh 56vh 30vh;
  grid-template-areas:
  ". title title title ."
  ". control control side ."
  ". control control map .";
  grid-column-gap: 20px;
  grid-row-gap: 20px;
  padding: 0px 0 0 0;
}

.main-content-collapsed {
  grid-template-areas:
  ". title title title ."
  ". radar us us ."
  ". radar cn cn ."
  ". control control map .";
  grid-template-rows: 7vh 28vh 28vh 30vh;
}

.content-panel {
  display: inline-block;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 10px;
  -webkit-box-shadow: 0px 0px 8px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0px 0px 4px 1px rgba(0, 0, 0, 0.1);
}

#title {
  font-size: 35px;
  color: #484848;
  text-align: left;
  font-weight: 900;
  padding-left: 10px;
}

</style>
