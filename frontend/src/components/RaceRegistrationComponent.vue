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
              <p><strong>Date:</strong> {{ formattedRaceDate(race.start_time) }}</p>
            </v-card-subtitle>
            <v-card-subtitle>
              <p><strong>Price:</strong> ${{ formatPrice(race.price) }}</p>
            </v-card-subtitle>
            <!-- Add more details as needed -->
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-stepper v-model="activeStep">
            <v-stepper-header>
              <v-stepper-step :complete="activeStep > 1" step="1">Waiver</v-stepper-step>
              <v-stepper-step :complete="activeStep > 2" step="2">Racer Data</v-stepper-step>
              <v-stepper-step :complete="activeStep > 3" step="3">Checkout</v-stepper-step>
            </v-stepper-header>
  
            <v-stepper-items>
                <v-stepper-content step="1">
                    <RacerDataComponent @next="nextStep" />
                </v-stepper-content>
                <v-stepper-content step="2">
                    <WaiverComponent @next="nextStep" @previous="previousStep" />
                </v-stepper-content>
                <v-stepper-content step="3">
                    <CheckoutComponent @previous="previousStep" />
                </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  import WaiverComponent from '@/components/WaiverComponent.vue';
  import RacerDataComponent from '@/components/RacerDataComponent.vue';
  import CheckoutComponent from '@/components/CheckoutComponent.vue';
  
  export default {
    components: {
        RacerDataComponent,
        WaiverComponent,
        CheckoutComponent,
    },
    data() {
      return {
        race: {},
        loading: true,
        error: null,
        activeStep: 1,
      };
    },
    methods: {
      formattedRaceDate(date) {
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
        return new Date(date).toLocaleDateString(undefined, options);
      },
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
      },
      nextStep() {
        this.activeStep += 1;
      },
      previousStep() {
        this.activeStep -= 1;
      },
    },
    async created() {
      const eventSlug = this.$route.params.url_alias;
      const raceId = this.$route.params.id;
      await this.fetchRace(eventSlug, raceId);
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
  