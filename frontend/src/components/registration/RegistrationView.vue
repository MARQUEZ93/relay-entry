<script>
import api from '@/services/api';
import WaiverComponent from '@/components/registration/WaiverComponent.vue';
import RegistrationData from '@/components/registration/RegistrationData.vue';
import CheckoutComponent from '@/components/registration/CheckoutComponent.vue';
import { formattedRaceDate, customSameDistance, formatMinute } from '@/utils/methods';
import { loadStripe } from '@stripe/stripe-js';

export default {
  inject: ['showSnackbar'],
  components: {
    WaiverComponent,
    RegistrationData,
    CheckoutComponent,
  },
  async mounted() {
    window.scrollTo(0, 0);
  },
  data() {
    return {
      paymentElementContainer: null,
      race: {},
      clientSecret: '',
      paymentIntentId: '',
      amount: '',
      stripe: null,
      elements: null, 
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
      this.stripe = await loadStripe(process.env.VUE_APP_STRIPE_PUBLISHABLE_KEY);
      if (this.clientSecret){
        const options = {
          clientSecret: this.clientSecret,
          loader: 'auto',
        };
        // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in a previous step
        this.elements = await this.stripe.elements(options);
        // Create and mount the Payment Element
        this.paymentElement = await this.elements.create('payment');
        // Create a container div for the payment element
        this.paymentElementContainer = await document.createElement('div');
        this.paymentElementContainer.id = 'payment-element-container';

        // Mount the Payment Element to the container div
        await this.paymentElement.mount(this.paymentElementContainer);
      }
    },
    async createPaymentIntentOnMount() {
      try {
        const response = await api.createPaymentIntent({
          raceId: this.race.id
        })
        this.clientSecret = response.data.clientSecret;
        this.paymentIntentId = response.data.id;
        this.amount = response.data.amount;
        this.loading = false;
      } catch (e) {
        this.showSnackbar('Payment gateway error. Please try again later.', 'error');
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
    },
    async fetchRace(eventSlug, raceId) {
      try {
        const response = await api.getRace(eventSlug, raceId);
        this.race = response.data;
        if ((this.race && this.race.registration_closed) || (this.race && this.race.event && this.race.event.registration_closed)){
          this.$router.push({ path: '/' });
        }
        this.loading = false;
      } catch (error) {
        this.error = 'Error fetching race details.';
        this.loading = false;
        this.$router.push({ path: '/' });
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
      <v-col cols="10">
        <v-card class="mx-auto my-5 pa-5">
          <v-img v-if="race && race.event && race.event.logo" :alt="`Event logo for ${race.event.name}`" :src="race.event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title v-if="race.event" class="text-center race-name">
            {{ race.name }}
          </v-card-title>
          <v-card-title v-if="race.event" class="text-center race-event-name">
            {{ race.event.name }}
          </v-card-title>
          <v-card-subtitle v-if="race.description" class="text-center">
            {{ race.description }}
          </v-card-subtitle>
          <v-card-subtitle v-if="race.is_relay && race.same_distance && race.custom_distance_value && race.custom_distance_unit">
            {{race.num_runners }} x {{customSameDistance(race)}}
          </v-card-subtitle>
          <v-card-subtitle>
            {{ race.hour }}:{{ formatMinute(race.minute) }} {{ race.time_indicator }}
          </v-card-subtitle>
          <v-card-subtitle class="text-center">
            {{ formattedRaceDate(race.date) }}
          </v-card-subtitle>
          <v-card-subtitle v-if="race.is_relay" class="text-center">
            <strong>${{ formatPrice(race.price) }} per Team</strong>
          </v-card-subtitle>
          <v-card-subtitle v-if="!race.is_relay" class="text-center">
            <strong>${{ formatPrice(race.price) }}</strong>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="race">
      <v-col cols="12">
        <v-tabs v-model="activeTab">
          <v-tab key="participantLabel-0-view" @click="selectTab(0)" class="tab-text">
            <v-icon left>mdi-account</v-icon>
            {{ participantLabel }}
          </v-tab>
          <v-tab key="waiver-1-view" :disabled="!racerDataComplete" @click="selectTab(1)" class="tab-text">
            <v-icon left>mdi-file-document</v-icon>
            Waiver
          </v-tab>
          <v-tab key="checkout-2-view" :disabled="!racerDataComplete || !waiverAccepted" @click="selectTab(2)" class="tab-text">
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
          <v-btn :disabled="!waiverAccepted" @click="nextTab" color="primary" class="mt-3">Next</v-btn>
        </div>
        <div v-if="activeTab === 2">
          <CheckoutComponent :elements="elements" :amount="amount" :paymentElementContainer="paymentElementContainer" :paymentIntentId="paymentIntentId" :stripe="stripe" :clientSecret="clientSecret" :waiverAccepted="waiverAccepted" :race="race" :registrationData="registrationData"/>
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
  .race-event-name {
    word-wrap: break-word;
    white-space: normal;
  }
  .race-name{
    font-size: 2.5rem;
  }
  @media (max-width: 600px) {
    .tab-text {
      font-size: 0.7rem; /* Adjust font size for mobile */
    }
  }
</style>
