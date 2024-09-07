<script>
import api from '@/services/api';  // Adjust the path according to your project structure
export default {
  inject: ['showSnackbar'],
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
    paymentElementContainer: {
      type: HTMLElement,
      required: true
    },
    elements: {
      required: true,
      type: Object,
    }
  },
  async mounted() {
    this.setupElements();
    window.scrollTo(0, 0);
  },
  computed: {
    formattedAmount() {
      return (this.amount / 100).toFixed(2);
    }
  },
  data() {
    return {
      elementsLoading: true,
      loading: false,
    };
  },
  methods: {
    async setupElements() {
      await this.$refs.paymentElementWrapper.appendChild(this.paymentElementContainer);
      this.elementsLoading = false;
    },
    async payAndRegisterTeam() {
      this.loading = true; // Show loader
      try {
        const cp = await this.stripe.confirmPayment({
          elements: this.elements,
          confirmParams: {
            receipt_email: this.registrationData.email,
          },
          redirect: 'if_required'
        });
        if (cp.error) {
          const error = cp.error;
          if (error.type === "card_error" || error.type === "validation_error") {
            this.showSnackbar(error.message, 'error');
          } else {
            this.showSnackbar("An unexpected error occured. No payment was processed.", 'error');
          }
          this.loading = false;
          return;
        }
        const response = await api.registerTeam({
          raceId: this.race.id,
          registrationData: this.registrationData,
          teamData: this.teamData,
          paymentIntentId: this.paymentIntentId,
        });
        if (response.data.error) {
          this.loading = false; // Hide loader on error
          this.showSnackbar('An error occurred while processing your registration. Please email relayentry@gmail.com', 'error');
          return;
        } else {
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
          this.loading = false; // Hide loader on error
          this.showSnackbar(`Something unexpected occurred while processing your registration: ${e.response.data.error} `, 'error');
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
              <div v-if="paymentElementContainer">
                <!-- Render the payment element container passed from the parent -->
                <div ref="paymentElementWrapper"></div>
              </div>
              <div v-if="elementsLoading || !paymentElementContainer || !stripe || !clientSecret">Loading payment gateway...</div>
              <!-- <div id="payment-element"></div> -->
              <p class="mt-3 order-total"><strong>Grand Total: ${{ formattedAmount }}</strong></p>
              <p class="mt-3 text-center"><strong>Note:</strong> All payments are non-refundable.</p>
            </v-col>
          </v-row>
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
