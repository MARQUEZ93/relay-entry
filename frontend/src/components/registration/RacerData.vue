<script>
export default {
  props: {
    race: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      valid: false,
      racerData: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        gender: '',
        dateOfBirth: '',
      },
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length > 1) || 'Name must be more than 1 character',
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      phoneRules: [
        v => !!v || 'Phone is required',
        v => /^\d{10}$/.test(v) || 'Phone must be valid',
      ],
      genders: ['Male', 'Female', 'Other'],
    };
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit('complete', this.racerData);
      }
    },
  },
};
</script>

<template>
  <v-form ref="form" v-model="valid" @submit.prevent="submit">
    <v-text-field
      v-model="racerData.firstName"
      :rules="nameRules"
      label="First Name"
      required
    ></v-text-field>
    <v-text-field
      v-model="racerData.lastName"
      :rules="nameRules"
      label="Last Name"
      required
    ></v-text-field>
    <v-text-field
      v-model="racerData.email"
      :rules="emailRules"
      label="Email"
      required
    ></v-text-field>
    <v-text-field
      v-model="racerData.phone"
      :rules="phoneRules"
      label="Phone"
    ></v-text-field>
    <v-select
      v-model="racerData.gender"
      :items="genders"
      label="Gender"
      required
    ></v-select>
    <v-text-field
      v-model="racerData.dateOfBirth"
      label="Date of Birth"
      type="date"
      required
    ></v-text-field>
    <v-btn @click="submit" :disabled="!valid">Next</v-btn>
  </v-form>
</template>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>
