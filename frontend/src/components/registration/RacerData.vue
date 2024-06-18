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
  computed: {
    firstNameLabel() {
      return this.race.is_relay ? 'Team Captain First Name' : 'First Name';
    },
    lastNameLabel() {
      return this.race.is_relay ? 'Team Captain Last Name' : 'Last Name';
    },
  },
  data() {
    return {
      valid: false,
      localRacerData: {
        ...this.racerData,
        dateOfBirth: this.racerData.dateOfBirth || '',
        parentGuardianName: this.racerData.parentGuardianName || '',
        parentGuardianSignature: this.racerData.parentGuardianSignature || '',
        minor: this.racerData.minor || false,
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
      dobRules: [
        v => !!v || 'Date of Birth is required',
      ],
      teamName: '',  // New data property for team name
      projectedTeamTime: '',  // New data property for projected team time
      runnerEmails: Array(this.race.num_runners).fill(''),  // New data property for runner emails
    };
  },
  watch: {
    racerData: {
      handler(newVal) {
        this.localRacerData = {
          ...newVal,
          dateOfBirth: newVal.dateOfBirth || '',
          parentGuardianName: newVal.parentGuardianName || '',
          parentGuardianSignature: newVal.parentGuardianSignature || '',
          minor: newVal.minor || false,
        };
      },
      deep: true,
    },
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        const dataToSubmit = {
          ...this.localRacerData,
          teamName: this.teamName,  // Include team name
          projectedTeamTime: this.projectedTeamTime,  // Include projected team time
          runnerEmails: this.runnerEmails,  // Include runner emails
        };
      this.$emit('complete', dataToSubmit);
      }
    },
  },
};
</script>


<template>
  <v-form ref="form" v-model="valid" @submit.prevent="submit">
    <template v-if="race.is_relay">
      <v-text-field
        v-model="teamName"
        label="Team Name"
        :rules="nameRules"
        required
      ></v-text-field>
      <v-text-field
        v-model="projectedTeamTime"
        label="Projected Team Time"
        placeholder="HH:MM:SS"
        required
      ></v-text-field>
      <div v-for="(email, index) in runnerEmails" :key="index">
        <v-text-field
          v-model="runnerEmails[index]"
          :rules="emailRules"
          :label="`Leg ${index + 1} Runner Email`"
          required
        ></v-text-field>
      </div>
    </template>
    <v-text-field
      v-model="localRacerData.firstName"
      :rules="nameRules"
      :label="firstNameLabel"
      required
    ></v-text-field>
    <v-text-field
      v-model="localRacerData.lastName"
      :rules="nameRules"
      :label="lastNameLabel"
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
    <v-checkbox
      v-model="localRacerData.minor"
      label="The registrant is a minor (under 18 years old)"
    ></v-checkbox>
    <v-text-field
      v-if="localRacerData.minor"
      :rules="nameRules"
      v-model="localRacerData.parentGuardianName"
      label="Parent/Guardian Name"
    ></v-text-field>
    <v-textarea
      v-if="localRacerData.minor"
      :rules="nameRules"
      v-model="localRacerData.parentGuardianSignature"
      label="Parent/Guardian Signature"
    ></v-textarea>
    <v-btn type="submit" color="primary" :disabled="!valid">Next</v-btn>
  </v-form>
</template>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>
