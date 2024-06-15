<script>
import api from '@/services/api';
import WaiverComponent from '@/components/registration/WaiverComponent.vue';
import RacerDataComponent from '@/components/registration/RacerData.vue';
import CheckoutComponent from '@/components/registration/CheckoutComponent.vue';

export default {
  components: {
    WaiverComponent,
    RacerDataComponent,
    CheckoutComponent,
  },
  data() {
    return {
      race: {},
      racerData: {},
      waiverAccepted: false,
      paymentCompleted: false,
      loading: true,
      error: null,
      activeTab: 0,
    };
  },
  methods: {
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
    formattedRaceDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    },
    selectTab(tabIndex) {
      if (tabIndex <= this.activeTab) {
        this.activeTab = tabIndex;
      }
    },
    nextTab() {
      if (this.activeTab < 2) {
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
  },
};
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-card-title>
            <h1 class="text-h4 text-center">{{ race.name }}</h1>
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
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-tabs v-model="activeTab">
          <v-tab :key="0" @click="selectTab(0)">
            <v-icon left>mdi-account</v-icon>
            Registrant Data
          </v-tab>
          <v-tab :key="1" @click="selectTab(1)">
            <v-icon left>mdi-file-document</v-icon>
            Waiver
          </v-tab>
          <v-tab :key="2" @click="selectTab(2)">
            <v-icon left>mdi-credit-card</v-icon>
            Checkout
          </v-tab>
        </v-tabs>

        <div v-if="activeTab === 0">
          <RacerDataComponent :race="race" @complete="saveRacerData" />
        </div>
        <div v-if="activeTab === 1">
          <WaiverComponent :race="race" @complete="acceptWaiver" />
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="nextTab" color="primary" class="mt-3">Next</v-btn>
        </div>
        <div v-if="activeTab === 2">
          <CheckoutComponent :race="race" :racerData="racerData" @complete="submitData" />
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
