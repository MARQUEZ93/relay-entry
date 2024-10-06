<script>
import api from '@/services/api';
import WaiverComponent from '@/components/registration/WaiverComponent.vue';
import RegistrationData from '@/components/registration/RegistrationData.vue';
import { formattedRaceDate, customSameDistance, formatMinute } from '@/utils/methods';

export default {
  components: {
    WaiverComponent,
    RegistrationData,
  },
  inject: ['showSnackbar'],
  mounted() {
    window.scrollTo(0, 0);
  },
  data() {
    return {
      event: {},
      registrationData: {},
      racerDataComplete: false,
      waiverAccepted: false,
      ipAddress: '',
      loading: true,
      error: null,
      activeTab: 0,
      eventSlug: '',
    };
  },
  computed: {
    participantLabel() {
      return 'Registrant';
    },
  },
  methods: {
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
    async fetchEvent(eventSlug) {
      try {
        const response = await api.getEvent(eventSlug);
        this.event = response.data;
        this.loading = false;
      } catch (error) {
        this.error = 'Error fetching event details.';
        this.loading = false;
      }
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    },
    goToEventPage() {
      // this.eventSlug vs this.event.url_alias
      this.$router.push({ name: 'Event', params: { eventUrlAlias: this.eventSlug } });
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
    saveRegistrationData(registrationData) {
      this.registrationData = registrationData;
      this.racerDataComplete = true;
      this.waiverAccepted = false; // Reset waiverAccepted when registrationData is edited
      this.ipAddress = ''; // Reset waiverAccepted when registrationData is edited
      this.nextTab();
    },
    acceptWaiver() {
      this.waiverAccepted = true;
    },
    async submit() {
      try {
        this.loading = true;
        const response = await api.registerForEvent(this.eventSlug, {
          eventId: this.event.id,
          registrationData: this.registrationData,
        });
        const { registrationResponseData, eventData } = response.data;
        this.$store.commit('setConfirmationData', {
          registrationData: registrationResponseData,
          eventData: eventData,
        });
        this.loading = false;
        this.$router.push({ name: 'Confirmation' });
      } catch (e) {
        this.loading = false;
        let errorMessage = 'An error occurred while processing your registration: ';
        errorMessage += e.response.data.error;
        this.showSnackbar(errorMessage, 'error');
      }
    },
  },
  async created() {
    this.eventSlug = this.$route.params.url_alias;
    await this.fetchEvent(this.eventSlug);
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
    <v-row justify="center" v-if="event">
      <v-col cols="12" md="8">
        <v-card class="mx-auto my-5 pa-5">
          <v-img v-if="event && event.logo" :alt="`Event image for ${event.name}`" :src="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title v-if="event" class="text-center event-name">
            {{ event.name }}
          </v-card-title>
          <v-card-text v-if="event.description" class="text-center">
            {{ event.description }}
          </v-card-text>
          <v-card-subtitle class="text-center">
            {{ formattedRaceDate(event.date) }}
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="event">
      <v-col cols="12" md="8">
        <v-tabs v-model="activeTab">
          <v-tab key="participantLabel-0" @click="selectTab(0)" class="tab-text">
            <v-icon left>mdi-account</v-icon>
            {{ participantLabel }}
          </v-tab>
          <v-tab key="waiverLabel-1" :disabled="!racerDataComplete" @click="selectTab(1)" class="tab-text">
            <v-icon left>mdi-file-document</v-icon>
            Waiver
          </v-tab>
        </v-tabs>

        <div v-if="activeTab === 0">
          <RegistrationData :event="event" :raceField="true" :registrationData="registrationData" @complete="saveRegistrationData" />
        </div>
        <div v-if="activeTab === 1">
          <WaiverComponent :disabled="loading" :event="event" :initialAccepted="waiverAccepted" @complete="acceptWaiver" @update-accepted="updateWaiverAccepted" @get-ip="updateIpAddress"/>
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="submit" color="primary" :disabled="!waiverAccepted" class="mt-3 mr-3">Submit</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
  .v-btn {
    margin: 0 5px;
  }
  .event-name {
    font-size: 2.5rem;
    word-wrap: break-word;
    white-space: normal;
    overflow-wrap: break-word; 
  }
  @media (max-width: 600px) {
    .event-name {
      font-size: 2rem; /* Adjust the size as needed for mobile */
      word-break: keep-all; /* Prevents words from breaking up */
      white-space: normal; /* Allows normal wrapping */
    }
  }
</style>
