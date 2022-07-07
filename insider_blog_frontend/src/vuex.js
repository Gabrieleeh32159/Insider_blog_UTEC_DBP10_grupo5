import Vuex from "vuex";

let state = {
  user: null,
  users: null,
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
    users: (state) => {
      return state.users;
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
    users(context, users) {
      context.commit("users", users);
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
    users(state, users) {
      state.users = users;
    },
  },
});

export default store;
