<template>
  <div class="content-panel">
      <div style="overflow: hidden; height:100%">
          <h3>WORDCLOUD</h3>
          <div v-if="data != null" class="scroll">
            <wordcloud :data="data" nameKey="word" valueKey="value"
              :color="western_color"
              spiral="rectangular"
              :showTooltip="true"
              font="serif"
              :wordClick="wordClickHandler">
            </wordcloud>
          </div>
      </div>
  </div>
</template>

<script>
import wordcloud from 'vue-wordcloud'

export default {
    name: 'WordCloud',
    components:{
      wordcloud
    },
    props: {
        data: Array,
    },
    data(){
      return{
        western_color: ['#1f77b4', '#629fc9', '#94bedb', '#c9e0ef']
      }
    },
    methods: {
      wordClickHandler(name, value, vm) {
        console.log('wordClickHandler', name, value, vm);
      }
    },
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
