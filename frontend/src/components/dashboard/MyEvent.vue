<script>
    import api from '@/services/api';

    export default {
    name: 'MyEvent',
    inject: ['showSnackbar'],
    mounted() {
        this.baseUrl = process.env.VUE_APP_RE_URL;
    },
    data() {
        return {
            message: '',
            username: '',
            email: '',
            event: {},
            editModal: false,
            isValid: false,
            baseUrl: '',
        };
    },
    methods: {
        async updateEvent() {
            if (this.$refs.editForm.validate()) {
            try {
                // Make an API call to update the event
                const response = await api.updateEvent(this.event.id, this.event);
                this.event = response.data;
                this.editModal = false;
                this.showSnackbar('Event updated successfully.', 'success');
            } catch (error) {
                this.showSnackbar('Error updating event.', 'error');
            }
            }
        },
        dashboard() {
            this.$router.push('/dashboard');
        },
        logout() {
            api.logout();
            this.$router.push('/login'); // Ensure logout redirects to login
        },
        async fetchEvent(id) {
            try {
                const response = await api.getUserEvent(id);  // Fetch event by id
                this.event = response.data;
                console.log(this.event);
            } catch (error) {
                this.showSnackbar('Error loading event.', 'error'); // Adjusted message for clarity
            }
        },
    },
    async created() {
        try {
            const response = await api.dashboard(); // Fetch dashboard data
            this.message = response.data.message;
            this.email = response.data.email;

            // Get the event id from the route
            const id = this.$route.params.id; // Extract event id from URL
            if (id) {
                this.fetchEvent(id);
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
              <span class="my-event-span">{{ email }}</span>
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
            <v-btn color="primary" @click="editModal = true">Edit</v-btn>
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

                <!-- Media -->
                <p v-if="event.media_file">
                    <strong>Event Media:</strong> <v-img :src="event.media_file" max-width="150"></v-img>
                </p>
                <div v-if="event.logo">
                    <strong>Event Logo:</strong>
                    <div class="d-flex justify-center">
                        <v-img :src="event.logo" max-width="150"></v-img>
                    </div>
                </div>
                <!-- Social Media Links -->
                <p v-if="event.facebook_url"><strong>Facebook:</strong> <a :href="event.facebook_url" target="_blank">Facebook Page</a></p>
                <p v-if="event.instagram_url"><strong>Instagram:</strong> <a :href="event.instagram_url" target="_blank">Instagram Profile</a></p>
                <p v-if="event.twitter_url"><strong>Twitter:</strong> <a :href="event.twitter_url" target="_blank">Twitter Profile</a></p>

                <!-- Website -->
                <p><strong>Website:</strong> <a :href="event.website_url" target="_blank">{{ event.website_url }}</a></p>

                <!-- Waiver Text -->
                <p><strong>Waiver Text:</strong> 
                    {{ event.waiver_text?.length > 100 ? event.waiver_text.substring(0, 100) + '...' : event.waiver_text }}
                </p>

                <!-- T-shirt Images -->
                <p v-if="event.male_tshirt_image">
                    <strong>Male T-shirt:</strong> <v-img :src="event.male_tshirt_image" max-width="150"></v-img>
                </p>
                <p v-if="event.female_tshirt_image">
                    <strong>Female T-shirt:</strong> <v-img :src="event.female_tshirt_image" max-width="150"></v-img>
                </p>

                <!-- Created/Updated Dates -->
                <p><strong>Created At:</strong> {{ new Date(event.created_at).toLocaleString() }}</p>
                <p><strong>Last Updated:</strong> {{ new Date(event.updated_at).toLocaleString() }}</p>

                <!-- Published Status -->
                <p><strong>Published (Publicly viewable):</strong> {{ event.published ? 'Yes' : 'No' }}</p>

                <!-- Registration Status -->
                <p><strong>Registration Closed (this closes registration for all races):</strong> {{ event.registration_closed ? 'Yes' : 'No' }}</p>
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

    .my-event-span {
        font-size: 1.2rem;
    }

    .ml-3 {
        margin-left: 1rem;
    }

    @media (max-width: 600px) {
        .my-event-span {
            font-size: 1rem;
        }
    }
</style>
