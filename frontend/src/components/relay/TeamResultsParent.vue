<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  name: 'TeamResultsParent',
  data() {
    return {
      event: {},
      loading: true,
      error: null,
      eventSlug: '',
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
    formatPrice(price) {
      return Number(price).toFixed(2);
    },
    goToEventPage() {
      // this.eventSlug vs this.event.url_alias
      this.$router.push({ name: 'Event', params: { eventUrlAlias: this.eventSlug } });
    },
  },
  async created() {
    this.eventSlug = this.$route.params.eventUrlAlias;
    try {
      const response = await api.getEvent(this.eventSlug);
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
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-btn color="primary" @click="goToEventPage">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Event Page
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-card class="mx-auto my-5 pa-5">
            <v-img :src="event.logo" :alt="`Event logo for ${event.name}`" v-if="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
            <v-card-title class="event-name">{{ event.name }}</v-card-title>
            <v-card-subtitle v-if="formattedEventDate">
                <strong>Date:</strong> {{ formattedEventDate }}
            </v-card-subtitle>
            <v-card-subtitle v-if="formattedEventLocation">
                <strong>Location:</strong> {{ formattedEventLocation }}
            </v-card-subtitle>
            <v-card-actions class="social-icons">
                <v-btn v-for="icon in socialIcons" :key="icon.name" :href="icon.url" target="_blank" icon>
                  <v-icon :class="icon.iconClass">{{ icon.icon }}</v-icon>
                </v-btn>
            </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
    <v-row v-if="!loading && event.races">
        <v-col v-for="race in event.races" :key="'teamResults-' + race.id" cols="6">
            <v-card class="race-card">
                <v-card-title>
                    <router-link :to="{ name: 'TeamRaceResults', params: { eventUrlAlias: this.eventSlug, raceId: race.id } }">
                        {{ race.name }}
                    </router-link>
                </v-card-title>
            </v-card>
        </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
  .event-name {
    font-size: 2.5rem;
    word-wrap: break-word;
    white-space: normal;
    overflow-wrap: break-word; 
  }
  @media (max-width: 600px) {
    .event-name {
      font-size: 2rem; /* Adjust the size as needed for mobile */
      word-break: keep-all; /* Prevents words from breaking up */
      white-space: normal; /* Allows normal wrapping */
    }
  }
  .help-text {
    font-size: 0.9rem;
    color: #6c757d; /* A subtle gray color */
  }

  .v-btn {
    margin: 0 5px;
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
  .team-member-details {
    background-color: rgba(var(--v-theme-on-surface), var(--v-hover-opacity));
  }
</style>
