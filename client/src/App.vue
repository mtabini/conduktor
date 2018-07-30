<template>
  <v-app id="inspire">
    <router-view v-if="loggedIn" />
    <Login v-else />
  </v-app>
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

