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
        throw new Error('Stripe instance is undefined');
      }
      const elements = this.stripe.elements();
      this.cardElement = elements.create('card');
      this.cardElement.mount(this.$refs.cardElement);
    } catch (error) {
      console.error('Error setting up Stripe elements:', error);
    }
  },
  methods: {
    async registerTeamAndPay() {
      if (!this.$refs.form.validate()) {
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
        document.getElementById('card-errors').textContent = error.message;
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
            document.getElementById('card-errors').textContent = response.data.error;
          } else {
            
            // TODO: null check here
            // package this tighter
            const { confirmationCode, registrationData, raceData, paymentAmount, paymentStatus, teamData } = await response.data;
            console.log(response); 
            console.log('Payment and registration successful');
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
          console.error('Error submitting payment:', err);
          document.getElementById('card-errors').textContent = 'An error occurred while processing your payment.';
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
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.email"
              label="Email"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.address"
              label="Address"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.city"
              label="City"
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
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="billingInfo.zip"
              label="ZIP Code"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div ref="cardElement" id="card-element"></div>
            <div id="card-errors" role="alert" class="mt-2"></div>
            <p class="mt-4"><strong>Order Total: ${{ race.price }}</strong></p>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="registerTeamAndPay">Pay Now</v-btn>
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
#card-errors {
  color: red;
}
</style>
