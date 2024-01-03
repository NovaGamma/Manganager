<template>
  <div class="column items-center">
    <div class="row">
      <q-input class="q-mr-md" type="text" v-model="input" placeholder="Search manga..." />
      <q-input class="q-mr-md" type="text" v-model="add" placeholder="Add manga...(paste url)"/>
      <q-btn @click="add_serie()" label="Add" />

    </div>
    <Filter @filter="send_filters"></Filter>

    <div class="row">
      <div v-for="serie in filtered_series"
        class="col-xs-4 col-sm-3 col-md-2 q-pa-sm"
        :key="serie" 
      >
        <DisplaySerie 
          class="fit hover"
          :serie="serie"
        />
      </div>
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

.hover {
  border-radius: 10px;
  height: fit-content;
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.hover:hover {
  box-shadow: 0px 0px 14px 1px rgba(0, 0, 0, 0.2);
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
