<script>
import brandLogo from '@/assets/logo.svg';
import api from '@/services/api';
export default {
  name: 'App',
  mounted() {
    api.fetchCsrfToken();
  },
  provide() {
    return {
      showSnackbar: this.showSnackbar,
    };
  },
  methods: {
    showSnackbar(message, color = 'success', timeout = 5000) {
      this.snackbar.message = message;
      this.snackbar.color = color;
      this.snackbar.timeout = timeout;
      this.snackbar.show = true;
    },
  },
  data() {
    return {
      drawer: false,
      brandLogo,
      snackbar: {
        show: false,
        message: '',
        color: 'success',
        timeout: 5000,
      },
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
      <router-link to="/contact" class="white--text" v-if="$vuetify.display.mdAndUp">
        <v-btn text class="white--text">Contact</v-btn>
      </router-link>
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
        <router-link to="/contact" @click="drawer = false">
          <v-list-item>
            <v-list-item-title>Contact</v-list-item-title>
          </v-list-item>
        </router-link>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>
     <!-- Snackbar -->
     <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
      {{ snackbar.message }}
      <template v-slot:action>
        <v-btn color="white" text @click="snackbar.show = false">Close</v-btn>
      </template>
    </v-snackbar>
    <v-footer app color="primary" dark>
      <v-row>
        <v-col cols="12">
          <v-typography variant="subtitle-1">&copy; 2024 RelayEntry - Alpha 2.1.2 (Early Access)</v-typography>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>
<style>
  .v-main {
    --v-layout-top: 8px !important;  /* Reduce the top offset globally */
  }
  #app {
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: black;
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
  .prevent-overflow{
    white-space: normal;
    overflow: visible;
    text-overflow: initial;
  }
  .social-icons {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }

  .social-icons .v-btn {
    margin: 0 10px;
  }

  .social-icons .v-icon {
    font-size: 30px;
  }

  .facebook-icon {
    color: #3b5998;
    background-color: #e9ebee;
    border-radius: 50%;
  }

  .instagram-icon {
    color: #e1306c;
    background-color: #f7f7f7;
    border-radius: 50%;
  }

  .twitter-icon {
    color: #1da1f2;
    background-color: #e8f5fd;
    border-radius: 50%;
  }

  .email-icon {
    color: #ea4335;
    background-color: #fce8e6;
    border-radius: 50%;
  }

  .website-icon {
    color: #4285f4;
    background-color: #e8f0fe;
    border-radius: 50%;
  }
</style>