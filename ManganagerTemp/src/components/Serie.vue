<template>
  <div class="outer">
  <div class="box">
    <div>
      <img :src="'http://127.0.0.1:4444/API/get_preview/'+title" width="200" height="300"/>
      <div>
        {{title}}
        <br>
        <div>
          <button @click="drop()">Drop</button>
          <button @click='del()'>Remove</button>
        </div>
        <button v-for="site of serie.sites" :key="site" @click="displayedSite = site">
          {{site}}
        </button> 
        <br>
        Last Chapter: Chapter {{serie.last_chapter}}
        <p v-if="serie.last_chapter_read != 'None'">
          Last Chapter Read: Chapter {{serie.last_chapter_read}}
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
    <div v-for="chapter of chapters[displayedSite]" :key="chapter[2]" :class="{chapter:true, read: serie.read.includes(chapter[2])}">
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
      read_until: "",
      displayedSite: ''
    }
  },
  props: {title:String},
  async created(){
    await this.get_infos()
    await this.get_chapters()
    this.displayedSite = this.serie.sites[0]
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
    async del(){
      if(confirm('Do you want to delete ?')){
        await fetch("http://127.0.0.1:4444/API/delete",{
          method:"POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'title':this.title
          })
        })
      }
    },
    async drop(){
      await fetch("http://127.0.0.1:4444/API/drop",{
          method:"POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'title':this.title
          })
        }) 
    },
    async get_infos(){
      let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/"+this.title)
      this.serie = await r.json()
      console.log(this.serie)
    },
    async get_chapters(){
      let r = await fetch("http://127.0.0.1:4444/API/get_chap_list/"+this.title)
      let chapters = await r.json()
      let chapters_parsed = {}
      for(let site of Object.keys(chapters)) {
        let list_chapters = []
        for(let number of Object.keys(chapters[site])) {
          list_chapters.push(chapters[site][number])
        }
        list_chapters.sort((a,b) => a[2] - b[2])
        chapters_parsed[site] = list_chapters
      }
      this.chapters = chapters_parsed
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
