<template>
  <v-layout>
    <v-toolbar color="light-blue" app absolute clipped-left>
      <span class="title ml-3 mr-5 hidden-sm-and-down">{{ title }}</span>
      <v-text-field
        solo-inverted
        flat
        hide-details
        label="Search"
        prepend-inner-icon="search"
        :autofocus="true"
        v-model="textToSearch"
      ></v-text-field>
      <v-spacer></v-spacer>
      <span class="hidden-sm-and-down">{{ userName }}</span>
      <v-btn flat @click.stop="logout()">Logout</v-btn>
    </v-toolbar>
    
    <v-content>
      <v-container fluid fill-height class="grey lighten-4">
        <UrlList :search="search" v-on:edit="editUrl" v-on:view-log="viewUrlLog" />
      </v-container>
    </v-content>

    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      @click.stop="editUrl(null)"
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

  props: {
    search: String,
  },

  data: () => ({
    dialog: false,
    title: process.env.APP_TITLE,
    loading: false,

    textToSearch: '',
    textToSearchDebounce: null,
  }),

  computed: mapState({
    userName: state => state.auth.name,
  }),

  watch: {
    textToSearch(val) {
      if (this.textToSearchDebounce) {
        clearTimeout(this.textToSearchDebounce);
      }

      this.textToSearchDebounce = setTimeout(
        () => {
          this.textToSearchDebounce = null;
          this.$router.push({ name: 'MainDisplay' , query: { search: val }});
        },
        500,
      );
    },

    search(val) {
      this.textToSearch = val;
    }
  },

  mounted() {
    this.textToSearch = this.search;
  },

  methods: {
    logout() {
      logout();
      this.$store.commit(LogOut);
    },

    editUrl(urlId) {
      if (urlId) {
        this.$router.push({ name: 'editUrl', params: { urlId: urlId }, query: this.$route.query });
      } else {
        this.$router.push({ name: 'newUrl', query: this.$route.query });
      }
    },

    viewUrlLog(urlId) {
      this.$router.push({ name: 'viewUrlLogs', params: { urlId: urlId }, query: this.$route.query });
    }
  },

  components: {
    UrlList,
  }
}
</script>

<style>
</style>
