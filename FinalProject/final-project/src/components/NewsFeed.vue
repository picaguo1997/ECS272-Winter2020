<template>
  <div class="content-panel">
      <div style="overflow: hidden; height:100%">
          <h3>News Feed</h3>
          <div v-if="news1 != null && news2 != null && date != null" class="scroll">
              <NewsArticle v-for="article in getNews(news1,2)" :key="article.url" :data="article" />
              <NewsArticle v-for="article in getNews(news2,2)" :key="article.url" :data="article" />
          </div>
      </div>
  </div>
</template>

<script>
import NewsArticle from './NewsArticle'

export default {
    name: 'NewsFeed',
    components: {
        NewsArticle
    },
    props: {
        news1: Array,
        news2: Array,
        date: Date
    },
    methods: {
        getNews(data, limit) {
            if (data == null) {
                return []
            }

            var result = data.filter(e => {
                var news_date = new Date(e['time-stamp'])
                return (news_date.getUTCMonth() == this.date.getUTCMonth()) &&
                (news_date.getUTCDate() == this.date.getUTCDate()) &&
                (news_date.getUTCFullYear() == this.date.getUTCFullYear())
            })

            result.sort(() => Math.random() - 0.5)

            if (limit != null) {
                return result.slice(0,limit)
            } else {
                return result
            }
        }
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