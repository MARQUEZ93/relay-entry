<script>
import { mapState } from 'vuex';
export default {
  computed: {
    ...mapState({
      confirmationCode: state => state.confirmationCode,
      racerData: state => state.racerData,
      raceData: state => state.raceData,
      paymentIntent: state => state.paymentIntent,
    }),
  },
  mounted() {
    // Log the props to inspect them
    console.log('Confirmation Code:', this.confirmationCode);
    console.log('Racer Data:', this.racerData);
    console.log('Race Data:', this.raceData);
    console.log('Payment Intent:', this.paymentIntent);
  },
  beforeUnmount() {
    // Clear the data when the component is destroyed
    this.$store.commit('clearConfirmationData');
  },
};
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-card-title class="text-h5 text-center">
            Registration Successful!
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" class="text-center">
                <p>Thank you for your registration. Here are your details:</p>
              </v-col>

              <v-col cols="12">
                <v-divider></v-divider>
                <h3 class="text-h6">Confirmation Code:</h3>
                <p class="my-2">{{ confirmationCode }}</p>
              </v-col>

              <v-col cols="12">
                <v-divider></v-divider>
                <h3 class="text-h6">Racer Information:</h3>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Name:</strong> {{ racerData.firstName }} {{ racerData.lastName }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Email:</strong> {{ racerData.email }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Phone:</strong> {{ racerData.phone }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Gender:</strong> {{ racerData.gender }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Date of Birth:</strong> {{ racerData.dateOfBirth }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="racerData.minor">
                    <v-list-item-content>
                      <v-list-item-title><strong>Minor:</strong> {{ racerData.minor }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="racerData.minor">
                    <v-list-item-content>
                      <v-list-item-title><strong>Parent/Guardian Name:</strong> {{ racerData.parentGuardianName }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="racerData.minor">
                    <v-list-item-content>
                      <v-list-item-title><strong>Parent/Guardian Signature:</strong> {{ racerData.parentGuardianSignature }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12">
                <v-divider></v-divider>
                <h3 class="text-h6">Race Information:</h3>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Name:</strong> {{ raceData.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Date:</strong> {{ raceData.date }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Event:</strong> {{ raceData.event }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Description:</strong> {{ raceData.description }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12">
                <v-divider></v-divider>
                <h3 class="text-h6">Payment Information:</h3>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Amount Paid:</strong> {{ paymentIntent.amount / 100 }} USD</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title><strong>Status:</strong> {{ paymentIntent.status }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>

              <v-col cols="12" class="text-center">
                <v-divider></v-divider>
                <p class="my-2">You will receive an email confirmation shortly.</p>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<style scoped>
    .v-card {
    max-width: 100%;
    }
</style>
