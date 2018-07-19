<template>
  <v-dialog v-model="show" :persistent="true" width="800px">
    <v-card>
      <v-form v-model="canSubmit" ref="form">
        <v-card-title
          class="grey lighten-4 py-4 title"
        >
          <span v-if="id == 0">Create URL</span>
          <span v-else>Update URL</span>
        </v-card-title>
        <v-container grid-list-sm class="pa-4">
            <v-layout row wrap>
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
          <v-btn flat color="primary">More</v-btn>
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
import { createURL } from '../lib/api';

export default {
  name: 'UrlEdit',
  data: () => ({
    show: false,
    id: 0,
    slug: 'jira',
    redirect: 'https://noomhq.jira.com',
    description: 'For all tickets',
    active: false,
    canSubmit: false,
  }),
  methods: {
    toggle() {
      this.show = !this.show;
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
      if (!this.$refs.form.validate()) {
        return;
      }

      if (this.url) {
        return;
      }

      await createURL(
        this.$store.state.auth.token,
        {
          slug: this.slug,
          redirect: this.redirect,
          description: this.description,
        }
      );
    }
  }
}
</script>