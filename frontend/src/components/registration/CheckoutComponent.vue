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
  },
  async mounted() {
    await this.createPaymentIntent();
    await this.initStripe();
  },
  data() {
    return {
      loading: true,
      stripe: null,
      clientSecret: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length > 1) || 'Name must be more than 1 character',
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      addressRules: [
        v => !!v || 'Address is required',
      ],
      cityRules: [
        v => !!v || 'City is required',
      ],
      stateRules: [
        v => !!v || 'State is required',
      ],
      zipRules: [
        v => !!v || 'ZIP code is required',
      ],
      snackbar: {
        show: false,
        message: '',
        timeout: 8000
      },
      valid: false,
      billingInfo: {
        name: '',
        email: '',
        address: '',
        city: '',
        state: '',
        zip: '',
      },
    };
  },
  methods: {
    async initStripe() {
      if (!window.Stripe) {
        // Ensure Stripe.js is loaded from the global scope
        await new Promise((resolve) => {
          // Fallback in case the script hasn't loaded yet
          const script = document.createElement('script');
          script.src = 'https://js.stripe.com/v3/';
          script.async = true;
          script.onload = resolve;
          document.head.appendChild(script);
        });
      }
      this.stripe = Stripe("pk_test_51PNivYBsh8Ne4MdUVijN6hN4Ueoo8vLEFj5o5BqkAinexlV7S2f7P2EufuWHpqIR9SAAdZF5lpvk2kgHDFzTeuOQ009WWgftkv");
      this.setupElements();
    },
    async createPaymentIntent() {
      try {
        const response = api.createPaymentIntent({
          raceId: this.race.id
        })
        this.clientSecret = response.data.clientSecret;
        this.loading = false;
      } catch (error) {
        this.showError('Payment gateway error. Please try again later.');
        console.error('Error creating PaymentIntent:', error);
      }
    },
    setupElements() {
      const options = {
        clientSecret: this.clientSecret,
        // Fully customizable with appearance API.
        // appearance: {/*...*/},
      };
      // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in a previous step
      const elements = this.stripe.elements(options);
      // Create and mount the Payment Element
      const paymentElement = elements.create('payment');
      paymentElement.mount('#payment-element');
      this.loading = false;
    },
    showError(message) {
      this.snackbar.message = message;
      this.snackbar.show = true;
    },
    validateBillingInfo() {
      return (
        this.billingInfo.address &&
        this.billingInfo.city &&
        this.billingInfo.state &&
        this.billingInfo.zip &&
        this.billingInfo.name &&
        this.billingInfo.email
      );
    },
    async payAndRegisterTeam() {
      this.loading = true; // Show loader
      if (!this.$refs.form.validate()) {
        this.loading = false;
        return;
      }
      if (!this.validateBillingInfo()) {
        // Show an error message if validation fails
        this.loading = false; // Hide loader on error
        this.showError('Please fill out all required billing information.');
        return;
      }
      try {
        const { paymentMethod, error } = await this.stripe.createPaymentMethod({
          type: 'card',
          card: this.cardElement,
          billing_details: {
            name: this.billingInfo.name,
            email: this.billingInfo.email,
            address: {
              line1: this.billingInfo.address,
              city: this.billingInfo.city,
              state: this.billingInfo.state,
              postal_code: this.billingInfo.zip,
            },
          },
        });
      } catch (error){
        this.loading = false; // Hide loader on error
        this.showError('There was an issue with your card details. Please check and try again.');
        return;
      }
      try {
        const { error: confirmError, paymentIntent } = await this.stripe.confirmCardPayment(this.clientSecret, {
          payment_method: paymentMethod.id,
        });

        if (confirmError) {
          this.loading = false; // Hide loader on error
          this.showError('An error occurred while confirming your payment. Please try again.');
          return;
        } else {
          const response = await api.registerTeam({
            raceId: this.race.id,
            registrationData: this.registrationData,
            teamData: this.teamData,
            paymentIntent: paymentIntent,
          });
          if (response.data.error) {
            this.loading = false; // Hide loader on error
            this.showError('An error occurred while processing your registration. Please try again later.');
            return;
          } else {
            const { registrationData, raceData, paymentData, teamData } = await response.data;
            this.$store.commit('setConfirmationData', {
              registrationData: registrationData,
              raceData: raceData,
              paymentData: paymentData,
              teamData: teamData
            });
            this.loading = false;
            this.$router.push({ name: 'Confirmation' });
          }
        }
      } catch {
          this.loading = false; // Hide loader on error
          this.showError('An error occurred while processing your transaction. Please try again later.');
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
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="billingInfo.name"
                :readonly="loading"
                label="Name"
                :rules="nameRules"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                :readonly="loading"
                v-model="billingInfo.email"
                label="Email"
                :rules="emailRules"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                :readonly="loading"
                v-model="billingInfo.address"
                label="Address"
                :rules="addressRules"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                :readonly="loading"
                v-model="billingInfo.city"
                label="City"
                :rules="cityRules"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                :readonly="loading"
                v-model="billingInfo.state"
                label="State"
                required
                :rules="stateRules"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                :readonly="loading"
                v-model="billingInfo.zip"
                label="ZIP Code"
                required
                :rules="zipRules"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <div v-if="loading && !stripe">Loading payment gateway...</div>
              <div v-else id="payment-element"></div>
              <p class="mt-3 order-total"><strong>Grand Total: ${{ race.price }}</strong></p>
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
        <v-btn :readonly="loading" color="primary" @click="registerTeamAndPay" class="pay-now">Pay Now</v-btn>
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
