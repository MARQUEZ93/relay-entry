<template>
    <v-card>
      <v-card-title>
        <h2>Waiver</h2>
      </v-card-title>
      <v-card-text>
        <p>Please read and accept the waiver to proceed.</p>
        <!-- Display the waiver text here -->
        <v-checkbox
          v-model="accepted"
          label="I have read and accept the waiver"
        ></v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-btn :disabled="!accepted" @click="$emit('next')">Next</v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script>
  export default {
    data() {
      return {
        accepted: false,
      };
    },
  };
  </script>
  