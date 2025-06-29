import { createApp } from 'vue'
import './styles/styles.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';

const app = createApp(App);

const pinia = createPinia();

app.use(pinia)

app.use(router)

app.mount('#app')
