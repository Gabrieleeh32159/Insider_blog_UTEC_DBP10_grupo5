import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    //component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/newpost",
    name: "newpost",
    component: () => import("../views/NewPostView.vue"),
  },
  {
    path: "/group/:slug",
    name: "Groups",
    props: true,
    component: () => import("../views/GroupView.vue"),
  },
  {
    path: "/user/:slug",
    name: "Users",
    props: true,
    component: () => import("../views/UserView.vue"),
  },
  {
    path: "/post/:slug",
    name: "Posts",
    props: true,
    component: () => import("../views/PostView.vue"),
  },
  {
    path: "/newgroup",
    name: "newgroup",
    component: () => import("../views/NewGroupView.vue"),
  },
  {
    path: "/joingroup",
    name: "joingroup",
    component: () => import("../views/JoinGroupView.vue"),
  },
  {
    path: "/edit/:slug",
    name: "edit",
    props: true,
    component: () => import("../views/EditView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
