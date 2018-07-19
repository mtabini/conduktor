'use strict';

import Vue from 'vue'
import Vuex from 'vuex';

import { getAuthData, logout } from './auth'

Vue.use(Vuex)

export const SetAuth = 'SetAuth';
export const LogOut = 'LogOut';

const store = new Vuex.Store({
    state:{
        auth: getAuthData(),
    },
    
    mutations: {
        [SetAuth](state, payload) {
            state.auth = payload;
        },

        [LogOut](state) {
            state.auth = getAuthData();
        }
    },

    strict: true,
});

export default store;