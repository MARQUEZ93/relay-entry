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
        data() {
            return {
                message: '',
                username: '',
                event: {},
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
                <p><strong>Event Name:</strong> {{ event.name }}</p>

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
                    {{ event.description?.length > 100 ? event.description.substring(0, 100) + '...' : event.description }}
                </p>

                 <!-- URL Alias -->
                <p><strong>Event URL: </strong> 
                    <a :href="`${baseUrl}events/${event.url_alias}`" target="_blank">
                    {{ `${baseUrl}events/${event.url_alias}` }}
                    </a>
                </p>
                <!-- Links -->
                <v-row>
                  <v-col cols="3" v-if="event.facebook_url">
                    <p><a :href="event.facebook_url" target="_blank"><strong>Facebook</strong></a></p>
                  </v-col>
                  <v-col cols="3" v-if="event.instagram_url">
                    <p><a :href="event.instagram_url" target="_blank"><strong>Instagram</strong></a></p>
                  </v-col>
                  <v-col v-if="event.twitter_url">
                    <p><a :href="event.twitter_url" target="_blank"><strong>Twitter</strong></a></p>
                  </v-col>
                  <v-col v-if="event.website_url">
                    <p><a :href="event.website_url" target="_blank"><strong>Website</strong></a></p>
                  </v-col>
                </v-row>
                <!-- Waiver Text -->
                <p><strong>Waiver Text:</strong> 
                    {{ event.waiver_text?.length > 100 ? event.waiver_text.substring(0, 100) + '...' : event.waiver_text }}
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
  
      <!-- Fourth Row: List of Races -->
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>My Races<v-spacer></v-spacer></v-card-title>
            <v-list>
              <v-list-item
                v-for="race in races"
                :key="race.id"
                @click="$router.push(`/dashboard/events/${event.id}/races/${race.id}/edit`)"
                class="hoverable"
              >
                <v-list-item-title>{{ race.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ race.distance }}</v-list-item-subtitle>
                <v-list-item-action>
                  <v-icon color="primary">mdi-pencil</v-icon>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card>
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
