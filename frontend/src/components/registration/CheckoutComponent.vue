<script>
import api from '@/services/api';  // Adjust the path according to your project structure
export default {
  props: {
    race: {
      type: Object,
      required: true,
    },
    registrationData: {
      type: Object,
      required: true,
    },
    clientSecret: {
      type: String,
      required: true,
    },
    amount: {
      required: true,
    },
    paymentIntentId: {
      type: String,
      required: true,
    },
    stripe: {
      required: true,
      type: Object,
    },
  },
  async mounted() {
    this.setupElements();
  },
  computed: {
    formattedAmount() {
      return (this.amount / 100).toFixed(2);
    }
  },
  data() {
    return {
      elements: {},
      elementsLoading: true,
      loading: false,
      snackbar: {
        show: false,
        message: '',
        timeout: 8000
      },
    };
  },
  methods: {
    async setupElements() {
      if (!this.stripe || !this.clientSecret){
        return;
      }
      const options = {
        clientSecret: this.clientSecret,
      };
      // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in a previous step
      this.elements = this.stripe.elements(options);
      // Create and mount the Payment Element
      const paymentElement = this.elements.create('payment');
      await paymentElement.mount('#payment-element');
      this.elementsLoading = false;
    },
    showError(message) {
      this.snackbar.message = message;
      this.snackbar.show = true;
    },
    async payAndRegisterTeam() {
      this.loading = true; // Show loader
      try {
        console.log("hit payAndRegisterTeam");
        const cp = await this.stripe.confirmPayment({
          elements: this.elements,
          confirmParams: {
            // return_url: `${window.location.origin}`
            receipt_email: this.registrationData.email,
          },
          redirect: 'if_required'
        });
        console.log(cp);
        if (cp.error) {
          const error = cp.error;
          if (error.type === "card_error" || error.type === "validation_error") {
            this.showError(error.message);
          } else {
            this.showError("An unexpected error occured.");
          }
          this.loading = false;
          return;
        }
        console.log(this.paymentIntentId);
        console.log("HI");
        const response = await api.registerTeam({
          raceId: this.race.id,
          registrationData: this.registrationData,
          teamData: this.teamData,
          paymentIntentId: this.paymentIntentId,
        });
        if (response.data.error) {
          this.loading = false; // Hide loader on error
          this.showError('An error occurred while processing your registration. Please Teamtry again later.');
          return;
        } else {
          console.log(response.data);
          const { registrationData, raceData, teamData, paymentData } = response.data;
          this.$store.commit('setConfirmationData', {
            registrationData: registrationData,
            raceData: raceData,
            teamData: teamData,
            paymentData: paymentData,
          });
          this.loading = false;
          this.$router.push({ name: 'Confirmation' });
        }
      } catch (e){
          console.log(e);
          this.loading = false; // Hide loader on error
          this.showError('An error occurred while processing your registration. Please try again later.');
          return;
      }
    },
  },
};
</script>

<template>
  <div>
    <v-card>
      <v-card-title>
        <h2>Checkout</h2>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-row>
            <v-col cols="12">
              <div v-if="elementsLoading || !stripe || !clientSecret">Loading payment gateway...</div>
              <div id="payment-element"></div>
              <p class="mt-3 order-total"><strong>Grand Total: ${{ formattedAmount }}</strong></p>
            </v-col>
          </v-row>
          <!-- Snackbar for error messages -->
          <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" color="error">
            {{ snackbar.message }}
            <v-btn color="white" text @click="snackbar.show = false">Close</v-btn>
          </v-snackbar>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn :readonly="loading || elementsLoading" color="primary" @click="payAndRegisterTeam" class="pay-now">Pay Now</v-btn>
      </v-card-actions>
      <v-progress-circular class="mt-5 mb-5" v-if="loading" color="primary" indeterminate :size="80" :width="7"></v-progress-circular>
    </v-card>
  </div>
</template>

<style scoped>
#card-element {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.v-btn {
  margin: 0 5px;
}
.pay-now{
  background: rgb(24, 103, 192);
  color: white !important;
}
.order-total {
  font-size: 18px;
  font-weight: bold;
}
</style>
