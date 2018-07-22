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
        <UrlList :search="search" v-on:edit="editURL" />
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

    <router-view></router-view>
  </v-layout>
</template>

<script>
import { mapState } from 'vuex';
import { logout } from '../lib/auth';
import { LogOut } from '../lib/store';

import UrlList from './UrlList';

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
      if (urlId) {
        this.$router.push({ name: 'editUrl', params: { urlId: urlId } });
      } else {
        this.$router.push({ name: 'newUrl' });
      }
    },
  },

  components: {
    UrlList,
  }
}
</script>

<style>
</style>
