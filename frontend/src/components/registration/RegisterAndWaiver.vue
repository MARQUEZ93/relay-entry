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
  data() {
    return {
      snackbar: {
        show: false,
        message: '',
        timeout: 8000
      },
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
    showError(message) {
      this.snackbar.message = message;
      this.snackbar.show = true;
    },
    updateIpAddress(ipAddress) {
      this.ipAddress = ipAddress;
      this.registrationData.ipAddress = ipAddress;
      console.log(this.registrationData);
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
    //   TODO: removed below
    //   this.nextTab();
    },
    async submit() {
      try {
        this.loading = true;
        const response = await api.registerForEvent(this.eventSlug, {
          eventId: this.event.id,
          registrationData: this.registrationData,
        });
        if (response.data.error) {
          this.loading = false; // Hide loader on error
          this.showError('An error occurred while processing your registration. Please try again later.');
        } else {
          const { registrationResponseData, eventData } = await response.data;
          console.log(registrationResponseData);
          console.log(eventData);
          this.$store.commit('setConfirmationData', {
            registrationData: registrationResponseData,
            eventData: eventData,
          });
          console.log(this.$store);
          this.loading = false;
          this.$router.push({ name: 'Confirmation' });
        }
      } catch (error) {
        this.loading = false;
        this.showError('An error occurred while processing your registration. Please try again later.');
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
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-img v-if="event && event.logo" style="width: 50%; height: auto; margin:auto;" :src="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title v-if="event" class="text-center">
            <h1 class="text-h4">{{ event.name }}</h1>
            </v-card-title>
          <v-card-text v-if="event.description">
            <p class="text-center">{{ event.description }}</p>
          </v-card-text>
          <v-card-subtitle>
            <p class="text-center">{{ formattedRaceDate(event.date) }}</p>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="event">
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
        </v-tabs>

        <div v-if="activeTab === 0">
          <RegistrationData :registrationData="registrationData" @complete="saveRegistrationData" />
        </div>
        <div v-if="activeTab === 1">
          <WaiverComponent :disabled="loading" :event="event" :initialAccepted="waiverAccepted" @complete="acceptWaiver" @update-accepted="updateWaiverAccepted" @get-ip="updateIpAddress"/>
          <v-btn @click="previousTab" color="secondary" class="mt-3 mr-3">Previous</v-btn>
          <v-btn @click="submit" color="primary" :disabled="!waiverAccepted" class="mt-3 mr-3">Submit</v-btn>
        </div>
        <!-- Snackbar for error messages -->
        <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" color="error">
          {{ snackbar.message }}
          <v-btn color="white" text @click="snackbar.show = false">Close</v-btn>
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
  .v-btn {
    margin: 0 5px;
  }
</style>
