<template>
  <div id="nav" class="row justify-center">
    <router-link to="/">Home</router-link>
  </div>
  <router-view/>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      user: {},
      token: ''
    }
  },
}
</script>
