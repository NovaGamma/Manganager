<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
  </div>
  <router-view/>
</template>


<script>
export default{
  name:'NavBar',
  data(){
    return {
      user:{},
      token:''
    }
  },
}


</script>
