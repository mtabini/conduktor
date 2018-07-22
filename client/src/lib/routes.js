import Vue from 'vue'
import Router from 'vue-router'

import MainDisplay from '../components/MainDisplay';
import UrlEdit from '../components/UrlEdit';
import UrlLogList from '../components/UrlLogList';

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MainDisplay',
      component: MainDisplay,
      props: (route) => ({
        search: route.query.search,
      }),
      
      children: [
        {
          name: 'newUrl',
          path: 'new',
          component: UrlEdit,
          props: { urlId: 0 },
        },

        {
          name: 'editUrl',
          path: 'edit/:urlId',
          component: UrlEdit,
          props: (route) => ({
            urlId: Number(route.params.urlId),
          }),
        },

        {
          name: 'viewUrlLogs',
          path: 'logs/:urlId',
          component: UrlLogList,
          props: (route) => ({
            urlId: Number(route.params.urlId),
          }),
        },
      ],
    },
  ]
})
