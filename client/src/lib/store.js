'use strict';

import Vue from 'vue'
import Vuex from 'vuex';

import { getAuthData, logout } from './auth'

Vue.use(Vuex)

export const SetAuth = 'SetAuth';
export const LogOut = 'LogOut';

export const SetURLs = 'SetURLs';
export const AddURLs = 'AddURLs';
export const UpdateURL = 'UpdateURL';
export const SetURLToEdit = 'SetURLToEdit';

const store = new Vuex.Store({
    state:{
        auth: getAuthData(),
        urls: {},
    },
    
    mutations: {
        [SetAuth](state, payload) {
            state.auth = payload;
        },

        [LogOut](state) {
            state.auth = getAuthData();
        },

        [SetURLs](state, rows) {
            state.urls = {};
            rows.forEach(row => Vue.set(state.urls, row.id, row));
        },

        [AddURLs](state, rows) {
            rows.forEach(row => Vue.set(state.urls, row.id, row));
        },

        [UpdateURL](state, url) {
            console.log(url);
            Vue.set(state.urls, url.id, url);
        },
    },

    strict: true,
});

export default store;