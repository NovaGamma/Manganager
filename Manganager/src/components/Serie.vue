<template>
  <div class="row justify-center">
    <div class="col-7 column items-center">
      <img :src="'http://127.0.0.1:4444/API/get_preview/'+title" width="200" height="300"/>
      <div>
        {{title}}
        <br>
        <div>
          <q-btn @click="$router.push(`/admin/${serie.title}`)" label="admin" />
          <q-btn @click="drop()" label="drop"/>
          <q-btn @click="del()" label="remove"/>
          <q-btn @click="update()" icon="autorenew" />
        </div>
        <q-btn
          v-for="site of serie.sites"
          :label="site"
          :key="site"
          @click="displayedSite = site"
        />
        <q-linear-progress
          :value="serie.last_chapter_read / serie.last_chapter"
          size="7px"
          stripe
          rounded
        />
        <p v-if="serie.last_chapter_read != 0" class="no-margin">
          {{ serie.last_chapter_read }} / {{ serie.last_chapter }}
        </p>
      </div>
    </div>
    <div class="col-6 column items-center">
      <div class="full-width">
        <select v-model="read_until">
          <option disabled value="">Select</option>
          <option v-for="chapter in chapters[displayedSite]" :key="chapter[2]">{{chapter[0]}}</option>
        </select>
        <button @click="setRead()">Read until</button>
      </div>
      <div
        v-for="chapter of chapters[displayedSite]" :key="chapter[2]"
        class="hover q-pa-sm q-my-xs full-width"
        :class="{read: serie.read.includes(chapter[2])}"
        @click="open(chapter[1])"
      >
        <p class="no-margin">
          {{ chapter[0] }}
        </p>
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
  props: {title: String},
  async created(){
    await this.get_infos()
    await this.get_chapters()
    this.displayedSite = this.serie.sites[0]
    for (let site of this.serie.sites) {
      let len = this.chapters[site].length
      if (len > this.chapters[this.displayedSite].length) {
        this.displayedSite = site
      }
    }
  },
  methods: {
    async open(url){
      await fetch("http://127.0.0.1:4444/API/open/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: url
        })
      })
    },
    async del(){
      if (confirm('Do you want to delete ?')){
        await fetch("http://127.0.0.1:4444/API/delete", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title
          })
        })
      }
    },
    async update() {
      await fetch("http://127.0.0.1:4444/API/add_site/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title,
          site: 'asurascans'
        })
      })
    },
    async drop(){
      await fetch("http://127.0.0.1:4444/API/drop",{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title
        })
      })
    },
    async get_infos(){
      let r = await fetch("http://127.0.0.1:4444/API/get_infos_serie/" + this.title)
      this.serie = await r.json()
      console.log(this.serie)
    },
    async get_chapters(){
      let r = await fetch("http://127.0.0.1:4444/API/get_chap_list/" + this.title)
      let chapters = await r.json()
      let chapters_parsed = {}
      for (let site of Object.keys(chapters)) {
        let list_chapters = []
        for (let number of Object.keys(chapters[site])) {
          list_chapters.push(chapters[site][number])
        }
        list_chapters.sort((a, b) => a[2] - b[2])
        chapters_parsed[site] = list_chapters
      }
      this.chapters = chapters_parsed
    },
    async setRead(){
      let chapterNumber = this.chapters[this.displayedSite].filter((chapter) => this.read_until == chapter[0])[0][2]
      await fetch("http://127.0.0.1:4444/API/read_until/",{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: this.title,
          chapter: chapterNumber
        })
      })
      await this.get_chapters()
      await this.get_infos()
    }
  }
}
</script>
<style>
  .read{
    background-color:grey;
    color:white;
  }

  .hover {
  border-radius: 10px;
  height: fit-content;
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.hover:hover {
  box-shadow: 0px 0px 14px 1px rgba(0, 0, 0, 0.2);
}
</style>
