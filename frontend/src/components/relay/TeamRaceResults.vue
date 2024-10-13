<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  name: 'TeamRaceResults',
  data() {
    return {
      event: {},
      loading: true,
      error: null,
      eventSlug: '',
      raceId: '',
      raceResults: [],
      itemsPerPage: 50, // Default items per page
      numRunners: 0,
      raceName: '',
    };
  },
  computed: {
    dynamicHeaders() {
      const baseHeaders = [
        { title: 'Place', value: 'place', key: 'place', sortable: false, align: 'center' },
        { title: 'Team', value: 'name', key: 'name', sortable: false, align: 'center' },
        { title: 'Captain', value: 'captain_name', key: 'captain_name', sortable: false, align: 'center' },
        { title: 'Time', value: 'time', key: 'time', sortable: false, align: 'center' },
      ];

      // for (let i = 1; i <= this.numRunners; i++) {
      //   baseHeaders.push({ title: `Leg ${i} Time`, value: `leg_times[${i}]`, key: `leg_times[${i}]`, sortable: false });
      // }

      return baseHeaders;
    },
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
    goToResultsPage() {
      // this.eventSlug vs this.event.url_alias
      this.$router.push({ name: 'TeamResultsParent', params: { eventUrlAlias: this.eventSlug } });
    },
  },
  async created() {
    this.eventSlug = this.$route.params.eventUrlAlias;
    this.raceId = this.$route.params.raceId;
    try {
        const eventResponse = await api.getEvent(this.eventSlug);
        this.event = eventResponse.data;
        const response = await api.getTeamRaceResults(this.raceId);
        if (response.data.length > 0) {
          this.raceName = response.data[0].race_name;
          this.numRunners = response.data[0].num_runners;
        }
        // Sort teams by team_result.place
        this.raceResults = response.data.sort((a, b) => {
          const placeA = a.team_result ? a.team_result.place : Number.MAX_VALUE;
          const placeB = b.team_result ? b.team_result.place : Number.MAX_VALUE;
          return placeA - placeB;
        });
        this.loading = false;
    } catch (error) {
        this.error = 'Error fetching race results details.';
        this.loading = false;
    }
  },
};
</script>

<template>
  <v-container>
    <v-row>
        <v-col>
            <v-card class="mx-auto my-5 pa-5">
            <v-img :src="event.logo" :alt="`Event image for ${event.name}`" v-if="event.logo" class="mb-4" aspect-ratio="2.75"></v-img>
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
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-btn color="primary" @click="goToResultsPage">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Results Page
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-if="!loading && raceResults.length > 0">
      <v-col cols="12">
        <v-card-title>{{ raceName }} Results</v-card-title>
        <v-card-subtitle class="prevent-overflow">
          Results displayed exactly as provided by the event or timer.
        </v-card-subtitle>
        <v-data-table
          :items="raceResults"
          :headers="dynamicHeaders"
          :items-per-page="itemsPerPage"
        >
          <template v-slot:[`item.place`]="{ item }">
            {{ item.team_result ? item.team_result.place : '' }}
          </template>
          <template v-slot:[`item.name`]="{ item }">
            {{ item.name }}
          </template>
          <template v-slot:[`item.captain_name`]="{ item }">
            {{ item.captain_name ? item.captain_name : '' }}
          </template>
          <template v-slot:[`item.time`]="{ item }">
            {{ item.team_result ? formatMinute(item.team_result.time) : '' }}
          </template>
          <template v-slot:no-data>
            <v-alert :value="true" color="error" icon="mdi-alert">
              No results found for this race.
            </v-alert>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-row v-if="!loading && raceResults.length === 0">
      <v-col cols="12">
        <v-card>
          <v-card-title>No Results</v-card-title>
          <v-card-text>
            No results available for this race.
          </v-card-text>
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
