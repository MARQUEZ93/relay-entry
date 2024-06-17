import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify'; // Import the Vuetify setup
import store from './store'; // Import the store
import '@mdi/font/css/materialdesignicons.css'; // Import MDI CSS

const app = createApp(App);

app.use(vuetify); // Use Vuetify
app.use(router); // Use the router
app.use(store); // Use the store

app.mount('#app'); // Mount the app
