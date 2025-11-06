import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persistedstate';
// import Toast from "vue-toastification";
// import "vue-toastification/dist/index.css";
import App from './App.vue';
import router from '@/routers/router';
import '@/assets/styles/main.scss';

const pinia = createPinia();
pinia.use(piniaPersist);

const app = createApp(App);
app.use(pinia);
app.use(router);
// app.use(Toast);
app.mount('#app');
