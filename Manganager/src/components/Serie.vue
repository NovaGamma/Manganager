<template>
  <div class="outer">
  <div class="box">
    <div>
      <img :src="'http://127.0.0.1:4444/API/get_preview/'+title">
      <div>
        {{title}}
        {{serie.site}}
        {{serie.last_chapter[0]}}
        <p v-if="serie.last_chapter_read != 'None'">
          {{serie.last_chapter_read[0]}}
        </p>
      </div>
    </div>
    <div>
      <select v-model="read_until">
        <option disabled value="">Select</option>
        <option v-for="chapter in chapters" :key="chapter[0]">{{chapter[0]}}</option>
      </select>
      <button @click="setRead()">Read until</button>
    </div>
    <div v-for="chapter in chapters" :key="chapter[0]" :class="{chapter:true, read:chapter[2]}">
      <a @click="open(chapter[1])">
        {{chapter[0]}}
      </a>
    </div>
 </div>
</div>
</template>
<script>
export default {
  name: 'Serie',
  data(){
    return {
      serie: Object,
      chapters: Array,
      read_until: ""
    }
  },
  props: {title:String},
  created(){
    this.get_infos()
    this.get_chapters()
  },
  methods:{
    async open(url){
      await fetch("http://127.0.0.1:4444/API/open/",{
        method:"POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'url':url
        })
      });
    },
    async get_infos(){
      let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/"+this.title)
      this.serie = await r.json()
    },
    async get_chapters(){
      let r = await fetch("http://127.0.0.1:4444/API/get_chap_list/"+this.title)
      this.chapters = await r.json()
    },
    async setRead(){
      await fetch("http://127.0.0.1:4444/API/read_until/",{
        method:"POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'title':this.title,
          'chapter':this.read_until
        })
      });
      await this.get_chapters();
      await this.get_infos();
    }
  }
}
</script>
<style>
  .outer{
    display:flex;
    justify-content:center;
  }
  .box{
    display:flex;
    flex-direction: column;
    width:fit-content;
    position:center
  }
  .chapter{
    border: 2px solid black;
    border-radius: 5px;
    padding:2px;
    margin:2px;
  }
  a{
    text-decoration: none;
    color:black;
  }
  a:hover{
    color:green;
  }
  .read{
    background-color:grey;
    color:white;
  }
</style>
