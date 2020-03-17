<template>
      <div style="overflow: hidden; height:100%">
          <div v-if="news != null && date != null" class="scroll">
            <NewsArticle v-for="article in getNews(news,5)" :data="article"  :key="article.url" />
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
        news: Array,
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
    height: 100%;
    /* Below lines hide the scroll bar */
    width: 100%;
    box-sizing: content-box;
}
</style>