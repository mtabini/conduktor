import Vue from 'vue'
import Router from 'vue-router'

import MainDisplay from '../components/MainDisplay';
import UrlEdit from '../components/UrlEdit';

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MainDisplay',
      component: MainDisplay,
      
      children: [
        {
          path: 'new',
          component: UrlEdit,
        },

        {
          path: 'edit/:id',
          component: UrlEdit,
        },
      ],
    },
  ]
})
