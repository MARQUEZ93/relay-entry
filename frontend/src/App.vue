<script>
import brandLogo from '@/assets/logo.svg';
import api from '@/services/api';
export default {
  name: 'App',
  mounted() {
    api.fetchCsrfToken();
  },
  data() {
    return {
      drawer: false,
      brandLogo,
    };
  },
};
</script>
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <router-link to="/">
        <v-img :src="brandLogo" alt="RelayEntry Logo" class="logo-image ml-5"></v-img>
      </router-link>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon class="mr-5" @click="drawer = !drawer" v-if="!$vuetify.display.mdAndUp"></v-app-bar-nav-icon>
      <router-link to="/" class="white--text" v-if="$vuetify.display.mdAndUp">
        <v-btn text class="white--text">Home</v-btn>
      </router-link>
      <router-link to="/about" class="white--text" v-if="$vuetify.display.mdAndUp">
        <v-btn text class="white--text">About</v-btn>
      </router-link>
      <router-link to="/pricing" class="white--text" v-if="$vuetify.display.mdAndUp">
        <v-btn text class="white--text">Pricing</v-btn>
      </router-link>
      <v-btn text href="mailto:relayentry@gmail.com" class="white--text" v-if="$vuetify.display.mdAndUp">Contact</v-btn>
    </v-app-bar>

    <v-navigation-drawer app v-model="drawer" color="primary" dark v-if="!$vuetify.display.mdAndUp">
      <v-list dense>
        <router-link to="/" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>
        </router-link>
        <router-link to="/about" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item>
        </router-link>
        <router-link to="/pricing" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Pricing</v-list-item-title>
          </v-list-item>
        </router-link>
        <a href="mailto:relayentry@gmail.com" @click="drawer = false">
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
      <v-row>
        <v-col cols="6">
          <v-typography variant="subtitle-1">&copy; 2024 RelayEntry. All rights reserved.</v-typography>
        </v-col>
        <v-col cols="6">
          <v-typography variant="subtitle-1">Alpha 1.0.3 (Early Access)</v-typography>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>
<style>
#app {
  font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  margin-bottom: 0;
}
@media only screen and (max-width: 600px) {
  .logo-image, .footer-logo {
    width: 110px;
    height: 110px;
  }
}
.white--text {
  color: white !important;
}
.footer-logo{
  height: 220px;
  width: 220px;
}
.logo-image {
  height: 220px;
  width: 220px;
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