<template>
  <div>
    <div>
      <input type="text" v-model="input" placeholder="Search manga..." />
      <input type="text" v-model="add" placeholder="Add manga...(paste url)"/>
      <button @click="add_serie()">Add</button>
    </div>
    <div>
      <button v-if="page > 1" @click="page--">Previous Page</button>
      <a v-for="i in Math.floor(series.length/10)" @click="page=i" :key="i">{{i}}|</a>
      <button v-if="series.length/10 > page" @click="page++">Next Page</button>
    </div>
    <Filter @filter="send_filters"></Filter>
    <DisplaySerie v-for="serie in filtered_series" :key="serie" :serie="serie"/>
    <div>
      <button v-if="page > 1" @click="page--">Previous Page</button>
      <a v-for="i in Math.floor(series.length/10)" @click="page=i" :key="i">{{i}}|</a>
      <button v-if="series.length/10 > page" @click="page++; scrollTop()">Next Page</button>
    </div>
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
      page:1,
      per_page:10,
      params:{'finished':false, 'sort': "date"}
    }
  },
  async created(){
    await this.getChapterList();
  },
  computed: {
    filtered_series(){
      let start = (this.page-1) * this.per_page
      let end = this.page * this.per_page
      let filtered = this.series
      filtered = filtered.filter((serie)=>{
          return serie.title.toLowerCase().includes(this.input.toLowerCase())
      })
      if(filtered.length > this.per_page)
          filtered = filtered.slice(start,end)
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
