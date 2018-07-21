<template>
  <v-dialog v-model="show" :persistent="true" width="800px">
    <v-card>
      <v-form v-model="canSubmit" ref="form">
        <v-card-title class="grey lighten-4 py-4 title">
          <span v-if="id == 0">Create URL</span>
          <span v-else>Update URL</span>
        </v-card-title>

        <v-container grid-list-sm class="pa-4">
            <v-layout row wrap>
              <v-flex xs12 align-center justify-space-between>
                <v-alert :value="errorMessage != ''" :dismissible="true" type="error">
                  {{ errorMessage }}
                </v-alert>
              </v-flex>
              <v-flex xs12 align-center justify-space-between>
                <v-text-field
                  v-model="slug"
                  placeholder="Slug"
                  required
                  :rules="[() => validateRequiredField(slug), validateSlug]"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 align-center justify-space-between>
                <v-text-field
                  v-model="redirect"
                  placeholder="Redirect to"
                  required
                  :rules="[() => validateRequiredField(redirect), validateRedirect]"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 align-center justify-space-between>
                <v-text-field
                  v-model="description"
                  placeholder="Description"
                  required
                  :rules="[() => validateRequiredField(description)]"
                ></v-text-field>
              </v-flex>
            </v-layout>
        </v-container>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="show = false">Cancel</v-btn>
          <v-btn flat v-if="id != 0" :disabled="!canSubmit" @click.stop="save()">Update</v-btn>
          <v-btn flat v-else :disabled="!canSubmit" @click.stop="save()">Create</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
import { createURL, updateURL } from '../lib/api';
import { UpdateURL } from '../lib/store';
import { mapState } from 'vuex';

export default {
  name: 'UrlEdit',
  data: () => ({
    show: false,
    canSubmit: false,
    errorMessage: '',
    id: 0,
    slug: '',
    redirect: '',
    description: '',
    active: true,
  }),
  methods: {
    toggle(urlId) {
      if (urlId) {
        const url = this.$store.state.urls[urlId];

        this.id = url.id;
        this.slug = url.slug;
        this.redirect = url.redirect;
        this.description = url.description;
        this.active = url.active;
      } else {
        this.id = 0;
        this.slug = '';
        this.redirect = '';
        this.description = '';
        this.active = true;
      }

      this.errorMessage = '';
      this.show = true;
    },
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
    async save() {
      this.errorMessage = '';

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
          )
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
        }

        this.$store.commit(UpdateURL, newUrl);
        this.show = false;
      } catch(e) {
        console.error(e);
        const response = e.response;

        if (response && response.status == 400) {
          this.errorMessage = response.data.error;
        } else {
          this.errorMessage = 'A network error has occurred. Please try again.';
        }
      }
    }
  }
}
</script>