import { createApp, VueElement } from "vue";
import App from "./App.vue";
import router from "./router";
import './components/axios.js'
import store from './vuex'
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

createApp(App).use(router).use(store).mount("#app");
