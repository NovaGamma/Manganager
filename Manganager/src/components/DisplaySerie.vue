<template>
  <div
      @click="$router.push(`/serie/${serie.title}`)"
      class="property-card row"
  >
    <q-img
      :src="'http://127.0.0.1:4444/API/get_preview/'+serie.title"
      :placeholder-src="imageSrc"
      @error="replaceByDefault"
      style="border-radius: 10px; z-index: inherit"
      :ratio="9 / 12"
      spinner-color="grey"
      spinner-size="md"
      class="property-image row col-12"
    />
    <div class="col-12 q-px-sm">
      {{serie.title}}
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

.logo{
  display: inline-block;
  margin-right: 2%;
}


</style>
