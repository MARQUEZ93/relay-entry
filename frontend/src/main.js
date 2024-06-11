import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify'; // Import the Vuetify setup
import '@mdi/font/css/materialdesignicons.css'; // Import MDI CSS

const app = createApp(App);

app.use(vuetify); // Use Vuetify
app.use(router); // Use the router

app.mount('#app'); // Mount the app
