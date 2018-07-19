import Vuex from 'vuex';

export default new Vuex.Store({
    state:{
        login: {
            loggedIn: false,
            userName: '',
        }
    },
    
    mutations: {

    },

    strict: true,
});