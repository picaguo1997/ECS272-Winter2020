<template>
    <div id="wordcloud" v-if="data!=null">
      <vue-word-cloud
        :words="data.wordcloud"
        :color="colorAssign"
        :spacing="0.4"
        :load-font="loadFont"
        font-family="Helvetica"
        :font-size-ratio="5"
      />
    </div>
</template>

<script>
import VueWordCloud from 'vuewordcloud'
import FontFaceObserver from 'fontfaceobserver'

export default {
    name: 'WordCloud',
    components:{
      [VueWordCloud.name]: VueWordCloud
    },
    props: {
        data: Object,
        color: Array
    },
    methods: {
      loadFont(family, style, weight, text) {
        return (new FontFaceObserver(family, {style, weight})).load(text);
      },
      colorAssign: function([, weight]){
        if (weight > this.data.wordcloud_scope.Q3) //also got Q2
          return this.color[0]
        else if (weight > this.data.wordcloud_scope.Q2)
          return this.color[1]
        else if (weight > this.data.wordcloud_scope.Q1)
          return this.color[2]
        else
          return this.color[3]
      }
    }
}
</script>

<style scoped>
#wordcloud {
    display: inline-block;
    padding: 10px;
    overflow: hidden;
    width: 800px;
    height: 200px;
}
</style>
