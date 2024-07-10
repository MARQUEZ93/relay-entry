<script>
import { mapState } from 'vuex';
export default {
  methods: {
    formatDate(dateStr) {
      const [year, month, day] = dateStr.split('-');
      const date = new Date(year, month - 1, day); // month is 0-based in JavaScript Date
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return date.toLocaleDateString('en-US', options);
    }
  },
  computed: {
    confirmationHeader(){
      if (this.teamData){
        return "Team Registration Successful";
      } else {
        return "Registration Successful"
      }
    },
    ...mapState({
      registrationData: state => state.registrationData,
      raceData: state => state.raceData,
      paymentData: state => state.paymentData,
      teamData: state => state.teamData,
      eventData: state => state.eventData,
    }),
  },
  mounted() {
    window.scrollTo(0, 0);
  },
  beforeUnmount() {
    // Clear the data when the component is destroyed
    this.$store.commit('clearConfirmationData');
  },
};
</script>

<template>
  <div>
    <p class="confirmation-header"><strong>{{ confirmationHeader }}</strong>&nbsp;#{{ registrationData.confirmationCode }}</p>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <v-card class="mx-auto my-5 pa-5" max-width="1000">
            <v-card-title class="d-flex justify-center">
              <v-icon class="mr-3">mdi-email</v-icon>
              <h3>We'll send you a confirmation email.</h3>
            </v-card-title>
            <v-card-text>
              <v-row v-if="teamData">
                <!-- Column 1: Team Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-1">
                    <p class="text-center"><strong>Team Info</strong></p>
                  </v-card-subtitle>
                  <p class="mt-1"><strong>{{ teamData.name }}</strong></p>
                  <p class="mt-1"><strong>Race:</strong> {{ raceData.name }}</p>
                  <p class="mb-2 mt-1"><strong>Projected Team Time:</strong> {{ teamData.projectedTeamTime }}</p>
                  <v-row>
                    <v-col cols="6" v-for="(member, index) in teamData.emails" :key="index" class="d-flex align-center justify-center">
                      <v-icon class="mr-2">mdi-account</v-icon>
                      <p class="mb-0"><strong>Leg {{ member.legOrder }}:</strong> {{ member.email }}</p>
                    </v-col>
                  </v-row>

                </v-col>

                <!-- Column 2: Registration Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-1">
                    <p class="text-center"><strong>Registration & Race Info</strong></p>
                  </v-card-subtitle>
                  <p class="mt-1"><strong>{{ registrationData.name }}</strong></p>
                  <p class="mt-1">{{ registrationData.email }}</p>
                  <p class="mt-1"><strong>Confirmation Code:</strong> #{{ registrationData.confirmationCode }}</p>
                  <p class="mt-1"><strong>Date: <span class="confirmation-registration-date"> {{ raceData.time }} {{ formatDate(raceData.date) }}</span></strong> </p>
                  <p class="mt-1"><strong>Location:</strong> {{ raceData.address }}, {{ raceData.city }}, {{ raceData.state }}</p>
                  <p class="mt-1"><strong>Contact:</strong> {{ raceData.contact }}</p>
                  <p class="mt-1"><a :href="raceData.websiteUrl" target="_blank">{{ raceData.websiteUrl }}</a></p>
                  <p class="mt-1"><a :href="raceData.instagramUrl" target="_blank"><v-icon class="instagram-icon pa-2">mdi-instagram</v-icon></a></p>
                </v-col>
              </v-row>
              <v-row v-if="!teamData && eventData && registrationData">
                <!-- Column 1: Registrant Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-2">
                    <p class="text-center"><strong>Registrant Info</strong></p>
                  </v-card-subtitle>
                  <p class="mt-1"><strong>{{ registrationData.name }}</strong></p>
                  <p class="mt-1">{{ registrationData.email }}</p>
                  <p class="mt-1"><strong>Confirmation Code:</strong> #{{ registrationData.confirmationCode }}</p>

                </v-col>

                <!-- Column 2: Event Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-1">
                    <p class="text-center"><strong>Event Info</strong></p>
                  </v-card-subtitle>
                  <p class="mt-1"><strong>{{ eventData.name }}</strong></p>
                  <p class="mt-1"><strong>Date: <span class="confirmation-registration-date"> {{ eventData.time }} {{ formatDate(eventData.date) }}</span></strong> </p>
                  <p class="mt-1"><strong>Location:</strong> {{ eventData.address }}, {{ eventData.city }}, {{ eventData.state }}</p>
                  <p class="mt-1"><strong>Contact:</strong> {{ eventData.contact }}</p>
                  <p class="mt-1"><a :href="eventData.websiteUrl" target="_blank">{{ eventData.websiteUrl }}</a></p>
                  <p class="mt-1"><a :href="eventData.instagramUrl" target="_blank"><v-icon class="instagram-icon pa-2">mdi-instagram</v-icon></a></p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
           <!-- Second Card: Billing Info -->
          <v-card class="mx-auto my-5 pa-5" max-width="1000" v-if="paymentData">
            <v-card-title class="d-flex justify-center">
              <v-icon class="mr-3">mdi-credit-card</v-icon>
              <h3>Order Summary</h3>
            </v-card-title>
            <v-card-text>
              <v-row>
                <!-- Column 1: Billing Amount -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-1">
                    <p class="text-center"><strong>Transaction Details</strong></p>
                  </v-card-subtitle>
                  <!-- Correctly format amount -->
                  <p class="confirmation-billing-amount mt-1"><strong>Total: ${{ (paymentData.amount / 100).toFixed(2) }}</strong></p>
                  <p class="mt-1"><strong>Transaction receipt sent to: </strong>{{ paymentData.receiptEmail }}</p>
                </v-col>
                <v-col cols="6">
                  <v-card-subtitle class="mb-1">
                    <!-- change this here. what is appropriate? -->
                    <p class="text-center"><strong>Payment Information</strong></p>
                  </v-card-subtitle>
                  <p class="mt-1">Please note this transaction will appear on your credit card statement as a variation of <strong>RelayEntry</strong>.</p>
                  <p class="mt-1"><strong>Important:</strong> RelayEntry does not store any payment details or credit card information. Your transaction is securely processed through our payment provider.</p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<style scoped>
    .v-card {
      max-width: 100%;
    }
    .confirmation-header{
      font-size: 2rem;
    }
    .confirmation-registration-date{
      color: #4caf50;
    }
    .confirmation-billing-amount{
      color: rgb(24, 103, 192);
      font-size: 1.5rem;
    }
    .instagram-icon {
      color: #e1306c;
      background-color: #f7f7f7;
      border-radius: 50%;
    }
</style>
