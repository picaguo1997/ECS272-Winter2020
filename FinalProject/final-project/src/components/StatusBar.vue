<template>
  <div class="bar">
      <h2 class="title">{{title}}</h2>
  </div>
</template>

<script>
export default {
  name: 'StatusBar',
  props: {
    title: String
  }
}
</script>

<style scoped>
.bar{
    overflow: hidden;
    background-color: #242A3D;
    position: fixed;
    top: 10px;
    left: 15px;
    width: 400px;
    -webkit-box-shadow: 0px 0px 8px 1px rgba(0,0,0,0.5); 
    box-shadow: 0px 0px 8px 1px rgba(0,0,0,0.5);
}

.title {
    color: #FFF;
}
</style>