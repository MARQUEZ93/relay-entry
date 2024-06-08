<template>
    <v-container>
      <v-row>
        <v-col>
          <h1>Event: {{ event.name }}</h1>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    name: 'EventComponent',
    data() {
      return {
        event: {},
      };
    },
    async created() {
      const eventId = this.$route.params.id;
      try {
        const response = await api.getEvent(eventId);
        console.log(response);
        this.event = response.data;
      } catch (error) {
        console.log(error);
        console.error('Error fetching event:', error);
      }
    },
  };
  </script>
  
  <style scoped>
  h1 {
    color: #2c3e50;
    margin-top: 20px;
  }
  
  p {
    font-size: 1.2em;
    color: #2c3e50;
  }
  </style>
  