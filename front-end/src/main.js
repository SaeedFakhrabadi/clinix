import { createApp } from 'vue';

// Pinia
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persistedstate';

// Toast
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

import App from '@/App.vue';
import router from '@/routers';
import '@/assets/styles/main.scss';

const pinia = createPinia();
pinia.use(piniaPersist);

const app = createApp(App);
app.use(pinia);
app.use(router);
app.use(Toast);
app.mount('#app');
