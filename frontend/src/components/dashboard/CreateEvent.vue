<script>
  import api from '@/services/api';
  
  export default {
    name: 'CreateEvent',
    data() {
      return {
        eventData: {
          name: '',
          description: '',
          date: '',
          end_date: '',
          city: '',
          state: '',
          email: '',
          waiver_text: '',
          published: false,
        },
        states: [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ],
        menu: false,
        menu2: false,
      };
    },
    methods: {
      async createEvent() {
        try {
          await api.post('/events/create/', this.eventData);
          this.$router.push('/events'); // Redirect to the events page
          this.$emit('showSnackbar', 'Event created successfully!', 'success');
        } catch (error) {
          this.$emit('showSnackbar', 'Failed to create event.', 'error');
        }
      },
    },
    beforeCreate() {
      if (!localStorage.getItem('access_token')) {
        this.$router.push('/login'); // Redirect to login if not authenticated
      }
    },
  };
  </script>

<template>
    <v-container class="fill-height" fluid>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6">
          <v-card>
            <v-card-title>
              <span class="headline">Create Event</span>
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="createEvent">
                <v-text-field
                  v-model="eventData.name"
                  label="Event Name"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="eventData.description"
                  label="Description"
                  rows="4"
                ></v-textarea>
                <v-menu
                  ref="menu"
                  v-model="menu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="eventData.date"
                      label="Start Date"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="eventData.date" @input="menu = false"></v-date-picker>
                </v-menu>
                <v-menu
                  ref="menu2"
                  v-model="menu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="eventData.end_date"
                      label="End Date"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="eventData.end_date" @input="menu2 = false"></v-date-picker>
                </v-menu>
                <v-text-field
                  v-model="eventData.city"
                  label="City"
                ></v-text-field>
                <v-select
                  v-model="eventData.state"
                  :items="states"
                  label="State"
                  required
                ></v-select>
                <v-text-field
                  v-model="eventData.email"
                  label="Contact Email"
                  type="email"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="eventData.waiver_text"
                  label="Waiver Text"
                  rows="4"
                  required
                ></v-textarea>
                <v-checkbox
                  v-model="eventData.published"
                  label="Published"
                ></v-checkbox>
                <v-btn type="submit" color="primary" block>Create Event</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <style scoped>
  .headline {
    font-weight: bold;
  }
  </style>
  