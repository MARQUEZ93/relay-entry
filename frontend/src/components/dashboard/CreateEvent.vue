<script>
import api from '@/services/api';

export default {
  name: 'CreateEvent',
  inject: ['showSnackbar'],
  data() {
    return {
      eventData: {
        name: '',
        description: '',
        date: '',
        end_date: '',
        city: '',
        state: '',
        postal_code: '',
        address: '',
        facebook_url: '',
        instagram_url: '',
        twitter_url: '',
        website_url: '',
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
    };
  },
  methods: {
    async createEvent() {
      try {
        // Function to convert empty string fields to null
        const convertEmptyStringsToNull = (data) => {
          const transformedData = { ...data };
          Object.keys(transformedData).forEach(key => {
            if (transformedData[key] === '') {
              transformedData[key] = null;
            }
          });
          return transformedData;
        };

        const eventDataSubmit = convertEmptyStringsToNull(this.eventData);
        await api.createEvent(eventDataSubmit);
        this.showSnackbar('Event created successfully!', 'success');
        this.$router.push('/dashboard');
      } catch (error) {
          let errorMessage = '';
          if (error.response && error.response.data) {
            // Loop through the error data
            for (const [field, messages] of Object.entries(error.response.data)) {
              if (Array.isArray(messages)) {
                errorMessage += `${field}: ${messages.join(', ')}\n`; // Join multiple error messages for the field if it's an array
              } else {
                errorMessage += `${field}: ${messages}\n`; // If it's not an array, append the message directly
              }
            }
          } else {
            // Fallback for unknown errors
            errorMessage = error.response?.data?.message || 'Unknown error occurred';
          }
          this.showSnackbar(`Failed to create event: ${errorMessage}`, 'error');
      }
    },
  },
};
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-btn color="primary" @click="$router.push('/dashboard')">
            <v-icon left>mdi-arrow-left</v-icon>
            Go Back
          </v-btn>
          <v-card-title>
            <span class="headline">Create Event</span>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="createEvent" enctype="multipart/form-data">
              <v-text-field
                v-model="eventData.name"
                label="Event Name *"
                required
              ></v-text-field>

              <v-textarea
                v-model="eventData.description"
                label="Description"
                rows="4"
              ></v-textarea>
              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.address"
                    label="Address"
                  ></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.city"
                    label="City"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.postal_code"
                    label="Zip"
                  ></v-text-field>
                </v-col>

                <v-col cols="6">
                  <v-select
                    v-model="eventData.state"
                    :items="states"
                    label="State"
                  ></v-select>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.date"
                    label="Start Date *"
                    required
                    type="date"
                  ></v-text-field>
                </v-col>

                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.end_date"
                    label="End Date"
                    type="date"
                  ></v-text-field>
                </v-col>
              </v-row>


              <v-text-field
                v-model="eventData.email"
                label="Contact Email *"
                type="email"
                required
              ></v-text-field>

              <v-textarea
                v-model="eventData.waiver_text"
                label="Waiver Text *"
                rows="4"
                required
              ></v-textarea>

              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.facebook_url"
                    label="Facebook URL"
                  ></v-text-field>
                </v-col>

                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.instagram_url"
                    label="Instagram URL"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.twitter_url"
                    label="Twitter URL"
                  ></v-text-field>
                </v-col>

                <v-col cols="6">
                  <v-text-field
                    v-model="eventData.website_url"
                    label="Website URL"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-file-input v-model="localEvent.media_file" label="Event Media"></v-file-input>
                </v-col>
                <v-col cols="6">
                    <v-file-input v-model="localEvent.logo" label="Event Logo"></v-file-input>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-file-input v-model="localEvent.male_tshirt_image" label="Male T-Shirt Image"></v-file-input>
                </v-col>
                <v-col cols="6">
                    <v-file-input v-model="localEvent.female_tshirt_image" label="Female T-Shirt Image"></v-file-input>
                </v-col>
              </v-row>

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

  .v-btn {
    font-weight: bold;
  }
</style>
