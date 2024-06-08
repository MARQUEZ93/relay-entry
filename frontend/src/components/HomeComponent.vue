<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>RelayEntry</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text>Home</v-btn>
      <v-btn text>About</v-btn>
      <v-btn text>Contact</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col>
            <h1>Welcome to RelayEntry</h1>
            <p>Your ultimate solution for race registrations.</p>
            <!-- Add more content here as needed -->
          </v-col>
        </v-row>
      </v-container>
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
  name: 'HomeComponent',
};
</script>

<style scoped>
h1 {
  color: #2c3a50;
  margin-top: 20px;
}

p {
  font-size: 1.2em;
  color: #4caf50;
}

.v-app-bar {
  background-color: #4caf50;
}

.v-footer {
  background-color: #4caf50;
  padding: 10px;
}
</style>

