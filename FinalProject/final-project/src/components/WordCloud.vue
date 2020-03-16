<template>
  <div class="content-panel">
      <div style="overflow: hidden; height:100%">
          <h3>WORDCLOUD</h3>
          <div v-if="data!=null" class="scroll">
            <vue-word-cloud
              :words="data.wordcloud"
              :color="colorAssign"
              :spacing="0.4"
              :load-font="loadFont"
              font-family="Helvetica"
            />
            <!--
            <wordcloud :data="data" nameKey="word" valueKey="value"
              :color="western_color"
              spiral="rectangular"
              :showTooltip="true"
              font="serif"
              :wordClick="wordClickHandler">
            </wordcloud>-->
          </div>
      </div>
  </div>
</template>

<script>
//import wordcloud from 'vue-wordcloud'
import VueWordCloud from 'vuewordcloud'
import FontFaceObserver from 'fontfaceobserver'

export default {
    name: 'WordCloud',
    components:{
      //wordcloud
      [VueWordCloud.name]: VueWordCloud
    },
    props: {
        data: Object
    },
    data(){
      return{
        eastern_color: ['#A71739','#CB1B45', '#D44466', '#DD6D88', '#E797AA'],
        western_color: ['#004C90','#005CAF', '#2E79BD', '#5C97CC', '#8BB4DA'],
        wordcloud_ready: false
      }
    },
    methods: {
      loadFont(family, style, weight, text) {
        return (new FontFaceObserver(family, {style, weight})).load(text);
      },
      colorAssign: function([, weight]){
        if (weight > this.data.wordcloud_scope.Q3) //also got Q2
          return this.western_color[0]
        else if (weight > this.data.wordcloud_scope.Q2)
          return this.western_color[1]
        else if (weight > this.data.wordcloud_scope.Q1)
          return this.western_color[2]
        else
          return this.western_color[3]
      }
      /*
      wordClickHandler(name, value, vm) {
        console.log('wordClickHandler', name, value, vm);
      }*/
    }
}
</script>

<style scoped>
.scroll {
    padding:10px;
    overflow-x: hidden;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    height: calc(100% - 95px);
    /* Below lines hide the scroll bar */
    width: 100%;
    padding-right: 17px;
    box-sizing: content-box;
}
</style>
