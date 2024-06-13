<template>
    <v-container>
      <v-row class="justify-center">
        <v-col cols="12" md="8" class="text-center">
          <h1>Page Not Found</h1>
          <p>The page you are looking for does not exist.</p>
          <router-link to="/">
            <v-btn color="primary" class="go-home-btn">Go to Home</v-btn>
          </router-link>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'NotFound',
  };
  </script>
  
  <style scoped>
  h1 {
    font-size: 3rem;
    margin-top: 20px;
  }
  
  p {
    font-size: 1.5rem;
  }
  
  .go-home-btn {
    margin-top: 20px; /* Adjust the margin as needed */
    padding: 10px 20px; /* Optional: Adjust the padding for better spacing */
  }
  </style>
  