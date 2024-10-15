<script>
import api from '@/services/api';

export default {
  name: 'CreateRace',
  inject: ['showSnackbar'],
  mounted(){
    if (process.env.NODE_ENV === 'development'){
        this.fillForm();
    }
  },
  computed: {
    projectedTeamTimeInput: {
      get() {
        // Convert array to comma-separated string for display
        return this.raceData.projected_time_choices.join(', ');
      },
      set(value) {
        // Convert comma-separated string to array for saving
        this.raceData.projected_time_choices = value.split(',').map(time => time.trim());
      }
    }
  },
  async created() {
    console.log(this.$route.params);
    this.raceData.event = this.$route.params.eventId;
  },
  data() {
    return {
      raceData: {
        name: '',
        event: '',
        description: '',
        date: '',
        city: '',
        state: '',
        postal_code: '',
        address: '', 
        distance: '',
        custom_distance_value: '',
        custom_distance_unit: '',
        is_relay: false,
        num_runners: null,
        team_type: '',
        same_distance: false,
        price: '',
        course_map: null,
        hour: '',
        minute: '',
        time_indicator: 'AM',
        projected_time_choices: [],
        // TODO: FORMAT to choices
        projectedTimeInput: '', // This will store the user's comma-separated input
      },
      states: [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
      ],
      distanceChoices: ['5K', '10K', 'Half Marathon', 'Marathon', 'Ultra Marathon', 'Custom' ], 
      distanceUnits: ['km', 'mi'],
      teamTypeChoices: ['Male', 'Female', 'Mixed'],
      hours: Array.from({ length: 12 }, (_, i) => i + 1), // [1, 2, 3, ..., 12]
      minutes: ['00', '15', '30', '45'],
      timeIndicators: ['AM', 'PM'],
    };
  },
  methods: {
    fillForm(){
        this.raceData = {
            name: 'Race Name',
            description: 'Description',
            postal_code: '75244',
            city: 'Austin',
            event: 1,
            state: 'TX',
            address: '123 Test Address',
            num_runners: 5,
            is_relay: true,
            custom_distance_unit: 'mi',
            custom_distance_value: 2,
            hour: '11',
            minute: '45',
            price: 20,
            team_type: 'Male',
            time_indicator: 'AM',
        };
    },
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
          const file = this.raceData[field];  // Dynamically access each field
          if (file && file.size > MAX_FILE_SIZE) {
            console.error(`${field} file size exceeds the allowed limit`);
            this.showSnackbar(`${field} file size exceeds the 5 MB limit.`, 'error');
            return;
          }
        }
        console.log(raceDataSubmit);
        await api.createRace(raceDataSubmit);
        this.showSnackbar('Race created successfully!', 'success');
        // TODO: push to event page
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
            <!-- TODO: GO BACK TO EVENT -->
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
                <v-row>
                    <v-col cols="6">
                        <v-text-field
                            v-model="raceData.date"
                            label="Date *"
                            required
                            type="date"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-text-field
                            v-model="raceData.price"
                            label="Registration Price *"
                            type="number"
                            prefix="$"
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-card-subtitle>
                    <span class="headline">If Race has Address different from Event</span>
                </v-card-subtitle>
                <v-row>
                    <v-col cols="6">
                        <v-text-field
                            v-model="raceData.address"
                            label="Address"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-text-field
                            v-model="raceData.city"
                            label="City"
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6">
                    <v-text-field
                        v-model="raceData.postal_code"
                        label="Zip"
                    ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                    <v-select
                        v-model="raceData.state"
                        :items="states"
                        label="State"
                    ></v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6">
                        <v-switch
                            v-model="raceData.is_relay"
                            label="Is this a relay race?"
                        ></v-switch>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="raceData.distance"
                            :items="distanceChoices"
                            label="Race Distance *"
                            required
                        ></v-select>
                    </v-col>
                </v-row>
                <v-row v-if="raceData.distance === 'Custom'">
                    <v-col cols="6">
                        <v-text-field
                            v-model="raceData.custom_distance_value"
                            label="Distance Value"
                            type="number"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <v-select
                            v-model="raceData.custom_distance_unit"
                            :items="distanceUnits"
                            label="Distance Unit"
                        ></v-select>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="6">
                        <!-- Number of Runners (conditionally shown if is_relay is true) -->
                        <v-text-field
                            v-if="raceData.is_relay"
                            v-model="raceData.num_runners"
                            label="Runners per Team"
                            type="number"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                        <!-- Team Type (conditionally shown if is_relay is true) -->
                        <v-select
                            v-if="raceData.is_relay"
                            clearable
                            v-model="raceData.team_type"
                            :items="teamTypeChoices"
                            label="Gender Type"
                        ></v-select>
                    </v-col>
                </v-row>
                <!-- Same Distance Switch (conditionally shown if is_relay is true) -->
                <v-switch
                    v-if="raceData.is_relay"
                    v-model="raceData.same_distance"
                    label="Do all team members run the same distance?"
                ></v-switch>

                <!-- Course Map Upload -->
                <v-file-input
                    v-model="raceData.course_map"
                    label="Upload Course Map"
                    accept="image/*"
                ></v-file-input>

                <v-text-field
                    v-model="raceData.projectedTimeInput"
                    label="Projected Times (e.g. 9:00/mile, 8:30/mile)"
                    placeholder="Enter times seperated by comma"
                ></v-text-field>

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
