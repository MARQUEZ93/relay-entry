<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  inject: ['showSnackbar'],
  data() {
    return {
      team: null,  // Will hold the team data
      event: null,
    };
  },
  created() {
    const token = this.$route.params.token;
    this.fetchTeamData(token);
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
    goToEventPage() {
      this.$router.push({ name: 'Event', params: { eventUrlAlias: this.event.url_alias } });
    },
    formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute,
    fetchTeamData(token) {
      api.getTeamData(token)
        .then(response => {
          this.team = response.data.team;
          this.event = response.data.event;
        })
        .catch((e) => {
          this.showSnackbar(`An error occurred while fetching data: ${e.response.data.error}`, 'error');
          setTimeout(() => {
            this.$router.push({ name: 'HomeComponent' });
          }, 5000);
        });
    },
    updateTeam() {
      const token = this.$route.params.token;
      api.updateTeam(token, this.team)
        .then((response) => {
          this.showSnackbar(response.data.message, 'info');
          // Wait 5 seconds, then toggle back to the previous state
          setTimeout(() => {
            this.goToEventPage();
          }, 5000);
        })
        .catch((e) => {
          this.showSnackbar(`An error occurred while updating the team: ${e.response.data.error}`, 'error');
        });
    },
  }
};
</script>
<template>
  <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-btn color="primary" @click="goToEventPage">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Event Page
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
        <v-col v-if="event">
            <v-card class="mx-auto my-5 pa-5">
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
    <h1 class="mb-2">Update Team</h1>
    <v-row justify="center mb-5" v-if="team">
      <v-col cols="12" md="6">
        <v-form @submit.prevent="updateTeam">
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="team.name"
                label="Team Name"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="6">
              <v-select
                v-model="team.projected_team_time"
                :items="team.projected_team_time_choices"
                label="Projected Team Time"
                required
              ></v-select>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>
          <div class="text-subtitle-1 mb-2">Team Members</div>
          <v-row v-for="index in Math.ceil(team.members.length / 2)" :key="index">
            <!-- First text field for the current pair -->
            <v-col cols="6">
              <v-text-field
                v-model="team.members[(index - 1) * 2].email"
                :label="`Leg ${team.members[(index - 1) * 2].leg_order} Email`"
                type="email"
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                required
              ></v-text-field>
            </v-col>

            <!-- Second text field for the current pair, if it exists -->
            <v-col cols="6" v-if="team.members[(index - 1) * 2 + 1]">
              <v-text-field
                v-model="team.members[(index - 1) * 2 + 1].email"
                :label="`Leg ${team.members[(index - 1) * 2 + 1].leg_order} Email`"
                type="email"
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-divider class="my-4"></v-divider>
          <v-btn type="submit" color="primary">Update Team</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>
