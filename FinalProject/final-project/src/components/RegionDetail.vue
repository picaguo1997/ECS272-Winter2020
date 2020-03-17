<template>
  <div id="region-detail" class="content-panel">
    <WordCloud :data="word_data" :color="color" style="grid-area: cloud; width: 45%; height: 100%; float: left"
    />
    <NewsFeed :news="news" :date="date" style="grid-area: feed; width: 45%; height: 100%; float: left; margin-left: 40px"/>
  </div>
</template>

<script>
import NewsFeed from './NewsFeed.vue'
import WordCloud from './WordCloud.vue'

export default {
    name: 'RegionDetail',
    components:{
      WordCloud,
      NewsFeed
    },
    props: {
      data: Object,
      news: Array,
      label: String,
      date: Date
    },
    data() {
      return{
        width: 0,
        height: 0,
        color: null,
        word_date: null,
        word_data: null,
        word_ready: false,
        eastern_color: ['#A71739','#CB1B45', '#D44466', '#DD6D88', '#E797AA'],
        western_color: ['#004C90','#005CAF', '#2E79BD', '#5C97CC', '#8BB4DA']
      }
    },
    computed: {
      dataReady() {
        return this.data != null && this.label!= null && this.date!=null;
      }
    },
    watch:{
      date(newVal) {
        if (newVal != null && this.word_ready) {
          this.word_date = this.formatDate(newVal)
          if (typeof this.data[this.word_date] != 'undefined') {
            this.init()
          }
        }
      },
      dataReady() {
        this.init()
        this.word_ready=true;
      }
    },
    methods:{
      init(){
        this.word_data = this.data[this.word_date]

        if(this.label == "us"){
          this.color = this.western_color
        }
        else if (this.label == "china") {
          this.color = this.eastern_color
        }
      },
      formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2)
            month = '0' + month;
        if (day.length < 2)
            day = '0' + day;

        return [year, month, day].join('-');
    }
    }
}
</script>

<style scoped>
#region-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 100%;
  grid-column-gap: 150px;
  grid-template-areas:
  "cloud feed";
  padding: 50px;
}
</style>
