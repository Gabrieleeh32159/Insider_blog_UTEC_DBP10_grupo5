import Vuex from "vuex";

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
    },
  },
  actions: {
    user(context, user) {
      context.commit("user", user);
    },
    posts(context, posts) {
        context.commit("posts", posts);
    }
  },
  mutations: {
    user(state, user) {
      state.user = user;
    },
    posts(state, posts) {
      state.posts = posts;
    },
  },
});

export default store;
