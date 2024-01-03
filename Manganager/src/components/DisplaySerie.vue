<template>
  <div class="chapter">
    <div class="logo">
      <router-link :to="'/serie/'+serie.title">
        <img :src="'http://127.0.0.1:4444/API/get_preview/'+serie.title" width="200" height="300">
      </router-link>
    </div>
    <div class="chapter-info">
      {{serie.title}}
      {{serie.sites}}
      <p v-if="serie.last_chapter_read != undefined">Last Chapter : Chapter {{serie.last_chapter}}</p>
      <p v-if='serie.last_chapter_read != undefined && serie.last_chapter_read != "None"'>Last Chapter Read : Chapter {{serie.last_chapter_read}}</p>
    </div>
  </div>
</template>
<script>
export default {
  name: 'DisplaySerie',
  data(){
    return {
    }
  },
  props: {serie: Object},
  async created(){
    /*
    let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/"+this.title)
    this.serie = await r.json()
    console.log(this.serie)*/
  },
  methods:{
    async get_infos(){
      /*
      let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/"+this.title)
      this.serie = await r.json()
      console.log(this.serie)*/
    }
  }
}
</script>
<style>

.chapter-info{
  display:inline-block;
  margin-left: 3%;
}


.logo{
  display: inline-block;
  margin-right: 2%;
}


.chapter{
  margin-left : 2%;
  margin-right : 2%;
  margin-top : .1%;
  margin-bottom : .1%;
  background-color: white;
}

</style>
