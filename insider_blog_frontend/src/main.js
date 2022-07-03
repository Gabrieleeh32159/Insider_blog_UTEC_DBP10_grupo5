import { createApp, VueElement } from "vue";
import App from "./App.vue";
import router from "./router";
import './components/axios.js'

import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

createApp(App).use(router).mount("#app");
