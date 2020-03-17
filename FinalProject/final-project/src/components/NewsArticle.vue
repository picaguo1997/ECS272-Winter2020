<template>
<div class="article" v-on:click="articleClicked()">
    <div style="grid-area: img">
        <img :src="getImagePath()" width=50>
    </div>
    <div style="grid-area: text">
        <b>{{data.headline}}</b>
        <!-- <br><br>
        {{data.journal}}, {{data['time-stamp']}} -->
    </div>
</div>
</template>

<script>
export default {
    name: 'NewsArticle',
    props: {
        data: Object
    },
    methods: {
        articleClicked() {
            window.open(this.data.url, '_blank');
        },
        getImagePath() {
            let path = '/img/'

            switch(this.data.journal) {
                case 'ABC News':
                    path += 'abc.png'
                    break
                case 'Breitbart':
                    path += 'bb.png'
                    break
                case 'CNN':
                    path += 'cnn.png'
                    break
                case 'FoxNews':
                    path += 'fox.svg'
                    break
                case 'New York Times':
                    path += 'nyt.jpg'
                    break
                case 'Washington Post':
                    path += 'wp.png'
                    break

                case 'CGTN':
                    path += 'cgtn.png'
                    break
                case 'ECNS':
                    path += 'ecns.jpg'
                    break
                case 'People':
                    path += 'people.jpg'
                    break
                case 'Xinhua':
                    path += 'xinhua.jpg'
                    break
            }

            return path
        }
    }
}
</script>

<style scoped>
.article {
    display: grid;
    grid-template-columns: 75px 1.5fr;
    grid-template-areas: "img text";
    text-align: left;
    align-items: center;
    grid-column-gap: 15px;

    margin: 10px;
    padding: 3px;
    /* border: 2px solid grey; */
    /* border-radius: 15px; */
    background-color: #fff;
    color: rgb(70, 70, 70);
    cursor: pointer;
/* -webkit-box-shadow: 5px 5px 10px 0px rgba(0,0,0,0.16);
-moz-box-shadow: 5px 5px 10px 0px rgba(0,0,0,0.16);
box-shadow: 5px 5px 10px 0px rgba(0,0,0,0.16); */
}
</style>