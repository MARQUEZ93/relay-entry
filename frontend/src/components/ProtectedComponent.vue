<script>
  import api from '@/services/api';
  
  export default {
    name: 'ProtectedComponent',
    data() {
      return {
        message: '',
      };
    },
    async created() {
      try {
        const response = await api.protected();
        this.message = response.data.message;
      } catch (error) {
        console.error(error);
        this.message = 'Error fetching protected data.';
      }
    },
  };
  </script>
<template>
    <v-container>
        <h2>Protected Page</h2>
        <p>{{ message }}</p>
    </v-container>
</template>

  