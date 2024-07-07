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
    ...mapState({
      registrationData: state => state.registrationData,
      raceData: state => state.raceData,
      paymentData: state => state.paymentData,
      teamData: state => state.teamData,
    }),
  },
  mounted() {
    console.log("confirmation mounted");
    window.scrollTo(0, 0);
    console.log('Registration Data:', this.registrationData);
    console.log('Race Data:', this.raceData);
    console.log('Payment Data:', this.paymentData);
    console.log('Team Data:', this.teamData);
  },
  beforeUnmount() {
    // Clear the data when the component is destroyed
    this.$store.commit('clearConfirmationData');
  },
};
</script>

<template>
  <div>
    <p class="confirmation-header"><strong>Registration Successful </strong>#{{ registrationData.confirmationCode }}</p>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <v-card class="mx-auto my-5 pa-5" max-width="1000">
            <v-card-title class="d-flex justify-center">
              <v-icon class="mr-3">mdi-email</v-icon>
              <h3>We'll send you an email with your registration information.</h3>
            </v-card-title>
            <v-card-text>
              <v-row>
                <!-- Column 1: Team Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-2">
                    <p class="text-center"><strong>Team Info</strong></p>
                  </v-card-subtitle>
                  <p><strong>{{ teamData.name }}</strong></p>
                  <p><strong>Race:</strong> {{ teamData.race }}</p>
                  <p><strong>Date: <span class="confirmation-registration-date">{{ formatDate(teamData.date) }}</span></strong> </p>
                  <p class="mb-2"><strong>Projected Team Time:</strong> {{ teamData.projectedTeamTime }}</p>
                  <v-row>
                    <v-col cols="6" v-for="(member, index) in teamData.emails" :key="index">
                      <v-icon>mdi-account</v-icon>
                      <p>Leg {{ member.legOrder }}: {{ member.email }}</p>
                    </v-col>
                  </v-row>

                </v-col>

                <!-- Column 2: Registration Information -->
                <v-col cols="6">
                  <v-card-subtitle class="mb-2">
                    <p class="text-center"><strong>Registration Info</strong></p>
                  </v-card-subtitle>
                  <p><strong>{{ registrationData.name }}</strong></p>
                  <p>{{ registrationData.email }}</p>
                  <p><strong>Confirmation Code:</strong> #{{ registrationData.confirmationCode }}</p>
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
</style>
