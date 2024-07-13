<script>
import brandLogo from '@/assets/brand.svg';
import api from '@/services/api';
export default {
  name: 'App',
  mounted() {
    const response = api.fetchCsrfToken();
    console.log(response);
  },
  data() {
    return {
      drawer: false,
      brandLogo
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.white--text {
  color: white !important;
}
.logo-image {
  height: 130px; /* Adjust height as needed */
  width: 130px;
  max-width: 100%;
  display: block !important; /* Ensure the logo is displayed */
}
.v-navigation-drawer .v-list-item-title {
  font-weight: 500; /* Make the text bolder */
  text-transform: uppercase; /* Make the text all caps */
  color: white; /* Ensure the text color matches the header */
}
/* Remove underline from links */
.v-navigation-drawer a {
  text-decoration: none;
  color: inherit; /* Ensure the text color is inherited */
}

.v-navigation-drawer a:hover {
  text-decoration: underline;
}
</style>
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <router-link to="/">
        <v-img :src="brandLogo" alt="RelayEntry Logo" class="logo-image"></v-img>
      </router-link>
      <v-spacer></v-spacer>
      <router-link to="/" class="white--text">
        <v-btn text class="white--text">Home</v-btn>
      </router-link>
      <router-link to="/pricing" class="white--text">
        <v-btn text class="white--text">Pricing</v-btn>
      </router-link>
      <v-btn text href="mailto:contact@relayentry.com" class="white--text">Contact</v-btn>
    </v-app-bar>

    <v-navigation-drawer app v-model="drawer" color="primary" dark>
      <v-list dense>
        <router-link to="/" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>
        </router-link>
        <router-link to="/pricing" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Pricing</v-list-item-title>
          </v-list-item>
        </router-link>
        <a href="mailto:contact@relayentry.com" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Contact</v-list-item-title>
          </v-list-item>
        </a>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer app color="primary" dark>
      <v-col class="text-center" cols="12">
        &copy; 2024 RelayEntry - Alpha 1.0.0 (Early Access)
      </v-col>
    </v-footer>
  </v-app>
</template>