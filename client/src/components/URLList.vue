<template>
  <v-flex fill-height>

    <v-alert :value="errorMessage != ''" :dismissible="true" type="error">
      {{ errorMessage }}. Please refresh to try again.
    </v-alert>

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
      <span @click="fetchData()" v-if="!loading && loadMore">Load more…</span>
    </v-flex>
  </v-flex>
</template>

<script>
import { mapState } from 'vuex';
import { SetURLs, AddURLs } from '../lib/store';
import { searchURLs } from '../lib/api';

const EditUrlEvent = 'edit';

export default {
  name: 'URLList',

  props: {
    search: String,
  },

  data: () => ({
    loading: false,
    loadMore: true,
    errorMessage: '',
  }),

  computed: mapState({
    rows: state => state.urls,
  }),

  methods: {
    async fetchData(reset=false) {
      this.loading = true;
      this.errorMessage = '';

      try {
        const data = await searchURLs(this.$store.state.auth.token, this.search, Object.keys(this.rows).length);


        if (reset) {
          this.$store.commit(SetURLs, data.rows)
        } else {
          this.$store.commit(AddURLs, data.rows)
        }

        this.loadMore = data.hasMore;
      } catch(e) {
        this.errorMessage = e.message;
      }

      this.loading = false;
    },

    editURL(urlId) {
      this.$emit(EditUrlEvent, urlId);
    }
  },

  watch: {
    search(val) {
      this.fetchData(true);
    }
  },

  mounted() {
    this.fetchData(true);
  }
}

</script>