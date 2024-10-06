<script>
import api from '@/services/api';
export default {
  props: {
    event: Object
  },
  inject: ['showSnackbar'],
  data() {
    return {
        states: [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ],
        localEvent: { ...this.event } // Create a local copy of the event prop
    };
  },
  watch: {
    event: {
      immediate: true,
      handler(newValue) {
        this.localEvent = { ...newValue }; // Update localEvent when the prop changes
      }
    }
  },
  methods: {
    async updateEvent(updatedEvent) {
        try {
          const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB in bytes
          const fileFields = ['logo', 'media_file', 'male_tshirt_image', 'female_tshirt_image']; 
          for (const field of fileFields) {
            const file = this.localEvent[field];  // Dynamically access each field
            if (file && file.size > MAX_FILE_SIZE) {
              console.error(`${field} file size exceeds the allowed limit`);
              this.showSnackbar(`${field} file size exceeds the 5 MB limit.`, 'error');
              return;
            }
          }
          // Detect which fields have changed
          const updatedFields = {};
          Object.entries(this.localEvent).forEach(([key, value]) => {
            // Only include fields that have changed
            if (value !== this.event[key]) {
              updatedFields[key] = value;
            }
          });

          await api.updateEvent(updatedEvent.id, updatedFields);
          this.showSnackbar('Event updated successfully', 'success');
          this.$emit('event-updated');  // Emit a custom event to refresh the event
        } catch (error) {
            let errorMessage = '';
            if (error.response && error.response.data) {
                for (const [field, messages] of Object.entries(error.response.data)) {
                if (Array.isArray(messages)) {
                    errorMessage += `${field}: ${messages.join(', ')}\n`;
                } else {
                    errorMessage += `${field}: ${messages}\n`;
                }
                }
            } else {
                errorMessage = error.response?.data?.message || 'Unknown error occurred';
            }
            this.showSnackbar(`Failed to update event: ${errorMessage}`, 'error');
        } finally {
            this.$emit('close-modal');
        }
    },
    updateEventClick() {
      if (this.$refs.editForm.validate()) {
        this.updateEvent(this.localEvent);
        this.$emit('close-modal');
      }
    }
  }
};
</script>

<template>
  <v-dialog max-width="800px">
    <!-- Adjust the width here by changing max-width -->
    <v-card>
      <v-card-title>Edit Event</v-card-title>
      <v-card-text>
        <v-form ref="editForm" enctype="multipart/form-data">
          
          <!-- Event Name -->
          <v-text-field v-model="localEvent.name" label="Event Name" required></v-text-field>
          <v-textarea v-model="localEvent.description" label="Description" rows="3"></v-textarea>
          
          <!-- Dates: Combine Start and End Dates into a single row -->
          <v-row>
            <v-col cols="6">
              <v-text-field v-model="localEvent.date" label="Start Date" type="date" required></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="localEvent.end_date" label="End Date" type="date"></v-text-field>
            </v-col>
          </v-row>

          <!-- Address: Combine Address, City, State, and Postal Code -->
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="localEvent.address" label="Address"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="5">
              <v-text-field v-model="localEvent.city" label="City"></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-select v-model="localEvent.state" :items="states" label="State"></v-select>
            </v-col>
            <v-col cols="4">
              <v-text-field v-model="localEvent.postal_code" label="Zip"></v-text-field>
            </v-col>
          </v-row>

          <!-- Google Maps Link -->
          <v-text-field v-model="localEvent.google_maps_link" label="Google Maps Link"></v-text-field>

          <!-- Media fields-->
          <v-row>
            <v-col cols="6">
              <v-file-input accept="image/*" v-model="localEvent.media_file" label="Event Media"></v-file-input>
            </v-col>
            <v-col cols="6">
                <v-file-input accept="image/*" v-model="localEvent.logo" label="Event Image"></v-file-input>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="6">
              <v-file-input accept="image/*" v-model="localEvent.male_tshirt_image" label="Male T-Shirt Image"></v-file-input>
            </v-col>
            <v-col cols="6">
                <v-file-input accept="image/*" v-model="localEvent.female_tshirt_image" label="Female T-Shirt Image"></v-file-input>
            </v-col>
          </v-row>

          <!-- Social Media Links: Combine in two columns -->
          <v-row>
            <v-col cols="6">
              <v-text-field v-model="localEvent.website_url" label="Website URL"></v-text-field>
              <v-text-field v-model="localEvent.facebook_url" label="Facebook URL"></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="localEvent.instagram_url" label="Instagram URL"></v-text-field>
              <v-text-field v-model="localEvent.twitter_url" label="Twitter URL"></v-text-field>
            </v-col>
          </v-row>

          <!-- Waiver Text: Keep full-width since it's a large field -->
          <v-textarea v-model="localEvent.waiver_text" label="Waiver Text" rows="4"></v-textarea>
          <v-row>
            <v-col cols="6">
                <!-- Checkboxes: Published and Registration Closed -->
                <v-checkbox v-model="localEvent.published" label="Published"></v-checkbox>
            </v-col>
            <v-col cols="6">
                <v-checkbox v-model="localEvent.registration_closed" label="Registration Closed (All races closed)"></v-checkbox>
            </v-col>
          </v-row>

        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="updateEventClick">Save</v-btn>
        <v-btn @click="$emit('close-modal')">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
