<template>
  <v-container fluid fill-height class="grey lighten-4">
    <v-layout justify-center align-center>
      <v-flex shrink>
        <v-jumbotron>
          <v-container fill-height>
            <v-layout align-center>
              <v-flex>
                <h3 class="display-3">Welcome to {{ title }}</h3>

                <span class="subheading">You must sign in with Google before being able to use this app.</span>

                <v-divider class="my-3"></v-divider>

                <p class="subheading error">{{ error }}</p>

                <g-signin-button
                  :params="googleSignInParams"
                  @success="onSignInSuccess"
                  @error="onSignInError">
                  Sign in with Google
                </g-signin-button>
              </v-flex>
            </v-layout>
          </v-container>
        </v-jumbotron>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { extractAuthData } from '../lib/auth';
import { SetAuth } from '../lib/store';

export default {
  name: 'Login',

  data () {
    return {
      title: window.ConduktorConfig ? window.ConduktorConfig.APP_TITLE : process.env.APP_TITLE,
      error: null,
      
      googleSignInParams: {
        client_id:  window.ConduktorConfig ? window.ConduktorConfig.GOOGLE_OAUTH_CLIENT_ID : process.env.GOOGLE_OAUTH_CLIENT_ID,
      },
    }
  },

methods: {
    onSignInSuccess (googleUser) {
      try {
        const authData = extractAuthData(googleUser);
        this.$data.error = null;
        this.$store.commit(SetAuth, authData);
      } catch(e) {
        if (e.error != 'popup_closed_by_user') {
          this.$data.error = e.message;
        }
      }
    },

    onSignInError (error) {
      if (error.error != 'popup_closed_by_user') {
        this.$data.error = error;
      }
    },
  },
}
</script>

<style>
.g-signin-button {
  cursor: pointer;
  display: inline-block;
  padding: 4px 8px;
  border-radius: 3px;
  background-color: #3c82f7;
  color: #fff;
  box-shadow: 0 3px 0 #0f69ff;
}
</style>