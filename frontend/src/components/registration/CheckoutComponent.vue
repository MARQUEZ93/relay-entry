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
    stripePromise: {
      type: Promise,
      required: true,
    },
  },
  data() {
    return {
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
      stripe: null,
      cardElement: null,
      valid: false,
      billingInfo: {
        name: '',
        email: '',
        address: '',
        city: '',
        state: '',
        zip: '',
      },
      paymentSuccess: false,
      confirmationCode: '',
    };
  },
  async mounted() {
    try {
      this.stripe = await this.stripePromise; // Await the resolution of the promise to get the Stripe instance
      if (!this.stripe) {
        throw new Error('Stripe connection problems');
      }
      const elements = this.stripe.elements();
      this.cardElement = elements.create('card');
      this.cardElement.mount(this.$refs.cardElement);
    } catch (error) {
      console.error('Error setting up Stripe elements:', error);
    }
  },
  methods: {
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
    async registerTeamAndPay() {
      if (!this.$refs.form.validate()) {
        return;
      }
      if (!this.validateBillingInfo()) {
        // Show an error message if validation fails
        this.showError('Please fill out all required billing information.');
        return;
      }

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

      if (error) {
        this.showError('There was an issue with your card details. Please check and try again.');
      } else {
        try {
          const response = await api.payAndRegisterTeam({
            raceId: this.race.id,
            price: this.race.price,
            registrationData: this.registrationData,
            teamData: this.teamData,
            paymentMethod: paymentMethod,
            billingInfo: this.billingInfo
          });

          console.log("registerTeamAndPay");

          console.log(response);
          console.log(response.data);

          if (response.data.error) {
            this.showError('An error occurred while processing your registration. Please try again later.');
          } else {
            
            // TODO: null check here
            // package this tighter
            const { confirmationCode, registrationData, raceData, paymentAmount, paymentStatus, teamData } = await response.data;
            console.log(response); 
            console.log(registrationData);
            console.log(teamData);
            console.log(raceData);
            console.log(paymentAmount);
            console.log(confirmationCode);
            console.log(paymentStatus);

            // TODO: add loader
            // test bad data

            // Redirect to the confirmation page
             // Set the data in Vuex store
            //  TODO: null check
            this.$store.commit('setConfirmationData', {
              confirmationCode: confirmationCode,
              registrationData: registrationData,
              raceData: raceData,
              paymentStatus: paymentStatus,
              paymentAmount: paymentAmount,
              teamData: teamData
            });

            this.$router.push({ name: 'Confirmation' });
          }
        } catch (err) {
          this.showError('An error occurred while processing your transaction. Please try again later.');
        }
      }
    },
  },
};
</script>

<template>
  <v-card v-if="!paymentSuccess">
    <v-card-title>
      <h2>Checkout</h2>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.name"
              label="Name"
              :rules="nameRules"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
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
              v-model="billingInfo.address"
              label="Address"
              :rules="addressRules"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
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
              v-model="billingInfo.state"
              label="State"
              required
              :rules="stateRules"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.zip"
              label="ZIP Code"
              required
              :rules="zipRules"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div ref="cardElement" id="card-element"></div>
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
      <v-btn color="primary" @click="registerTeamAndPay" class="pay-now">Pay Now</v-btn>
    </v-card-actions>
  </v-card>

  <v-card v-else>
    <v-card-title>
      <h2>Registration Successful!</h2>
    </v-card-title>
    <v-card-text>
      <p>Thank you for your registration. Your confirmation code is: <strong>{{ confirmationCode }}</strong>.</p>
      <p>You will receive an email confirmation shortly.</p>
    </v-card-text>
  </v-card>
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
