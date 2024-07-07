<script>
import { mapState } from 'vuex';
export default {
  computed: {
    ...mapState({
      registrationData: state => state.registrationData,
      raceData: state => state.raceData,
      paymentData: state => state.paymentData,
      teamData: state => state.teamData,
    }),
  },
  mounted() {
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
        <v-col cols="12" md="8">
          <v-card class="mx-auto my-5 pa-5" max-width="800">
            <v-card-title>
              <h3>Registration Information</h3>
            </v-card-title>
            <v-card-text>
              <p><strong>Event Name:</strong> {{ "f" }}</p>
              <p><strong>Participant Name:</strong> {{ "f" }}</p>
              <!-- <p><strong>Email:</strong> {{ participantEmail }}</p>
              <p><strong>Team Name:</strong> {{ teamName }}</p>
              <p><strong>Team Members:</strong></p> -->
              <!-- <v-list>
                <v-list-item v-for="(member, index) in teamMembers" :key="index">
                  <v-list-item-content>{{ member.name }} - {{ member.email }}</v-list-item-content>
                </v-list-item>
              </v-list> -->
            </v-card-text>
          </v-card>

          <v-card class="mx-auto my-5 pa-5" max-width="800">
            <v-card-title>
              <h3>Order Summary</h3>
            </v-card-title>
            <v-card-text>
              <p><strong>Race Price:</strong> $222</p>
              <!-- <p><strong>Discount:</strong> -${{ discount }}</p>
              <p><strong>Total Payment:</strong> ${{ totalPayment }}</p> -->
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
</style>
