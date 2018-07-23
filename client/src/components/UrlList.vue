<template>
  <v-flex fill-height>

    <v-alert :value="errorMessage != ''" :dismissible="true" type="error">
      {{ errorMessage }}. Please refresh to try again.
    </v-alert>

    <v-card v-if="rows.length > 0 || !loading">
      <v-data-table 
        :headers="headers"
        :items="rows" 
        :rows-per-page-items="[5,10]"
        hide-actions
        :loading="loading"
        class="hidden-sm-and-down"
      >
        <template slot="no-data">
          <v-container fluid class="text-xs-center font-weight-bold">
            No results found.
          </v-container>
        </template>
        <template slot="items" slot-scope="props">
          <td class="table-list" @click="editURL(props.item.id)">
            <span class="font-weight-bold">{{ props.item.slug }}</span>
            <v-chip v-if="!props.item.active" small disabled>Inactive</v-chip>
          </td>
          <td class="table-list" @click="editURL(props.item.id)">
            {{ props.item.redirect }}
          </td>
          <td class="table-list" @click="editURL(props.item.id)">
            {{ props.item.description }}
          </td>
          <td class="justify-center layout px-0">
            <v-icon class="mr-2" small @click="copyLink(props.item.slug)" color="light-blue" title="View activity log">info</v-icon>
            <v-icon class="mr-3" small @click="viewLog(props.item.id)" color="light-blue" title="Copy link to clipboard">content_copy</v-icon>
          </td>
        </template>
      </v-data-table>

      <v-list two-line class="hidden-md-and-up">
        <v-list-tile v-if="rows.length == 0">
          <v-list-tile-content>
            <v-list-tile-sub-title>
              No results found.
            </v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>

        <template v-for="(item, index) in rows">
          <v-divider v-if="index != 0" :key="index" />
          <v-list-tile @click="editURL(item.id)" :key="item.slug">
            <v-list-tile-content>
              <v-list-tile-title>
                <span v-html="item.slug"/>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <span v-html="item.redirect" />
              </v-list-tile-sub-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-flex row>
                <v-chip v-if="!item.active" small disabled>Inactive</v-chip>
                <v-btn icon class="mx-2" title="Copy link to clipboard" @click.stop="copyLink(item.slug)">
                  <v-icon color="light-blue">content_copy</v-icon>
                </v-btn>
                <span class="caption">{{ item.views }} view<span v-if="item.views != 1">s</span></span>
              </v-flex>
            </v-list-tile-action>
          </v-list-tile>
        </template>
      </v-list>

    </v-card>
    
    <v-flex class="text-xs-center pt-3">
      <v-progress-circular v-if="loading" :indeterminate="true"/>
      <span @click="fetchData()" v-if="errorMessage == '' && !loading && loadMore">Load more…</span>
    </v-flex>

    <span ref="clipboardSpan"></span>

    <v-snackbar
      v-model="clipboardCopied"
      :timeout="3000"
    >
      URL copied to clipboard.
      <v-btn dark flat @click="clipboardCopied=false">
        Close
      </v-btn>
    </v-snackbar>
  </v-flex>

</template>

<script>
import { mapState } from 'vuex';
import { SetURLs, AddURLs, LogOut } from '../lib/store';
import { searchURLs } from '../lib/api';
import { logout } from '../lib/auth';

const EditUrlEvent = 'edit';
const ViewUrlLogEvent = 'view-log';

export default {
  name: 'UrlList',

  props: {
    search: String,
  },

  data: () => ({
    loading: false,
    loadMore: true,
    errorMessage: '',

    headers: [
      {
        text: 'Slug',
        sortable: false,
      },
      {
        text: 'URL',
        sortable: false,
      },
      {
        text: 'Description',
        sortable: false,
        width: '100%',
      },
      {
        text: '',
        sortable: false,
      },
    ],

    clipboardCopied: false,
  }),

  computed: mapState({
    rows: state => Object.values(state.urls).sort(((l, r) => l.slug.toLowerCase().localeCompare(r.slug.toLowerCase()))),
  }),

  methods: {
    async fetchData(reset=false) {
      this.loading = true;
      this.errorMessage = '';

      try {
        const data = await searchURLs(this.$store.state.auth.token, this.search, reset ? 0 : Object.keys(this.rows).length);

        if (reset) {
          this.$store.commit(SetURLs, data.rows)
        } else {
          this.$store.commit(AddURLs, data.rows)
        }

        this.loadMore = data.hasMore;
      } catch(e) {
        console.log(e);
        if (e.response && e.response.status == 403) {
          logout();
          this.$store.commit(LogOut);
          this.$router.push('/');
        } else {
          this.errorMessage = e.message;
        }
      }

      this.loading = false;
    },

    editURL(urlId) {
      this.$emit(EditUrlEvent, urlId);
    },

    copyLink(slug) {
      const span = this.$refs.clipboardSpan;

      span.innerText = `${process.env.BASE_URL}/${slug}`;

      const range = document.createRange();
      range.selectNode(span);

      const selection = window.getSelection();

      selection.removeAllRanges();
      selection.addRange(range);

      document.execCommand('copy');

      span.innerHTML = '';

      this.clipboardCopied = true;
    },

    viewLog(urlId) {
      this.$emit(ViewUrlLogEvent, urlId);
    }
  },

  watch: {
    search(val) {
      this.fetchData(true);
    }
  },

  mounted() {
    this.$store.commit(SetURLs, []);
    this.fetchData(true);
  }
}

</script>

<style scoped>
.table-list {
  cursor: pointer;
  text-overflow: ellipsis;
}
</style>
