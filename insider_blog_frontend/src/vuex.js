import Vuex, { Store } from 'vuex'

const state = {
    user: null,
    posts: null,
};

const store = new Vuex.Store({
    state,
    getters: {
        user: (state) => {
            return state.user;
        },
        posts: (state) => {
            return state.posts;
        } 
    },
    actions:{
        user(context, user){
            context.commit('user', user);
        }
    },
    mutations: {
        user(state, user){
            state.user = user;
        },
        posts(state, posts){
            state.posts = posts;
        }
    }
});

export default store;