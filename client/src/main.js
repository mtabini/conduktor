// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'

import App from './App'
import router from './lib/routes'
import store from './lib/store'

Vue.use(Vuetify);
import 'vuetify/dist/vuetify.min.css' 

import GSignInButton from 'vue-google-signin-button'
Vue.use(GSignInButton)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
