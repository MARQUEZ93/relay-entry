<script>
import api from '@/services/api';
import WaiverComponent from '@/components/registration/WaiverComponent.vue';
import RacerDataComponent from '@/components/registration/RacerData.vue';
import CheckoutComponent from '@/components/registration/CheckoutComponent.vue';
import { loadStripe } from '@stripe/stripe-js';
import { formattedRaceDate, customSameDistance } from '@/utils/methods';

export default {
  components: {
    WaiverComponent,
    RacerDataComponent,
    CheckoutComponent,
  },
  provide() {
    return {
      stripe: this.stripePromise,
    };
  },
  data() {
    return {
      race: {},
      stripePromise: null,
      racerData: {},
      racerDataComplete: false, // Add this line
      waiverAccepted: false,
      paymentCompleted: false,
      loading: true,
      error: null,
      activeTab: 0,
    };
  },
  computed: {
    tabLabel() {
      return this.race.is_relay ? 'Team Captain' : 'Registrant';
    },
  },
  methods: {
    customSameDistance,
    formattedRaceDate,
    updateWaiverAccepted(accepted) {
      this.waiverAccepted = accepted;
    },
    async fetchRace(eventSlug, raceId) {
      try {
        const response = await api.getRace(eventSlug, raceId);
        this.race = response.data;
        console.log("fetchRace");
        console.log(response.data);
        this.loading = false;
      } catch (error) {
        console.log(error);
        this.error = 'Error fetching race details.';
        this.loading = false;
      }
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    },
    goToEventPage() {
      this.$router.push({ name: 'Event', params: { eventUrlAlias: this.race.event.url_alias } });
    },
    selectTab(tabIndex) {
      if (tabIndex <= this.activeTab && (tabIndex === 0 || this.racerDataComplete)) {
        this.activeTab = tabIndex;
      }
    },
    nextTab() {
      if (this.activeTab < 2 && (this.activeTab === 0 || this.racerDataComplete)) {
        this.activeTab += 1;
      }
    },
    previousTab() {
      if (this.activeTab > 0) {
        this.activeTab -= 1;
      }
    },
    saveRacerData(data) {
      this.racerData = data;
      this.racerDataComplete = true; // Add this line
      this.waiverAccepted = false; // Reset waiverAccepted when racerData is edited
      this.nextTab();
    },
    acceptWaiver() {
      this.waiverAccepted = true;
      this.nextTab();
    },
    async submitData() {
      try {
        const response = await api.submitRegistration({
          waiverAccepted: this.waiverAccepted,
          racerData: this.racerData,
        });
        console.log('Registration successful:', response.data);
      } catch (error) {
        console.error('Error submitting registration:', error);
      }
    },
  },
  async created() {
    const eventSlug = this.$route.params.url_alias;
    const raceId = this.$route.params.id;
    await this.fetchRace(eventSlug, raceId);

    try{
      // this.stripePromise = loadStripe(process.env.STRIPE_PUBLISHABLE_KEY);
      this.stripePromise = loadStripe("pk_test_51PNivYBsh8Ne4MdUVijN6hN4Ueoo8vLEFj5o5BqkAinexlV7S2f7P2EufuWHpqIR9SAAdZF5lpvk2kgHDFzTeuOQ009WWgftkv");
      this.stripePromise.then(stripe => {
      if (stripe) {
        console.log('Stripe instance loaded successfully');
      } else {
        console.error('Failed to load Stripe instance');
      }
      });
    } catch (error) {
      // TODO: not allowed on prod
      console.error('Error loading Stripe:', error);
    }
  },
};
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-btn color="primary" @click="goToEventPage">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Event Page
        </v-btn>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="race">
      <v-col cols="12" md="8">
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-img v-if="race && race.event && race.event.logo" style="width: 50%; height: auto; margin:auto;" :src="race.event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title v-if="race.event" class="text-center">
            <h1 class="text-h4">{{ race.name }}</h1>
            <h2 class="text-h5">{{ race.event.name }}</h2>
            </v-card-title>
          <v-card-subtitle v-if="race.description">
            <p class="text-center">{{ race.description }}</p>
          </v-card-subtitle>
          <v-card-subtitle>
            <p class="text-center"><strong>Time:</strong> {{ formattedRaceDate(race.date) }}</p>
          </v-card-subtitle>
          <v-card-subtitle>
            <p class="text-center"><strong>Price:</strong> ${{ formatPrice(race.price) }}</p>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="race">
      <v-col cols="12" md="8">
        <v-tabs v-model="activeTab">
          <v-tab :key="0" @click="selectTab(0)">
            <v-icon left>mdi-account</v-icon>
            {{ tabLabel }}
          </v-tab>
          <v-tab :key="1" :disabled="!racerDataComplete" @click="selectTab(1)">
            <v-icon left>mdi-file-document</v-icon>
            Waiver
          </v-tab>
          <v-tab :key="2" :disabled="!racerDataComplete || !waiverAccepted" @click="selectTab(2)">
            <v-icon left>mdi-credit-card</v-icon>
            Checkout
          </v-tab>
        </v-tabs>

        <div v-if="activeTab === 0">
          <RacerDataComponent :racerData="racerData" :race="race" @complete="saveRacerData" />
        </div>
        <div v-if="activeTab === 1">
          <WaiverComponent :initialAccepted="waiverAccepted" :race="race" @complete="acceptWaiver" @update-accepted="updateWaiverAccepted"/>
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="nextTab" color="primary" class="mt-3">Next</v-btn>
        </div>
        <div v-if="activeTab === 2">
          <CheckoutComponent :waiverAccepted="waiverAccepted" :race="race" :racerData="racerData" @complete="submitData" :stripePromise="stripePromise"/>
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="submitData" color="primary" class="mt-3">Submit</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
  .v-btn {
    margin: 0 5px;
  }
</style>
