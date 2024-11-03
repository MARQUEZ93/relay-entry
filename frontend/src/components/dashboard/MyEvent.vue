<script>
    import api from '@/services/api';
    import EditEventModal from './EditEventModal.vue';

    export default {
        name: 'MyEvent',
        inject: ['showSnackbar'],
        components: {
            EditEventModal,
        },
        mounted() {
            this.baseUrl = process.env.VUE_APP_RE_URL;
        },
        computed: {
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
        data() {
            return {
                message: '',
                username: '',
                event: {},
                races: [],
                editModal: false,
                isValid: false,
                baseUrl: '',
                id: null,
            };
        },
        methods: {
          async openModal() {
            await this.fetchEvent();
            this.editModal = true;
          },
          closeModal() {
            this.editModal = false;
          },
          dashboard() {
              this.$router.push('/dashboard');
          },
          logout() {
              api.logout();
              this.$router.push('/login'); // Ensure logout redirects to login
          },
          async fetchEvent() {
              try {
                  if (!this.id){
                    this.id = this.$route.params.id;
                  }
                  const response = await api.getUserEvent(this.id);  // Fetch event by id
                  this.event = response.data;
                  this.races = response.data.races;
              } catch (error) {
                  this.showSnackbar('Error loading event.', 'error'); // Adjusted message for clarity
              }
          },
        },
        async created() {
            try {
                const response = await api.dashboard(); // Fetch dashboard data
                this.message = response.data.message;
                this.username = response.data.username;

                // Get the event id from the route
                this.id = this.$route.params.id; // Extract event id from URL
                if (this.id) {
                    this.fetchEvent();
                } else {
                    this.showSnackbar('No event ID found in the URL.', 'error');
                }
            } catch (error) {
                this.showSnackbar('Session expired. Log in again.', 'error');
                api.logout();
                this.$router.push('/login');
            }
        },
      };
</script>

<template>
    <v-container class="py-12">
      <!-- First Row: Header -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="mx-auto" elevation="2">
            <v-card-title class="d-flex justify-space-between">
              <span class="text-h4">{{ username }}</span>
              <div>
                <v-btn @click="dashboard" color="primary" class="my-event-v-btn" text>Back</v-btn>
                <v-btn @click="logout" color="error" text>Logout</v-btn>
              </div>
            </v-card-title>
            <v-card-subtitle class="mt-2">{{ message }}</v-card-subtitle>
            <v-divider></v-divider>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Second Row: Event Details -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="mt-6">
            <v-btn color="primary" @click="openModal">Edit</v-btn>
            <v-card-title>
              {{ event.name }}
              <v-spacer></v-spacer>
            </v-card-title>
            <v-card-text>

                <p><strong>Event URL: </strong> 
                    <a :href="`${baseUrl}events/${event.url_alias}`" target="_blank">
                    {{ `${baseUrl}events/${event.url_alias}` }}
                    </a>
                </p>
                <!-- Dates -->
                <p><strong>Start Date:</strong> {{ event.date }}</p>
                <p v-if="event.end_date"><strong>End Date:</strong> {{ event.end_date }}</p>

                <!-- Location -->
                <p><strong>Location:</strong> {{ event.address }}, {{ event.city }}, {{ event.state }}, {{ event.postal_code }}</p>
                <p v-if="event.google_maps_link">
                    <strong>Location Map:</strong> <a :href="event.google_maps_link" target="_blank">View on Google Maps</a>
                </p>

                <!-- Description -->
                <p><strong>Description:</strong> 
                    {{ event.description?.length > 50 ? event.description.substring(0, 50) + '...' : event.description }}
                </p>

                 <!-- URL Alias -->
                <!-- Waiver Text -->
                <p><strong>Waiver Text:</strong> 
                    {{ event.waiver_text?.length > 50 ? event.waiver_text.substring(0, 50) + '...' : event.waiver_text }}
                </p>

                <!-- Created/Updated Dates -->
                <p><strong>Created At:</strong> {{ new Date(event.created_at).toLocaleString() }}</p>
                <p><strong>Last Updated:</strong> {{ new Date(event.updated_at).toLocaleString() }}</p>

                <!-- Published Status -->
                <p><strong>Published (Public URL):</strong> {{ event.published ? 'Yes' : 'No' }}</p>

                <!-- Registration Status -->
                <p><strong>Registration Closed (All races closed):</strong> {{ event.registration_closed ? 'Yes' : 'No' }}</p>
                <!-- T-shirt Images -->
                <div v-if="event.male_tshirt_image || event.female_tshirt_image">
                  <v-row class="d-flex justify-center">
                    <!-- Female T-Shirt Image -->
                    <v-col cols="6" class="text-center">
                      <strong>Female T-Shirt Image</strong>
                      <v-img 
                        v-if="event.female_tshirt_image" 
                        :src="event.female_tshirt_image" 
                        max-width="75" 
                        class="mt-2 d-block mx-auto"
                        alt="Female T-Shirt Image"
                      ></v-img>
                    </v-col>
                    
                    <!-- Male T-Shirt Image -->
                    <v-col cols="6" class="text-center">
                      <strong>Male T-Shirt Image</strong>
                      <v-img 
                        v-if="event.male_tshirt_image" 
                        :src="event.male_tshirt_image" 
                        max-width="75" 
                        class="mt-2 d-block mx-auto"
                        alt="Male T-Shirt Image"
                      ></v-img>
                    </v-col>
                  </v-row>
                </div>
                <!-- Media -->
                <div v-if="event.media_file">
                    <strong>Event Media:</strong>
                    <div class="d-flex justify-center">
                        <v-img :src="event.media_file" max-width="150"></v-img>
                    </div>
                </div>
                <div v-if="event.logo">
                    <strong>Event Image:</strong>
                    <div class="d-flex justify-center">
                        <v-img :src="event.logo" max-width="150"></v-img>
                    </div>
                </div>
                 <v-row v-if="event.facebook_url || event.instagram_url || event.twitter_url || event.website_url">
                  <v-col cols="12" class="d-flex justify-center">
                    <v-card-actions class="social-icons">
                      <v-btn v-for="icon in socialIcons" :key="icon.name" :href="icon.url" target="_blank" icon>
                        <v-icon :class="icon.iconClass">{{ icon.icon }}</v-icon>
                      </v-btn>
                    </v-card-actions>
                  </v-col>
                </v-row>
              </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Third Row: Create Race Section -->
      <v-row justify="center">
        <v-col cols="12" md="6" lg="4" class="d-flex justify-center">
          <router-link :to="`/dashboard/events/${event.id}/create-race/`" class="text-decoration-none">
            <v-card class="elevation-2 hoverable">
              <v-card-title class="d-flex justify-center">
                <v-icon large color="primary">mdi-calendar-plus</v-icon>
                <span class="ml-3">Create Race</span>
              </v-card-title>
            </v-card>
          </router-link>
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="elevation-3">
            <v-card-title class="pb-0">
              <span class="text-h5 font-weight-bold">My Races</span>
            </v-card-title>

            <v-divider class="my-4"></v-divider>

            <v-row v-if="races.length">
              <v-col
                v-for="race in races"
                :key="race.id"
                cols="6"
                md="4"
                class="pb-4"
              >
                <v-card
                  class="hoverable rounded-lg elevation-2 race-card cursor"
                >
                  <v-card-title>
                    {{ race.name }}
                  </v-card-title>
                  <v-card-subtitle class="text-subtitle-1 font-weight-medium">
                    {{ race.distance }}
                  </v-card-subtitle>
                  <v-card-subtitle v-if="race.is_relay">
                    {{ race.team_type }} Relay Race: {{ race.num_runners }} runners
                  </v-card-subtitle>
                  <v-card-subtitle v-if="race.custom_distance_value">
                    {{ race.custom_distance_value }} {{race.custom_distance_unit}}
                  </v-card-subtitle>

                  <v-card-actions class="justify-center">
                    <v-btn
                      icon
                    >
                      <v-icon color="primary">mdi-pencil</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>

            <v-alert v-else type="info" class="mx-4 my-3">
              No races available. Add your first race by clicking the "+" button.
            </v-alert>
          </v-card>

          <v-btn
            fab
            color="primary"
            @click="$router.push(`/dashboard/events/${event.id}/races/create`)"
            class="position-fixed bottom-4 right-4"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <!-- Include the edit modal component -->
        <edit-event-modal
            v-model="editModal"
            :event="event"
            @event-updated="fetchEvent"
            @close-modal="closeModal"
        ></edit-event-modal>
    </v-container>
  </template>
  

<style scoped>
    .v-card-title {
        font-weight: 600;
    }

    .my-event-v-btn {
        margin-right: 3px;
    }
    
    .v-btn {
        font-weight: bold;
    }
    .hoverable {
        transition: transform 0.3s ease;
    }

    .hoverable:hover {
        transform: scale(1.03);
    }

    .text-decoration-none {
        text-decoration: none;
    }

    .text-h4 {
        font-size: 2rem;
    }

    .ml-3 {
        margin-left: 1rem;
    }

</style>
