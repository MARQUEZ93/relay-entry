<script>
  import api from '@/services/api';
  
  export default {
    name: 'DashboardComponent',
    inject: ['showSnackbar'],
    data() {
      return {
        message: '',
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
    </v-container>
</template>

  