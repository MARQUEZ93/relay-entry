<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  name: 'RegisteredTeams',
  data() {
    return {
      event: {},
      loading: true,
      error: null,
      eventSlug: '',
      expandedTeam: null,  // Track the currently expanded team
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
    getSortedMembers(members) {
      return members.slice().sort((a, b) => a.leg_order - b.leg_order);
    },
    toggleTeam(teamId) {
      this.expandedTeam = this.expandedTeam === teamId ? null : teamId;
    },
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
            <v-card-subtitle class="prevent-overflow">
                Each team member must register for their name to appear for their leg!
            </v-card-subtitle>
            </v-card>
        </v-col>
    </v-row>
    <v-row v-if="!loading && event.races">
        <v-col
            v-for="race in event.races"
            :key="'registeredTeams-race-' + race.id"
            cols="12"
            sm="6"
            md="4"
        >
            <v-card class="mx-auto my-3 race-card" outlined>
            <v-card-title>{{ race.name }}</v-card-title>
            <v-card-subtitle v-if="race.is_relay && race.same_distance && race.custom_distance_value && race.custom_distance_unit">
                {{race.num_runners }} x {{customSameDistance(race)}}
            </v-card-subtitle>
            <v-list dense v-if="race.teams.length > 0">
                <v-list-item
                    v-for="team in race.teams"
                    :key="team.id + team.name"
                    @click="toggleTeam(team.id)"
                >
                    <div>
                        <v-list-item-title class="d-flex align-center justify-center prevent-overflow">{{ team.name }} <v-icon small class="ml-3 mdi mdi-chevron-down"></v-icon></v-list-item-title>
                        <v-list-item-subtitle><strong>Captain:</strong> {{ team.captain.first_name }} {{ team.captain.last_name }}</v-list-item-subtitle>
                        <v-list-item-subtitle><strong>Projected Time:</strong> {{ team.projected_team_time }}</v-list-item-subtitle>
                    </div>
                    <v-expand-transition v-if="expandedTeam === team.id">
                        <v-card>
                            <v-list dense class="team-member-details">
                                <v-list-item
                                    v-for="member in getSortedMembers(team.members)"
                                    :key="member.id + team.name"
                                >
                                    <v-list-item-title>
                                        Leg {{ member.leg_order }}: 
                                        <span v-if="member.registration && member.registration.length > 0">
                                            {{ member.registration[0].first_name }} {{ member.registration[0].last_name }}
                                        </span>
                                    </v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-expand-transition>
                </v-list-item>
            </v-list>

            <v-alert v-else type="info">
                No teams registered yet for this race.
            </v-alert>
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
