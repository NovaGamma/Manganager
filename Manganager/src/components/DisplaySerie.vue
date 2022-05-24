<template>
  <div class="chapter">
    <div class="logo">
      <router-link :to="'/serie/'+serie.title">
        <img :src="'http://127.0.0.1:4444/API/get_preview/'+serie.title">
      </router-link>
    </div>
    <div class="chapter-info">
      {{serie.title}}
      <p v-if="serie.last_chapter_read != undefined">Last Chapter : {{serie.last_chapter[0]}}</p>
      <p v-if='serie.last_chapter_read != undefined && serie.last_chapter_read != "None"'>Last Chapter Read : {{serie.last_chapter_read[0]}}</p>
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
  props: {serie:Object},
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
  margin-left : 15%;
  margin-right : 15%;
  margin-top : 2%;
  margin-bottom : 2%;
  background-color: white;
}

</style>
