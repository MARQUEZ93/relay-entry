<script>
import api from '@/services/api';
import WaiverComponent from '@/components/registration/WaiverComponent.vue';
import RegistrationData from '@/components/registration/RegistrationData.vue';
import CheckoutComponent from '@/components/registration/CheckoutComponent.vue';
import { formattedRaceDate, customSameDistance, formatMinute } from '@/utils/methods';
import { loadStripe } from '@stripe/stripe-js';

export default {
  components: {
    WaiverComponent,
    RegistrationData,
    CheckoutComponent,
  },
  data() {
    return {
      race: {},
      clientSecret: '',
      stripe: null,
      registrationData: {},
      teamData: {},
      racerDataComplete: false,
      waiverAccepted: false,
      ipAddress: '',
      paymentCompleted: false,
      loading: true,
      error: null,
      activeTab: 0,
    };
  },
  computed: {
    participantLabel() {
      return this.race.is_relay ? 'Team Captain' : 'Registrant';
    },
  },
  methods: {
    async initStripe() {
      if (!window.Stripe) {
        // Ensure Stripe.js is loaded from the global scope
        await new Promise((resolve) => {
          // Fallback in case the script hasn't loaded yet
          const script = document.createElement('script');
          script.src = 'https://js.stripe.com/v3/';
          script.async = true;
          script.onload = resolve;
          document.head.appendChild(script);
        });
      }
      this.stripe = await loadStripe("pk_test_51PNivYBsh8Ne4MdUVijN6hN4Ueoo8vLEFj5o5BqkAinexlV7S2f7P2EufuWHpqIR9SAAdZF5lpvk2kgHDFzTeuOQ009WWgftkv");
      console.log("stripe loading");
    },
    async createPaymentIntentOnMount() {
      try {
        const response = await api.createPaymentIntent({
          raceId: this.race.id
        })
        this.clientSecret = response.data.clientSecret;
        console.log("createPaymentIntentOnMount done");
        this.loading = false;
      } catch (e) {
        this.showError('Payment gateway error. Please try again later.');
      }
    },
    customSameDistance,
    formattedRaceDate,
    formatMinute,
    updateWaiverAccepted(accepted) {
      this.waiverAccepted = accepted;
    },
    updateIpAddress(ipAddress) {
      this.ipAddress = ipAddress;
      this.registrationData.ipAddress = ipAddress;
      console.log(this.registrationData);
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
    saveRegistrationData(registrationData, teamData={}) {
      this.registrationData = registrationData;
      this.teamData = teamData;
      this.racerDataComplete = true;
      this.waiverAccepted = false; // Reset waiverAccepted when registrationData is edited
      this.ipAddress = ''; // Reset waiverAccepted when registrationData is edited
      this.nextTab();
    },
    acceptWaiver() {
      this.waiverAccepted = true;
      this.nextTab();
    },
    async submitData() {
      try {
        console.log("submitData");
      } catch (error) {
        console.log("error");
      }
    },
  },
  async created() {
    const eventSlug = this.$route.params.url_alias;
    const raceId = this.$route.params.id;
    await this.fetchRace(eventSlug, raceId);
    await this.createPaymentIntentOnMount();
    await this.initStripe();
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
          <v-card-subtitle v-if="race.is_relay && race.same_distance">
            <p v-if="race.custom_distance_value && race.custom_distance_unit">
              {{race.num_runners }} x {{customSameDistance(race)}}
            </p>
          </v-card-subtitle>
          <v-card-subtitle>
              <p>{{ race.hour }}:{{ formatMinute(race.minute) }} {{ race.time_indicator }} </p>
          </v-card-subtitle>
          <v-card-subtitle>
            <p class="text-center">{{ formattedRaceDate(race.date) }}</p>
          </v-card-subtitle>
          <v-card-subtitle v-if="race.is_relay">
            <p class="text-center"><strong>${{ formatPrice(race.price) }} per Team</strong></p>
          </v-card-subtitle>
          <v-card-subtitle v-if="!race.is_relay">
            <p class="text-center"><strong>${{ formatPrice(race.price) }}</strong></p>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="race">
      <v-col cols="12" md="8">
        <v-tabs v-model="activeTab">
          <v-tab :key="0" @click="selectTab(0)">
            <v-icon left>mdi-account</v-icon>
            {{ participantLabel }}
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
          <RegistrationData :registrationData="registrationData" :race="race" @complete="saveRegistrationData" />
        </div>
        <div v-if="activeTab === 1">
          <WaiverComponent :initialAccepted="waiverAccepted" :race="race" @complete="acceptWaiver" @update-accepted="updateWaiverAccepted" @get-ip="updateIpAddress"/>
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="nextTab" color="primary" class="mt-3">Next</v-btn>
        </div>
        <div v-if="activeTab === 2">
          <CheckoutComponent :stripe="stripe" :clientSecret="clientSecret" :waiverAccepted="waiverAccepted" :race="race" :registrationData="registrationData"/>
          <v-btn style="float:left;" @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
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
