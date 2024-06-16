<script>
import api from '@/services/api';  // Adjust the path according to your project structure
export default {
  props: {
    race: {
      type: Object,
      required: true,
    },
    racerData: {
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
    async handlePayment() {
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
          const response = await api.createPaymentIntent({
            payment_method_id: paymentMethod.id,
            race_id: this.race.id,
            racer_data: this.racerData,
            billing_info: this.billingInfo,
          });

          if (response.data.error) {
            document.getElementById('card-errors').textContent = response.data.error;
          } else {
            // Confirm the payment on the client side
            const { clientSecret } = response.data;
            const { error: confirmError } = await this.stripe.confirmCardPayment(clientSecret);

            if (confirmError) {
              document.getElementById('card-errors').textContent = confirmError.message;
            } else {
              // Handle successful payment here
              console.log('Payment successful');
            }
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
  <v-card>
    <v-card-title>
      <h2>Checkout</h2>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="billingInfo.name"
          label="Name"
          required
        ></v-text-field>
        <v-text-field
          v-model="billingInfo.email"
          label="Email"
          required
        ></v-text-field>
        <v-text-field
          v-model="billingInfo.address"
          label="Address"
          required
        ></v-text-field>
        <v-text-field
          v-model="billingInfo.city"
          label="City"
          required
        ></v-text-field>
        <v-text-field
          v-model="billingInfo.state"
          label="State"
          required
        ></v-text-field>
        <v-text-field
          v-model="billingInfo.zip"
          label="ZIP Code"
          required
        ></v-text-field>
        <div ref="cardElement" id="card-element"></div>
        <div id="card-errors" role="alert" class="mt-2"></div>
        <p class="mt-4"><strong>Order Total: ${{ race.price }}</strong></p>
      </v-form>
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
