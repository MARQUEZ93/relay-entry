<script>
import api from '@/services/api';

export default {
  name: 'CreateRace',
  inject: ['showSnackbar'],
  data() {
    return {
      raceData: {
        name: '',
        description: '',
        date: '',
        city: '',
        state: '',
        postal_code: '',
        address: '', 
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
    async createRace() {
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

        const raceDataSubmit = convertEmptyStringsToNull(this.raceData);
        const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB in bytes
        const fileFields = ["course_map",]; 
        for (const field of fileFields) {
          const file = this.eventData[field];  // Dynamically access each field
          if (file && file.size > MAX_FILE_SIZE) {
            console.error(`${field} file size exceeds the allowed limit`);
            this.showSnackbar(`${field} file size exceeds the 5 MB limit.`, 'error');
            return;
          }
        }
        await api.createRace(raceDataSubmit);
        this.showSnackbar('Race created successfully!', 'success');
        this.$router.push('/dashboard');
      } catch (error) {
          console.log(error);
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
          this.showSnackbar(`Failed to create race: ${errorMessage}`, 'error');
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
            <span class="headline">Create Race</span>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="createRace">
              <v-text-field
                v-model="raceData.name"
                label="Race Name *"
                required
              ></v-text-field>

              <v-textarea
                v-model="raceData.description"
                label="Description"
                rows="4"
              ></v-textarea>
                  <v-text-field
                    v-model="raceData.date"
                    label="Date *"
                    required
                    type="date"
                  ></v-text-field>
                   <!-- Distance -->
                <v-select
                v-model="raceData.distance"
                :items="distanceChoices"
                label="Race Distance *"
                required
                ></v-select>

                <!-- Custom Distance (conditionally shown if distance is CUSTOM) -->
                <v-row v-if="raceData.distance === 'Custom'">
                <v-col cols="6">
                    <v-text-field
                    v-model="raceData.custom_distance_value"
                    label="Custom Distance Value"
                    type="number"
                    ></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-select
                    v-model="raceData.custom_distance_unit"
                    :items="distanceUnits"
                    label="Custom Distance Unit"
                    ></v-select>
                </v-col>
                </v-row>

                <!-- Is Relay -->
                <v-switch
                v-model="raceData.is_relay"
                label="Is this a relay race?"
                ></v-switch>

                <!-- Number of Runners (conditionally shown if is_relay is true) -->
                <v-text-field
                v-if="raceData.is_relay"
                v-model="raceData.num_runners"
                label="Number of Runners"
                type="number"
                ></v-text-field>

                <!-- Team Type (conditionally shown if is_relay is true) -->
                <v-select
                v-if="raceData.is_relay"
                v-model="raceData.team_type"
                :items="teamTypeChoices"
                label="Team Type"
                ></v-select>

                <!-- Same Distance Switch (conditionally shown if is_relay is true) -->
                <v-switch
                v-if="raceData.is_relay"
                v-model="raceData.same_distance"
                label="Do all team members run the same distance?"
                ></v-switch>

                <!-- Price -->
                <v-text-field
                v-model="raceData.price"
                label="Registration Price"
                type="number"
                prefix="$"
                ></v-text-field>

                <!-- Course Map Upload -->
                <v-file-input
                v-model="raceData.course_map"
                label="Upload Course Map"
                accept="image/*"
                ></v-file-input>

                <!-- Time Selection -->
                <v-row>
                    <v-col cols="4">
                        <v-select
                        v-model="raceData.hour"
                        :items="hours"
                        label="Hour"
                        ></v-select>
                    </v-col>
                    <v-col cols="4">
                        <v-select
                        v-model="raceData.minute"
                        :items="minutes"
                        label="Minute"
                        ></v-select>
                    </v-col>
                    <v-col cols="4">
                        <v-select
                        v-model="raceData.time_indicator"
                        :items="timeIndicators"
                        label="AM/PM"
                        ></v-select>
                    </v-col>
                </v-row>
              <v-btn type="submit" color="primary" block>Create Race</v-btn>
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
