<template>
  <div>
    <v-dialog v-model="loading" :persistent="true" width="300px">
      <v-card color="primary" dark>
        <v-card-text>
          Loading…
          <v-progress-linear indeterminate color="white" class="mb-0" /> 
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="hasLoadError" :persistent="true" width="300px" @keydown.esc="cancel()">
      <v-card>
        <v-card-title class="grey lighten-4 py-4 title">
          <span>Error</span>
        </v-card-title>

        <v-card-text>
          {{ loadError }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="cancel()">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="show" @keydown.esc="cancel()" max-width="700px">
      <v-card>
        <v-card-title class="grey lighten-4 py-4 title">
          <span>Logs for Redirect '<span v-html="slug"></span>'</span>
        </v-card-title>

        <v-layout row wrap>
          <v-flex xs12 align-center justify-space-between>
            <v-alert :value="readError != ''" :dismissible="true" type="error">
              {{ readError }}
            </v-alert>
          </v-flex>
          <v-flex xs-12 align-center justify-space-between>
            <v-data-table 
              :must-sort="true" 
              hide-headers
              :items="logs" 
              :rows-per-page-items="[5,10]"
            >
              <template slot="items" slot-scope="props">
                <td>{{ props.item.date_created | relativeTime }}</td>
                <td>{{ props.item.log_info }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="cancel()">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { getURL, getURLLogs } from '../lib/api';
import moment from 'moment';
import { logout } from '../lib/auth';
import { LogOut } from '../lib/store';

export default {
  name: 'UrlLogList',

  props: {
      urlId: Number,
  },

  data: () => ({
    show: false,

    loading: false,
    hasLoadError: false,
    loadError: '',
    readError: '',

    slug: '',
    logs: [],
    headers: [
      {
        text: 'Date',
        align: 'left',
        sortable: 'true',
        value: 'date_created',
      },

      {
        text: 'Note',
        align: 'left',
        sortable: false,
        value: 'log_info',
      },
    ]
  }),

  filters: {
    relativeTime(value) {
      return moment(value * 1000).fromNow();
    }
  },

  mounted() {
    this.begin();
  },

  methods: {
    begin() {
      this.loading = true;
      this.hasLoadError = false;

      if (isNaN(this.urlId)) {
        this.loadError = 'Redirect not found. Please check your URL and try again.';
        this.hasLoadError = true;
        this.show = false;
      } else if (this.urlId) {
        this.$nextTick(this.load);
      }
    },

    cancel() {
      this.$router.go(-1);
    },

    async load() {
      try {
        const response = await getURLLogs(this.$store.state.auth.token, this.urlId);

        this.slug = response.data.url.slug;
        this.logs = response.data.logs;

        this.loading = false;
        this.show = true;
      } catch (e) {
        if (e.response) {
          switch(e.response.status) {
            case 403:
              logout();
              this.$store.commit(LogOut);
              this.$router.push('/');
              break;

            case 404:
              this.loadError = 'Redirect not found';
              break;

            default:
              this.loadError = e.message;
          }
        } else {
          this.loadError = e.message;
        }
      }
    }
  }
}
</script>