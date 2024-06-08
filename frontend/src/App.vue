<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <router-link to="/" class="white--text">
        <v-toolbar-title>RelayEntry</v-toolbar-title>
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

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer app color="primary" dark>
      <v-col class="text-center" cols="12">
        &copy; 2024 RelayEntry
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
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
</style>
