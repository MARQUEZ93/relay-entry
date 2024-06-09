<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-img :src="event.logo" v-if="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title>
            <h1>{{ event.name }}</h1>
          </v-card-title>
          <v-card-subtitle v-if="event.date">
            <p><strong>Date:</strong> {{ formattedEventDate(event.date, event.end_date) }}</p>
          </v-card-subtitle>
          <v-card-subtitle v-if="event.address || event.city || event.state || event.postal_code">
            <p><strong>Location: </strong>
              <span v-if="event.address">{{ event.address }}, </span>
              <span v-if="event.city">{{ event.city }}, </span>
              <span v-if="event.state">{{ event.state }}&nbsp;</span>
              <span v-if="event.postal_code">{{ event.postal_code }} </span>
            </p>
          </v-card-subtitle>
          <v-card-subtitle v-if="event.google_maps_link">
            <p v-if="event.google_maps_link"><a :href="event.google_maps_link" target="_blank">View on Google Maps</a></p>           
          </v-card-subtitle>
          <v-card-subtitle v-if="event.google_maps_html">
            <p v-if="event.google_maps_html" v-html="event.google_maps_html"></p>
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
        </v-card>
        <v-row>
          <v-col
            v-for="race in event.races"
            :key="race.id"
            cols="12"
            :md="event.races.length === 1 ? 12 : 4"
            class="d-flex align-center justify-center"
          >
            <v-card class="mx-auto my-3" outlined>
              <v-card-title>
                <span v-if="race.is_relay">Team Relay Race</span>
                <span v-else>{{ race.distance }}</span>
              </v-card-title>
              <v-card-subtitle v-if="race.description">
                <p>{{ race.description }}</p>
              </v-card-subtitle>
              <v-card-subtitle>
                <p><strong>Date:</strong> {{ formattedRaceDate(race.start_time) }}</p>
              </v-card-subtitle>
              <v-card-subtitle>
                <p><strong>Price:</strong> ${{ formatPrice(race.price) }}</p>
              </v-card-subtitle>
              <v-card-actions class="justify-center">
                <router-link :to="`/events/${event.url_alias}/${race.id}`">
                  <v-btn color="primary">Register</v-btn>
                </router-link>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
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
  methods: {
    formattedEventDate(startDate, endDate) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const start = new Date(startDate).toLocaleDateString(undefined, options);
      if (endDate) {
        const end = new Date(endDate).toLocaleDateString(undefined, options);
        return `${start} - ${end}`;
      }
      return start;
    },
    formattedRaceDate(date) {
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: 'numeric', 
        minute: 'numeric' 
      };
      return new Date(date).toLocaleString(undefined, options);
    },
    formatPrice(price) {
      return Number(price).toFixed(2);
    },
    formattedGoogleMapsLink(link) {
      const embedLink = link.replace('/maps', '/maps/embed');
      return embedLink;
    }
  },
  data() {
    return {
      event: {},
      loading: true,
      error: null,
    };
  },
  async created() {
    const urlAlias = this.$route.params.eventUrlAlias;
    try {
      console.log("hit");
      const response = await api.getEvent(urlAlias);
      this.event = response.data;
      console.log(response.data);
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

.v-card {
  max-width: 100%;
}

@media (min-width: 600px) {
  .v-card {
    max-width: 80%;
  }
}

@media (min-width: 960px) {
  .v-card {
    max-width: 60%;
  }
}
</style>

