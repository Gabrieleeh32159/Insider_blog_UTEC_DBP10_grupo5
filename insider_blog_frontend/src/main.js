import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./components/axios.js";
import store from "./vuex";
import "bootstrap/dist/css/bootstrap.min.css";
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'

createApp(App).use(router).use(store).mount("#app");
