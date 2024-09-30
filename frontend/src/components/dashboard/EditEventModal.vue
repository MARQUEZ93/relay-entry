<script>
export default {
  props: {
    modelValue: Boolean,
    event: Object
  },
  data() {
    return {
        states: [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ],
        isValid: false,
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
    updateEvent() {
      if (this.$refs.editForm.validate()) {
        this.$emit('update-event', this.localEvent); // Emit the updated localEvent object
        this.$emit('update:modelValue', false); // Close the modal by emitting update:modelValue
      }
    }
  }
};
</script>

<template>
  <v-dialog :model-value="modelValue" @update:modelValue="$emit('update:modelValue', $event)" max-width="800px">
    <!-- Adjust the width here by changing max-width -->
    <v-card>
      <v-card-title>Edit Event</v-card-title>
      <v-card-text>
        <v-form ref="editForm" v-model="isValid">
          
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

          <!-- Media fields: Combine Media and Logo -->
          <v-row>
            <v-col cols="6">
              <v-file-input v-model="localEvent.media_file" label="Event Media"></v-file-input>
            </v-col>
            <v-col cols="6">
                <v-file-input v-model="localEvent.logo" label="Event Logo"></v-file-input>
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
                <v-checkbox v-model="localEvent.registration_closed" label="Registration Closed (closes registration for all races)"></v-checkbox>
            </v-col>
          </v-row>

        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="updateEvent">Save</v-btn>
        <v-btn @click="$emit('update:modelValue', false)">Cancel</v-btn> <!-- Emit event to close -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
