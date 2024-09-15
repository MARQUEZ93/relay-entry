<script>
  import api from '@/services/api';
  
  export default {
    name: 'LoginComponent',
    inject: ['showSnackbar'],
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          const response = await api.login(this.username, this.password);
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
          this.$router.push('/dashboard');
        } catch (error) {
          this.showSnackbar('Invalid username or password', 'error');
        }
      },
    },
  };
  </script>
<template>
    <v-container class="fill-height" fluid>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="4">
          <v-card>
            <v-card-title>
              <span class="headline">Login</span>
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="login">
                <v-text-field
                  v-model="username"
                  label="Username"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  required
                ></v-text-field>
                <v-btn type="submit" color="primary" block>Login</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <style scoped>
  .headline {
    font-weight: bold;
  }
  </style>
  