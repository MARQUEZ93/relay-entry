<script>
import api from '@/services/api';
import { formattedRaceDate, customSameDistance, formatDateToUTC, formatMinute } from '@/utils/methods';

export default {
  name: 'EventComponent',
  inject: ['showSnackbar'],
  data() {
    return {
      event: {},
      loading: true,
      error: null,
      manageTeam: false,
      confirmRegistration: false,
      manageTeamEmail: '',
      confirmName: '',
      confirmationResults: [],
      confirmRegistrationHeaders: [
        { title: 'Name', value: 'full_name', key: 'full_name', sortable: false, align: 'center' },
        { title: 'Race', value: 'race__name', key: 'race__name', sortable: false, align: 'center' },
        { title: 'Team (If Applicable)', value: 'team_name', key: 'team_name', sortable: false, align: 'center' },
      ],
    };
  },
  computed: {
    eventHasRelayRace() {
      if (this.event && this.event.races) {
        return this.event.races.some(race => race.is_relay);
      }
      return false;
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
    clearName(){
      this.confirmName = '';
      this.confirmationResults = [];
    },
    confirmRegistrationQuery() {
      if (!this.confirmName || !this.event){
        this.showSnackbar('An error occurred while confirming registration', 'error');
        this.confirmName = '';
        this.confirmationResults = [];
        return;
      }
      if (this.confirmName.length < 3){
        this.showSnackbar('Input needs to be at least 3 characters long.', 'error');
        return;
      }
      api.confirmEventRegistration(this.event.url_alias, this.confirmName).then(response => {
        this.confirmationResults = response.data;
      })
      .catch( (e) => {
        this.showSnackbar(`An error occurred while confirming registration: ${e.response.data.error}`, 'error');
        this.confirmName = '';
        this.confirmationResults = [];
      });
    },
    sendManageTeamLink() {
      if (!this.manageTeamEmail || !this.eventHasRelayRace || !this.event){
        this.showSnackbar('An error occurred while sending the link.', 'error');
        this.manageTeamEmail = '';
        return;
      }
      api.requestEditLink(this.event.url_alias, {
        eventId: this.event.id,
        email: this.manageTeamEmail
      }).then(response => {
        this.showSnackbar(response?.data?.message, 'info');
        this.manageTeamEmail = '';
        this.toggleManageTeam();
      })
      .catch( () => {
        this.showSnackbar('An error occurred while sending the link.', 'error');
        this.manageTeamEmail = '';
      });
    },
    getRegisterButtonText(race) {
      return race.registration_closed ? 'Closed' : (race.is_relay ? 'Register Team' : 'Register');
    },
    formatPrice(price) {
      return Number(price).toFixed(2);
    },
    toggleManageTeam() {
      this.manageTeam = !this.manageTeam;
      if (this.manageTeam && this.confirmRegistration){
        this.confirmRegistration = false;
      }
    },
    toggleConfirmRegistration() {
      this.confirmRegistration = !this.confirmRegistration;
      if (this.confirmRegistration && this.manageTeam){
        this.manageTeam = false;
      }
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
      this.$router.push({ path: '/' });
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
          <!-- <v-card-subtitle v-if="event.google_maps_link">
            <p><a :href="event.google_maps_link" target="_blank">View on Google Maps</a></p>
          </v-card-subtitle> -->
          <!-- <v-card-subtitle v-if="event.google_maps_html">
            <p v-html="event.google_maps_html"></p>
          </v-card-subtitle> -->
          <v-card-text v-if="event.description">
            {{ event.description }}
          </v-card-text>
          <v-card-actions class="social-icons">
            <v-btn v-for="icon in socialIcons" :key="icon.name" :href="icon.url" target="_blank" icon>
              <v-icon :class="icon.iconClass">{{ icon.icon }}</v-icon>
            </v-btn>
          </v-card-actions>
          <v-card-actions class="d-flex flex-row justify-center align-center" v-if="eventHasRelayRace">
            <router-link :to="`/events/${event.url_alias}/teams`">
              <v-btn color="primary">Registered Teams</v-btn>
            </router-link>
            ·
            <v-btn :disabled="manageTeam" @click="toggleManageTeam" color="primary">My Team</v-btn>
          </v-card-actions>
          <v-card-actions class="d-flex flex-row justify-center align-center" v-if="eventHasRelayRace">
            <router-link :to="`/events/${event.url_alias}/team-results`">
              <v-btn color="primary">Results</v-btn>
            </router-link>
            ·
            <v-btn :disabled="confirmRegistration" @click="toggleConfirmRegistration" color="primary">Confirm Registration</v-btn>
          </v-card-actions>
          <v-card-actions class="d-flex flex-column align-center" v-if="!event.registration_closed">
            <router-link :to="`/events/${event.url_alias}/register`">
              <v-btn color="primary">Register & Sign Waiver</v-btn>
            </router-link>
            <div class="help-text mt-2 text-center"><strong>Team Members: </strong>Register & sign the waiver above. <strong>Team Captains:</strong> Register your team & yourself below.</div>
          </v-card-actions>
        </v-card>
        <v-container class="mt-5" v-if="confirmRegistration">
          <v-row class="justify-center mb-5">
            <v-col cols="12" md="8">
              <v-btn color="primary" @click="toggleConfirmRegistration">
                <v-icon left>mdi-arrow-left</v-icon>
                Go Back
              </v-btn>
            </v-col>
          </v-row>
          <v-alert type="info" class="mt-5 mb-5">
            Enter Name to Confirm Registration
          </v-alert>
          <v-row class="justify-center mb-5">
            <v-col cols="9" md="6">
              <v-form @submit.prevent="confirmRegistrationQuery">
                <v-text-field
                  v-model="confirmName"
                  label="Enter name"
                  required
                ></v-text-field>
                <v-btn class="mb-2" type="submit" color="primary">Confirm Registration</v-btn>
                <v-btn :disabled="!confirmName" @click="clearName" color="secondary">Reset</v-btn>
              </v-form>
            </v-col>
          </v-row>
          <v-row class="justify-center mt-5" v-if="confirmationResults && confirmationResults.length">
            <v-col cols="12" md="8">
              <v-data-table
                :headers="confirmRegistrationHeaders"
                :items="confirmationResults"
                class="elevation-1"
              >
                <template v-slot:[`item.full_name`]="{ item }">
                  {{ item.full_name }}
                </template>
                <template v-slot:[`item.race__name`]="{ item }">
                  {{ item.race__name }}
                </template>
                <template v-slot:[`item.team_name`]="{ item }">
                  {{ item.team_name ? item.team_name : '' }}
                </template>
                <template v-slot:no-data>
                  <v-alert :value="true" color="error" icon="mdi-alert">
                    No registrations for this name
                  </v-alert>
                </template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-container>
        <v-container class="mt-5" v-if="manageTeam">
          <v-row class="justify-center mb-5">
            <v-col cols="12" md="8">
              <v-btn color="primary" @click="toggleManageTeam">
                <v-icon left>mdi-arrow-left</v-icon>
                Go Back
              </v-btn>
            </v-col>
          </v-row>
          <v-alert type="info" class="mt-5 mb-5">
            Please enter the email associated with the team captain who registered. 
            This email will be used to send a link for managing your team.
          </v-alert>
          <v-row class="justify-center mb-5">
            <v-col cols="9" md="6">
              <v-form @submit.prevent="sendManageTeamLink">
                <v-text-field
                  v-model="manageTeamEmail"
                  label="Team captain email"
                  type="email"
                  :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                  required
                ></v-text-field>
                <v-btn type="submit" color="primary">Send Link</v-btn>
              </v-form>
            </v-col>
          </v-row>
        </v-container>
        <v-row v-if="!manageTeam && !confirmRegistration">
          <v-col
            v-for="race in event.races"
            :key="'race-' + race.id"
            cols="6"
            md="4"
            class="d-flex align-center justify-center"
          >
            <v-card class="mx-auto my-3 race-card" outlined>
              <v-card-title v-if="race.name" class="d-flex align-center justify-center">
                <span>{{ race.name }}</span>
                <v-icon v-if="race.description" size="x-small" class="ml-2" color="primary" v-tooltip.top="race.description">
                  mdi-information
                </v-icon>
              </v-card-title>
              <v-card-subtitle v-if="race.is_relay && race.same_distance && race.custom_distance_value && race.custom_distance_unit">
                {{race.num_runners }} x {{customSameDistance(race)}}
              </v-card-subtitle>
              <v-card-subtitle>
                {{ race.hour }}:{{ formatMinute(race.minute) }} {{ race.time_indicator }}
              </v-card-subtitle>
              <v-card-subtitle>
                ${{ formatPrice(race.price) }}
              </v-card-subtitle>
              <v-card-actions class="justify-center">
                <router-link :to="`/events/${event.url_alias}/${race.id}`">
                  <v-btn :disabled="race.registration_closed" :color="race.registration_closed ? 'red' : 'primary'">{{ getRegisterButtonText(race) }}</v-btn>
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
</style>
