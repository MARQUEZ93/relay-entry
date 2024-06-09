<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-img :src="event.logo" v-if="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title>
            <h1>Event: {{ event.name }}</h1>
          </v-card-title>
          <v-card-subtitle v-if="event.date">
            <p><strong>Date:</strong> {{ event.date }} <span v-if="event.end_date">- {{ event.end_date }}</span></p>
          </v-card-subtitle>
          <v-card-subtitle v-if="event.address || event.city || event.state || event.postal_code">
            <p><strong>Location:</strong>
              <span v-if="event.address">{{ event.address }}, </span>
              <span v-if="event.city">{{ event.city }}, </span>
              <span v-if="event.state">{{ event.state }} </span>
              <span v-if="event.postal_code">{{ event.postal_code }}</span>
            </p>
          </v-card-subtitle>
          <v-card-subtitle v-if="event.google_maps_link">
            <p><a :href="event.google_maps_link" target="_blank">View on Google Maps</a></p>
          </v-card-subtitle>
          <v-card-text v-if="event.description">
            <p>{{ event.description }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="event.facebook_url" :href="event.facebook_url" target="_blank" icon>
              <v-icon>mdi-facebook</v-icon>
            </v-btn>
            <v-btn v-if="event.instagram_url" :href="event.instagram_url" target="_blank" icon>
              <v-icon>mdi-instagram</v-icon>
            </v-btn>
            <v-btn v-if="event.twitter_url" :href="event.twitter_url" target="_blank" icon>
              <v-icon>mdi-twitter</v-icon>
            </v-btn>
            <v-btn v-if="event.email_url" :href="event.email_url" target="_blank" icon>
              <v-icon>mdi-email</v-icon>
            </v-btn>
            <v-btn v-if="event.website_url" :href="event.website_url" target="_blank" icon>
              <v-icon>mdi-web</v-icon>
            </v-btn>
          </v-card-actions>
          <v-card-subtitle v-if="event.media_file">
            <p><a :href="event.media_file" target="_blank">Download Media File</a></p>
          </v-card-subtitle>
        </v-card>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>
        <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'EventComponent',
  data() {
    return {
      event: {},
      loading: true,
      error: null,
    };
  },
  async created() {
    const eventId = this.$route.params.id;
    try {
      const response = await api.getEvent(eventId);
      this.event = response.data;
      this.loading = false;
    } catch (error) {
      this.error = 'Error fetching event details.';
      this.loading = false;
    }
  },
};
</script>

<style scoped>
h1 {
  color: #2c3e50;
  margin-top: 20px;
}

p {
  font-size: 1.2em;
  color: #2c3e50;
}

.v-btn {
  margin: 0 5px;
}
</style>
