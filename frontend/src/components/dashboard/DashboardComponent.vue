<script>
  import api from '@/services/api';
  
  export default {
    name: 'DashboardComponent',
    inject: ['showSnackbar'],
    data() {
      return {
        message: '',
        username: '',
        email: '',
      };
    },
    methods: {
      logout() {
        api.logout();
        this.$router.push('/');
      },
    },
    async created() {
      try {
        const response = await api.dashboard();
        this.message = response.data.message;
        this.username = response.data.username;
        this.email = response.data.email;
      } catch (error) {
        this.showSnackbar('Session expired. Log in again.', 'error');
        api.logout();
        this.$router.push('/login');
      }
    },
  };
  </script>
<template>
    <v-container>
        <h2>RelayEntry Dashboard</h2>
        <p>{{ message }}</p>
        <v-btn @click="logout" text>Logout</v-btn>

        <v-row>
          <v-col
            cols="6"
            md="4"
            class="d-flex align-center justify-center"
          >
            <v-card class="mx-auto my-3 race-card" outlined>
              <router-link :to="`/dashboard/create-event/`">
                <v-card-title class="d-flex align-center justify-center">
                  <span>Create Event</span>
                </v-card-title>
              </router-link>
            </v-card>
          </v-col>
        </v-row>
        
    </v-container>
</template>

  