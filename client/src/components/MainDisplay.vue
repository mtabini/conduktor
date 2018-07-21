<template>
  <v-layout>
    <v-toolbar color="light-blue" app absolute clipped-left>
      <span class="title ml-3 mr-5">{{ title }}</span>
      <v-text-field
        solo-inverted
        flat
        hide-details
        label="Search"
        prepend-inner-icon="search"
        :autofocus="true"
        v-model="search"
      ></v-text-field>
      <v-spacer></v-spacer>
      <span>{{ userName }}</span>
      <v-btn flat @click.stop="logout()">Logout</v-btn>
    </v-toolbar>
    
    <v-content>
      <v-container fluid fill-height class="grey lighten-4">
        <URLList :search="search" v-on:edit="editURL" />
      </v-container>
    </v-content>

    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      @click.stop="editURL(null)"
    >
      <v-icon>add</v-icon>
    </v-btn>

    <url-edit ref="urlEdit" />
  </v-layout>
  <!-- <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div> -->
</template>

<script>
import { mapState } from 'vuex';
import { logout } from '../lib/auth';
import { LogOut } from '../lib/store';

import UrlEdit from './UrlEdit';
import URLList from './URLList';

export default {
  name: 'MainDisplay',
  data: () => ({
    dialog: false,
    title: process.env.APP_TITLE,
    loading: false,
    search: '',
  }),

  computed: mapState({
    userName: state => state.auth.name,
  }),

  methods: {
    logout() {
      logout();
      this.$store.commit(LogOut);
    },

    editURL(urlId) {
      console.log(urlId);
    },
  },

  components: {
    URLList,
    UrlEdit,
  }
}
</script>

<style>
</style>
