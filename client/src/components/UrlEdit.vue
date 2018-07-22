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
    <v-dialog v-model="hasLoadError" :persistent="true" width="300px">
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
    <v-dialog v-model="show">
      <v-card>
        <v-form v-model="canSubmit" ref="form">
          <v-card-title class="grey lighten-4 py-4 title">
            <span v-if="id == 0">Create URL</span>
            <span v-else>Update URL</span>
          </v-card-title>

          <v-container grid-list-sm class="pa-4">
              <v-layout row wrap>
                <v-flex xs12 align-center justify-space-between>
                  <v-alert :value="saveError != ''" :dismissible="true" type="error">
                    {{ saveError }}
                  </v-alert>
                </v-flex>
                <v-flex xs12 align-center justify-space-between>
                  <v-text-field
                    v-model="slug"
                    placeholder="Slug"
                    required
                    :rules="[() => validateRequiredField(slug), validateSlug]"
                    :disabled="saving"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 align-center justify-space-between>
                  <v-text-field
                    v-model="redirect"
                    placeholder="Redirect to"
                    required
                    :rules="[() => validateRequiredField(redirect), validateRedirect]"
                    :disabled="saving"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 align-center justify-space-between>
                  <v-text-field
                    v-model="description"
                    placeholder="Description"
                    required
                    :rules="[() => validateRequiredField(description)]"
                    :disabled="saving"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 align-center justify-space-between>
                  <v-checkbox
                    label="Active"
                    v-model="active"
                    :disabled="saving"
                  />
                </v-flex>
              </v-layout>
          </v-container>
          
          <v-card-actions>
            <v-btn flat @click="viewLogs()" :disabled="saving">Activity Log</v-btn>
            <v-spacer></v-spacer>
            <v-btn flat color="primary" @click="cancel()" :disabled="saving">Cancel</v-btn>
            <v-btn flat :disabled="!canSubmit || saving" @click.stop="save()" :loading="saving">
              <span v-if="id == 0">Create</span>
              <span v-else>Update</span>
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { createURL, updateURL, getURL } from '../lib/api';
import { UpdateURL } from '../lib/store';

export default {
  name: 'UrlEdit',

  props: {
    urlId: Number,
  },

  data: () => ({
    show: false,

    loading: false,
    hasLoadError: false,
    loadError: '',

    canSubmit: false,
    saving: false,
    saveError: '',

    id: 0,
    slug: '',
    redirect: '',
    description: '',
    active: true,
  }),

  mounted() {
    this.begin();
  },

  methods: {
    validateRequiredField(val) {
      return (val && val.length > 0) || 'Required field';
    },

    validateSlug() {
      return !!this.slug.match(/[a-z0-9][a-z0-9_\-]{3,}/) || 'Must start with a letter or digit and be 4 characters or more long'
    },

    validateRedirect() {
      const regex = "^(https?://)?(www\\.)?([-a-z0-9]{1,63}\\.)*?[a-z0-9][-a-z0-9]{0,61}[a-z0-9]\\.[a-z]{2,6}(/[-\\w@\\+\\.~#\\?&/=%]*)?$";
      return !!this.redirect.match(regex) || 'Must be a valid URL and start with either "http://" or "https://"'
    },

    begin() {
      this.id = 0;
      this.slug = '';
      this.redirect = '';
      this.description = '';
      this.active = true;
      this.views = 0;

      this.hasLoadError = false;
      this.loading = !!this.urlId;
      this.saving = false;
      this.show = !this.urlId;

      if (isNaN(this.urlId)) {
        this.loadError = 'Redirect not found. Please check your URL and try again.';
        this.hasLoadError = true;
        this.show = false;
      } else if (this.urlId) {
        this.$nextTick(this.load);
      }
    },

    cancel() {
      this.$router.push('/');
    },

    viewLogs() {
      this.$router.push({ name: 'viewUrlLogs', params: { urlId: this. urlId } })
    },

    async load() {
      try {
        const response = await getURL(this.$store.state.auth.token, this.urlId);
        const url = response.data;

        this.id = url.id;
        this.slug = url.slug;
        this.redirect = url.redirect;
        this.description = url.description;
        this.active = url.active;
        this.views = url.views;

        this.loading = false;
        this.show = true;
      } catch (e) {
        console.error(e);
        this.loading = false;

        if (e.response) {
          switch(e.response.status) {
            case 404:
              this.loadError = 'Redirect not found. Please check your URL and try again.';
              break;

            case 500:
              this.loadError = 'A server error has occurred. Please refresh this page to try again.';
              break;

            default:
              this.loadError = e.message;
          }
        } else {
          this.loadError = e.message;
        }

        this.hasLoadError = true;
      }
    },

    async save() {
      this.saving = true;
      this.saveError = '';

      const token = this.$store.state.auth.token;

      if (!this.$refs.form.validate()) {
        return;
      }

      try {
        let newUrl;

        if (this.id) {
          newUrl = {
            id: this.id,
            slug: this.slug,
            redirect: this.redirect,
            description: this.description,
            active: this.active,
          };

          await updateURL(
            token,
            {
              id: this.id,
              slug: this.slug,
              redirect: this.redirect,
              description: this.description,
              active: this.active,
            }
          );

          newUrl.views = this.views;
        } else {
          const data = await createURL(
            token,
            {
              slug: this.slug,
              redirect: this.redirect,
              description: this.description,
            }
          );

          newUrl = data.data;
          newUrl.views = 0;
        }

        this.$store.commit(UpdateURL, newUrl);
        this.show = false;
        this.$router.push('/');
      } catch(e) {
        console.error(e);
        const response = e.response;

        if (response && response.status == 400) {
          this.saveError = response.data.error;
        } else {
          this.saveError = 'A network error has occurred. Please try again.';
        }
      }
    }
  },

  watch: {
    '$route' (to, from) {
      this.begin();
    }
  }
}
</script>