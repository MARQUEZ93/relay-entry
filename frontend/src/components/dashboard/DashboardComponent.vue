<script>
import api from '@/services/api';

export default {
  name: 'DashboardComponent',
  inject: ['showSnackbar'],
  data() {
    return {
      message: '',
      email: '',
      events: []  // Array to hold user's events
    };
  },
  methods: {
    logout() {
      api.logout();
      this.$router.push('/');
    },
    async fetchEvents() {
      try {
        const response = await api.getUserEvents()  // Fetch user events
        this.events = response.data;
      } catch (error) {
        this.showSnackbar('Error loading events.', 'error');
      }
    },
  },
  async created() {
    try {
      const response = await api.dashboard();
      this.message = response.data.message;
      this.email = response.data.email;
      this.fetchEvents();  // Fetch events when the component is created
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
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="mx-auto" elevation="2">
          <v-card-title class="d-flex justify-space-between">
            <span class="text-h5">{{ email }}</span>
            <v-btn @click="logout" color="error" text>Logout</v-btn>
          </v-card-title>
          <v-card-subtitle class="mt-2">
            {{ message }}
          </v-card-subtitle>

          <v-divider></v-divider>

          <!-- Create Event Box -->
          <v-row class="mt-6" justify="center">
            <v-col cols="12" md="6" lg="4" class="d-flex justify-center">
              <router-link :to="`/dashboard/create-event/`" class="text-decoration-none">
                <v-card class="elevation-2 hoverable">
                  <v-card-title class="d-flex justify-center">
                    <v-icon large color="primary">mdi-calendar-plus</v-icon>
                    <span class="ml-3">Create Event</span>
                  </v-card-title>
                </v-card>
              </router-link>
            </v-col>
          </v-row>

          <!-- Manage Events Box -->
          <v-row class="mt-6" justify="center">
            <v-col cols="12" md="12">
              <v-card class="mx-auto" elevation="2">
                <v-card-title>
                  <v-icon large color="primary">mdi-calendar-check</v-icon>
                  <span class="ml-3">Manage Events</span>
                </v-card-title>

                <v-list>
                  <v-list-item
                    v-for="event in events"
                    :key="event.id"
                    @click="$router.push(`/dashboard/events/${event.id}/`)"
                    rounded="lg"
                    elevation="1"
                  >
                      <v-list-item-title class="text-h6">{{ event.name }} <v-icon class="ml-auto" right>mdi-chevron-right</v-icon></v-list-item-title>
                      <v-list-item-subtitle class="text-body-2">{{ event.date }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>

                <v-card-text v-if="events.length === 0">
                  No events available.
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-card-title {
  font-weight: 600;
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

.text-h5 {
  font-size: 1.5rem;
}

.ml-3 {
  margin-left: 1rem;
}
</style>
