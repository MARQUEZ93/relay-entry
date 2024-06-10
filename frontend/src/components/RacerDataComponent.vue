<template>
    <v-card>
      <v-card-title>
        <h2>Racer Data</h2>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field v-model="racer.name" :rules="[rules.required]" label="Name"></v-text-field>
          <v-text-field v-model="racer.email" :rules="[rules.required, rules.email]" label="Email"></v-text-field>
          <v-text-field v-model="racer.dob" :rules="[rules.required]" label="Date of Birth"></v-text-field>
          <!-- Add more fields as necessary -->
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="$emit('previous')">Back</v-btn>
        <v-btn :disabled="!valid" @click="nextStep">Next</v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script>
  export default {
    data() {
      return {
        valid: false,
        racer: {
          name: '',
          email: '',
          dob: '',
          // Add more fields as necessary
        },
        rules: {
          required: value => !!value || 'Required.',
          email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
        },
      };
    },
    methods: {
      nextStep() {
        if (this.$refs.form.validate()) {
          this.$emit('next', this.racer);
        }
      },
    },
  };
  </script>
  