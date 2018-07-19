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
        <v-flex fill-height>
          <v-list two-line>
            <template v-for="(item) in rows">
              <v-list-tile :key="item.slug">
                <v-list-tile-content>
                  <v-list-tile-title v-html="item.slug"></v-list-tile-title>
                  <v-list-tile-sub-title v-html="item.redirect"></v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-flex row>
                    <span class="caption">{{ item.views }} view<span v-if="item.views != 1">s</span></span>
                    <v-btn icon ripple>
                      <v-icon color="grey lighten-1">edit</v-icon>
                    </v-btn>
                  </v-flex>
                </v-list-tile-action>
              </v-list-tile>
            </template>
          </v-list>
          <mugen-scroll :handler="fetchData" :should-handle="!loading">
            <v-flex>
              <v-progress-circular :indeterminate="true" v-if="loading" />
            </v-flex>
          </mugen-scroll>
        </v-flex>
      </v-container>
    </v-content>

    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      @click.stop="toggleDialog()"
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
import MugenScroll from 'vue-mugen-scroll';
import { mapState } from 'vuex';
import { logout } from '../lib/auth';
import { LogOut } from '../lib/store';
import { searchURLs } from '../lib/api';
import UrlEdit from './UrlEdit';

export default {
  name: 'MainDisplay',
  data: () => ({
    dialog: false,
    title: process.env.APP_TITLE,
    loading: false,
    rows: [],
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
    async fetchData() {
      this.loading = true;

      const data = await searchURLs(this.$store.state.auth.token, this.search, this.rows.length);
      this.rows = this.rows.concat(data);

      this.loading = false;
    },
    toggleDialog() {
      this.$refs.urlEdit.toggle();
    }
  },
  watch: {
    search(val) {
      this.rows = [];
      this.fetchData();
    }
  },
  components: {
    MugenScroll,
    UrlEdit
  }
}
</script>

<style>
</style>
