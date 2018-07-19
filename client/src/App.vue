<template>
  <v-app id="inspire">
    <MainDisplay v-if="loggedIn" />
    <Login v-else />
  </v-app>
  <!-- <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div> -->
</template>

<script>
import { mapState } from 'vuex';
import Login from './components/Login';
import MainDisplay from './components/MainDisplay';

export default {
  name: 'App',
  data: () => ({
    dialog: false,
  }),
  computed: mapState({
    loggedIn: state => state.auth.loggedIn,
  }),
  components: {
    Login,
    MainDisplay
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
