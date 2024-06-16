<script>
export default {
  mounted() {
    console.log('Confirmation Code:', this.confirmationCode);
    console.log('Racer Data:', this.racerData);
    console.log('Race Data:', this.raceData);
    console.log('Payment Intent:', this.paymentIntent);
  },
  props: {
    confirmationCode: {
      type: String,
      required: true,
    },
    racerData: {
      type: Object,
      required: true,
    },
    raceData: {
      type: Object,
      required: true,
    },
    paymentIntent: {
      type: Object,
      required: true,
    },
  },
};
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-card-title>
            <h2>Registration Successful!</h2>
          </v-card-title>
          <v-card-text>
            <p>Thank you for your registration. Here are your details:</p>
            <p><strong>Confirmation Code:</strong> {{ confirmationCode }}</p>
            <p><strong>Racer Information:</strong></p>
            <ul>
              <li><strong>Name:</strong> {{ racerData }} {{ racerData}}</li>
              <!-- <li><strong>Email:</strong> {{ racerData.email }}</li>
              <li><strong>Phone:</strong> {{ racerData.phone }}</li>
              <li><strong>Gender:</strong> {{ racerData.gender }}</li>
              <li><strong>Date of Birth:</strong> {{ racerData.dateOfBirth }}</li>
              <li><strong>Minor:</strong> {{ racerData.minor ? 'Yes' : 'No' }}</li> -->
              <!-- <li v-if="racerData.minor"><strong>Parent/Guardian Name:</strong> {{ racerData.parentGuardianName }}</li> -->
              <!-- <li v-if="racerData.minor"><strong>Parent/Guardian Signature:</strong> {{ racerData.parentGuardianSignature }}</li> -->
            </ul>
            <p><strong>Race Information:</strong></p>
            <ul>
              <!-- <li><strong>Name:</strong> {{ raceData.name }}</li>
              <li><strong>Date:</strong> {{ raceData.date }}</li>
              <li><strong>Event:</strong> {{ raceData.event }}</li>
              <li><strong>Description:</strong> {{ raceData.description }}</li> -->
            </ul>
            <p><strong>Payment Information:</strong></p>
            <ul>
              <!-- <li><strong>Amount Paid:</strong> {{ paymentIntent.amount / 100 }} USD</li> -->
              <!-- <li><strong>Status:</strong> {{ paymentIntent.status }}</li> -->
            </ul>
            <p>You will receive an email confirmation shortly.</p>
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
