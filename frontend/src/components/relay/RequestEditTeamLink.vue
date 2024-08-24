<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: ''
      };
    },
    methods: {
      sendEmail() {
        const eventId = this.$route.params.event_id;
        axios.post(`/api/events/${eventId}/request-edit-link/`, { email: this.email })
          .then(response => {
            this.$emit('show-snackbar', response.data.message);
          })
          .catch(error => {
            console.error('There was an error sending the email:', error);
            this.$emit('show-snackbar', 'An error occurred while sending the email.');
          });
      }
    }
  };
</script>
<template>
    <v-container class="mt-5">
      <v-form @submit.prevent="sendEmail" v-slot="{ errors }">
        <v-text-field
          v-model="email"
          label="Enter your email to edit your team"
          type="email"
          :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
          required
        ></v-text-field>
        <v-btn type="submit" color="primary">Send Link</v-btn>
      </v-form>
    </v-container>
</template>

  