<script>
import api from '@/services/api';

export default {
  name: 'MyEvent',
  inject: ['showSnackbar'],
  data() {
    return {
      message: '',
      username: '',
      email: '',
      event: {}
    };
  },
  methods: {
    logout() {
      api.logout();
      this.$router.push('/login'); // Ensure logout redirects to login
    },
    async fetchEvent(id) {
      try {
        const response = await api.getUserEvent(id);  // Fetch event by id
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
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="mx-auto" elevation="2">
          <v-card-title class="d-flex justify-space-between">
            <span class="text-h5">Dashboard - {{ username }}</span>
            <v-btn @click="logout" color="error" text>Logout</v-btn>
          </v-card-title>
          <v-card-subtitle class="mt-2">
            {{ message }}
          </v-card-subtitle>

          <v-divider></v-divider>

          <!-- Create Race Box -->
          <v-row class="mt-6" justify="center">
            <v-col cols="12" md="6" lg="4" class="d-flex justify-center">
              <!-- Fixed dynamic router-link -->
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
          <v-row>
            <v-col>
                <v-list>
                <v-subheader>My Races</v-subheader>
                <v-list-item
                    v-for="race in races"
                    :key="race.id"
                    @click="$router.push(`/dashboard/events/${event.id}/races/${race.id}/edit`)"
                    class="hoverable"
                >
                    <v-list-item-content>
                    <v-list-item-title>{{ race.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ race.distance }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                    <v-icon color="primary">mdi-pencil</v-icon>
                    </v-list-item-action>
                </v-list-item>
                </v-list>
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
