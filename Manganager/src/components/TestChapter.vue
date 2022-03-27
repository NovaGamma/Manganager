<template>
  <div>
    {{chapterList}}
  </div>
</template>

<script>
export default {
  name: 'TestChapter',
  data(){
    return {
      chapterList:{}
    }
  },
  created(){
    this.getChapterList();
  },
  methods:{
    getChapterList(){
      fetch("http://localhost:4444/API/get_read_list")
        .then(response => response.json())
        .then(data => {this.chapterList = data});
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
