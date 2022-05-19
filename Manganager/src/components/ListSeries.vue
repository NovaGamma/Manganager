<template>
  <div>
    <div>
      <input type="text" v-model="input" placeholder="Search manga..." />
      <input type="text" v-model="add" placeholder="Add manga...(paste url)"/>
      <button @click="add_serie()">Add</button>
    </div>
    <button v-if="page > 1" @click="page--">Previous Page</button>
    <a v-for="i in Math.floor(series.length/10)" @click="page=i" :key="i">{{i}}|</a>
    <button v-if="series.length/10 > page" @click="page++">Next Page</button>
    {{(page-1)*10}}/{{page*10-1}}
    <DisplaySerie v-for="serie in filteredList().slice((page-1)*10,page*10-1)" :key="serie" :title="serie"/>
  </div>
</template>

<script>
import { ref } from "vue"
import DisplaySerie from "./DisplaySerie.vue"
export default {
  name: 'ListSeries',
  components :{DisplaySerie},
  data(){
    return {
      series:[],
      input : "",
      add : "",
      page:1
    }
  },
  async created(){
    await this.getChapterList();
  },
  methods:{
    async getChapterList(){
      let response = await fetch("http://127.0.0.1:4444/API/get_read_list")
      this.series = await response.json()
      console.log(this.series)
    },
    filteredList(){
      return this.series.filter((serie)=>{
          return serie.toLowerCase().includes(this.input.toLowerCase())
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
