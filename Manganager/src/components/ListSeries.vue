<template>
  <div>
    <input type="text" v-model="input" placeholder="Search manga..." />
    <input type="text" v-model="add" placeholder="Add manga...(paste url)"/>
    <button @click="add_serie()">Add</button>
    <div v-for="serie in filteredList()" :key="serie.title" class="chapter">
      <div class="logo">
        <router-link :to="'/serie/'+serie.title">
          <img :src="'http://127.0.0.1:4444/API/get_preview/'+serie.title">
        </router-link>
      </div>
      <div class="chapter-info">
        {{serie.title}}
        <p>Last Chapter : {{serie.last_chapter[0]}}</p>
        <p v-if='serie.last_chapter_read != "None"'>Last Chapter Read : {{serie.last_chapter_read[0]}}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue"
export default {
  name: 'ListSeries',
  data(){
    return {
      series:[],
      input : "",
      add : "",
    }
  },
  created(){
    this.getChapterList();
  },
  methods:{
    async getChapterList(){
      let response = await fetch("http://127.0.0.1:4444/API/get_read_list")
        let series = await response.json()
        for(let serie of series){
          console.log(serie)
          let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/"+serie)
          this.series.push(await r.json())
        }
      console.log(this.series)
    },
    filteredList(){
      return this.series.filter((serie)=>{
          return serie.title.toLowerCase().includes(this.input.toLowerCase())
        }
      );
    },
    async add_serie(){
      let url = this.add;
      await fetch("http://127.0.0.1:4444/API/add_serie/",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'url':url
        })
      });
      this.getChapterList();
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chapter-info{
  display:inline-block;
  margin-left: 3%;
}

.logo{

}

.chapter{
  margin-left : 15%;
  margin-right : 15%;
  margin-top : 2%;
  margin-bottom : 2%;
  background-color: white;
}

.logo{
  display: inline-block;
  margin-right: 2%;
}

.text{
  display: inline-block;

}

.template{
  background-color: aliceblue;
}

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
