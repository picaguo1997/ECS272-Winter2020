<template>
  <div class="content-panel">
      <div style="overflow: hidden; height:100%">
          <h3>WORDCLOUD</h3>
          <div v-if="data != null" class="scroll">
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
        data: Object,
    },
    data(){
      return{
        western_color: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef']
      }
    },
    methods: {
      loadFont(family, style, weight, text) {
        return (new FontFaceObserver(family, {style, weight})).load(text);
      },
      colorAssign: function([, weight]){
        if (weight > this.data.wordcloud_scope.Q3) //also got Q2
          return '#005CAF'
        else if (weight > this.data.wordcloud_scope.Q1)
          return '#5893d4'
        else
          return '#7DB9DE'
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
