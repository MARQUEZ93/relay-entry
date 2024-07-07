<template>
    <v-container>
      <v-row>
        <v-col>
          <v-card class="mx-auto my-5 pa-5" max-width="800">
            <v-card-title>
              <h1>{{ race.name }}</h1>
            </v-card-title>
            <v-card-subtitle v-if="race.description">
              <p>{{ race.description }}</p>
            </v-card-subtitle>
            <v-card-subtitle>
              <p><strong>Date:</strong> {{ race.date }} </p>
            </v-card-subtitle>
            <v-card-subtitle>
              <p><strong>Time:</strong> {{ race.hour }} : {{ race.minute }} {{ race.time_indicator }}</p>
            </v-card-subtitle>
            <v-card-subtitle>
              <p><strong>Price:</strong> ${{ formatPrice(race.price) }}</p>
            </v-card-subtitle>
            <!-- Add more details as needed -->
            <v-card-actions class="justify-center">
              <v-btn color="primary">Register</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    name: 'RaceComponent',
    data() {
      return {
        race: {},
        loading: true,
        error: null,
      };
    },
    methods: {
      formatPrice(price) {
        return parseFloat(price).toFixed(2);
      },
      async fetchRace(eventSlug, raceId) {
        try {
          const response = await api.getRace(eventSlug, raceId);
          this.race = response.data;
          this.loading = false;
        } catch (error) {
          this.error = 'Error fetching race details.';
          this.loading = false;
        }
      }
    },
    async created() {
      const eventSlug = this.$route.params.url_alias;
      const raceId = this.$route.params.id;
      // Check if the race data is already passed through props or state
      if (this.$route.params.race) {
        this.race = this.$route.params.race;
        this.loading = false;
      } else {
        await this.fetchRace(eventSlug, raceId);
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
  
  .v-btn {
    margin: 0 5px;
  }
  </style>
  