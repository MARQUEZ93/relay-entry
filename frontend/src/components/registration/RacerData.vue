<script>
export default {
  props: {
    race: {
      type: Object,
      required: true,
    },
    racerData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      valid: false,
      localRacerData: { ...this.racerData }, // Initialize local state with prop data
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
      dobRules: [
        v => !!v || 'Date of Birth is required',
      ],
    };
  },
  watch: {
    racerData: {
      handler(newVal) {
        this.localRacerData = { ...newVal };
      },
      deep: true,
    },
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit('complete', this.localRacerData);
      }
    },
  },
};
</script>


<template>
  <v-form ref="form" v-model="valid" @submit.prevent="submit">
    <v-text-field
      v-model="localRacerData.firstName"
      :rules="nameRules"
      label="First Name"
      required
    ></v-text-field>
    <v-text-field
      v-model="localRacerData.lastName"
      :rules="nameRules"
      label="Last Name"
      required
    ></v-text-field>
    <v-text-field
      v-model="localRacerData.email"
      :rules="emailRules"
      label="Email"
      required
    ></v-text-field>
    <v-text-field
      v-model="localRacerData.phone"
      :rules="phoneRules"
      label="Phone"
      required
    ></v-text-field>
    <v-select
      v-model="localRacerData.gender"
      :items="genders"
      label="Gender"
      required
    ></v-select>
    <v-text-field
      v-model="localRacerData.dateOfBirth"
      label="Date of Birth"
      type="date"
      :rules="dobRules"
      required
    ></v-text-field>
    <v-btn type="submit" color="primary" :disabled="!valid">Next</v-btn>
  </v-form>
</template>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>
