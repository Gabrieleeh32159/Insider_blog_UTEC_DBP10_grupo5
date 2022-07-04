import Vuex from "vuex";

const state = {
  user: null,
  posts: null,
  groups: null,
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
    groups: (state) => {
        return state.groups;
      },
  },
  actions: {
    user(context, user) {
      context.commit("user", user);
    },
    posts(context, posts) {
        context.commit("posts", posts);
    },
    groups(context, groups) {
        context.commit("groups", groups);
    },
  },
  mutations: {
    user(state, user) {
      state.user = user;
    },
    posts(state, posts) {
      state.posts = posts;
    },
    groups(state, groups) {
        state.groups = groups;
      },
  },
});

export default store;
