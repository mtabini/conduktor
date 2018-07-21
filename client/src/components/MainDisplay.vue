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
          <v-card>
            <v-list two-line>
              <template v-for="(item, index) in rows">
                <v-list-tile @click="editURL(item.id)" :key="item.slug">
                  <v-list-tile-content>
                    <v-list-tile-title v-html="item.slug"></v-list-tile-title>
                    <v-list-tile-sub-title v-html="item.redirect"></v-list-tile-sub-title>
                  </v-list-tile-content>
                  <v-list-tile-action>
                    <v-flex row>
                      <span class="caption">{{ item.views }} view<span v-if="item.views != 1">s</span></span>
                    </v-flex>
                  </v-list-tile-action>
                </v-list-tile>
                <v-divider :key="index" />
              </template>
            </v-list>
          </v-card>
          <v-flex class="text-xs-center pt-3">
            <v-progress-circular v-if="loading" :indeterminate="true"/>
            <span @click="fetchData()" v-else>Load more…</span>
          </v-flex>
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
import { LogOut, SetURLs, AddURLs, SetURLToEdit } from '../lib/store';
import { searchURLs } from '../lib/api';
import UrlEdit from './UrlEdit';

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
    rows: state => state.urls,
  }),
  methods: {
    logout() {
      logout();
      this.$store.commit(LogOut);
    },
    async fetchData(reset=false) {
      this.loading = true;

      const data = await searchURLs(this.$store.state.auth.token, this.search, this.rows.length);

      if (reset) {
        this.$store.commit(SetURLs, data)
      } else {
        this.$store.commit(AddURLs, data)
      }

      this.loading = false;
    },
    editURL(urlId) {
      this.$refs.urlEdit.toggle(urlId);
    }
  },
  watch: {
    search(val) {
      this.fetchData(true);
    }
  },
  components: {
    UrlEdit
  }
}
</script>

<style>
</style>
