<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  name: 'EventComponent',
  data() {
    return {
      event: {},
      loading: true,
      error: null,
    };
  },
  computed: {
    formattedEventDate() {
      if (this.event.date) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const start = this.formatDateToUTC(this.event.date, options);
        if (this.event.end_date) {
          const end = this.formatDateToUTC(this.event.end_date, options);
          return `${start} - ${end}`;
        }
        return start;
      }
      return null;
    },
    formattedEventLocation() {
      const parts = [
        this.event.address,
        this.event.city,
        this.event.state,
        this.event.postal_code,
      ].filter(Boolean);
      return parts.join(', ');
    },
    socialIcons() {
      return [
        { name: 'facebook', icon: 'mdi-facebook', iconClass: 'facebook-icon', url: this.event.facebook_url },
        { name: 'instagram', icon: 'mdi-instagram', iconClass: 'instagram-icon', url: this.event.instagram_url },
        { name: 'twitter', icon: 'mdi-twitter', iconClass: 'twitter-icon', url: this.event.twitter_url },
        { name: 'email', icon: 'mdi-email', iconClass: 'email-icon', url: `mailto:${this.event.email}` },
        { name: 'website', icon: 'mdi-web', iconClass: 'website-icon', url: this.event.website_url },
      ].filter(icon => icon.url);
    },
  },
  methods: {
    customSameDistance,
    formattedRaceDate,
    formatDateToUTC,
    formatMinute,
    getRegisterButtonText(race) {
      return race.is_relay ? 'Register My Team' : 'Register';
    },
    formatPrice(price) {
      return Number(price).toFixed(2);
    },
  },
  async created() {
    const eventSlug = this.$route.params.eventUrlAlias;
    try {
      const response = await api.getEvent(eventSlug);
      this.event = response.data;
      this.loading = false;
    } catch (error) {
      this.error = 'Error fetching event details.';
      this.loading = false;
    }
  },
};
</script>

<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto my-5 pa-5" max-width="800">
          <v-img :src="event.logo" v-if="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
          <v-card-title>
            <h1>{{ event.name }}</h1>
          </v-card-title>
          <v-card-subtitle v-if="formattedEventDate">
            <p><strong>Date:</strong> {{ formattedEventDate }}</p>
          </v-card-subtitle>
          <v-card-subtitle v-if="formattedEventLocation">
            <p><strong>Location:</strong> {{ formattedEventLocation }}</p>
          </v-card-subtitle>
          <!-- <v-card-subtitle v-if="event.google_maps_link">
            <p><a :href="event.google_maps_link" target="_blank">View on Google Maps</a></p>
          </v-card-subtitle> -->
          <!-- <v-card-subtitle v-if="event.google_maps_html">
            <p v-html="event.google_maps_html"></p>
          </v-card-subtitle> -->
          <v-card-text v-if="event.description">
            <p>{{ event.description }}</p>
          </v-card-text>
          <v-card-actions class="social-icons">
            <v-btn v-for="icon in socialIcons" :key="icon.name" :href="icon.url" target="_blank" icon>
              <v-icon :class="icon.iconClass">{{ icon.icon }}</v-icon>
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
            <v-card class="mx-auto my-3 race-card" outlined>
              <v-card-title v-if="race.name">
                <span>{{ race.name }}</span>
              </v-card-title>
              <v-card-subtitle v-if="race.is_relay && race.same_distance">
                <p v-if="race.custom_distance_value && race.custom_distance_unit">
                  {{race.num_runners }} x {{customSameDistance(race)}}
                </p>
              </v-card-subtitle>
              <v-card-subtitle>
                <p>{{ race.hour }}:{{ formatMinute(race.minute) }} {{ race.time_indicator }} </p>
              </v-card-subtitle>
              <!-- <v-card-subtitle>
                <p>{{ formattedRaceDate(race.date) }} </p>
              </v-card-subtitle> -->
              <v-card-subtitle>
                <p>${{ formatPrice(race.price) }}</p>
              </v-card-subtitle>
              <v-card-actions class="justify-center">
                <router-link :to="`/events/${event.url_alias}/${race.id}`">
                  <v-btn color="primary">{{ getRegisterButtonText(race) }}</v-btn>
                </router-link>
              </v-card-actions>
              <v-card-actions class="justify-center">
                <router-link :to="`/events/${event.url_alias}/${race.id}`">
                  <v-btn color="primary">Member Waiver</v-btn>
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

.social-icons {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.social-icons .v-btn {
  margin: 0 10px;
}

.social-icons .v-icon {
  font-size: 30px;
}

.facebook-icon {
  color: #3b5998;
  background-color: #e9ebee;
  border-radius: 50%;
}

.instagram-icon {
  color: #e1306c;
  background-color: #f7f7f7;
  border-radius: 50%;
}

.twitter-icon {
  color: #1da1f2;
  background-color: #e8f5fd;
  border-radius: 50%;
}

.email-icon {
  color: #ea4335;
  background-color: #fce8e6;
  border-radius: 50%;
}

.website-icon {
  color: #4285f4;
  background-color: #e8f0fe;
  border-radius: 50%;
}
.race-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.race-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
</style>
