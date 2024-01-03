<template>
  <div>
    <div>
      <input type="text" v-model="input" placeholder="Search manga..." />
      <input type="text" v-model="add" placeholder="Add manga...(paste url)"/>
      <button @click="add_serie()">Add</button>
    </div>
    <Filter @filter="send_filters"></Filter>
    <DisplaySerie v-for="serie in filtered_series" :key="serie" :serie="serie"/>
  </div>
</template>

<script>
import DisplaySerie from "./DisplaySerie.vue"
import Filter from "./Filter.vue"
export default {
  name: 'ListSeries',
  components :{DisplaySerie, Filter},
  data(){
    return {
      series:[],
      input : "",
      add : "",
      params:{'finished':false, 'sort': "date"}
    }
  },
  async created(){
    await this.getChapterList();
  },
  computed: {
    filtered_series(){
      let filtered = this.series
      filtered = filtered.filter((serie)=>{
          return serie.title.toLowerCase().includes(this.input.toLowerCase())
      })
      return filtered
    }
  },
  methods:{
    async getChapterList(){
      let response = await fetch(`http://127.0.0.1:4444/API/get_read_list?finished=${this.params.finished}&sort=${this.params.sort}`)
      this.series = await response.json()
      console.log(this.series)
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
    },
    scrollTop(){
      window.scrollTo(0,0);
    },
    async send_filters(finished, sort){
        console.log(finished);
        this.params.sort = sort;
        this.params.finished = finished;
        await this.getChapterList();
    }
  },
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
