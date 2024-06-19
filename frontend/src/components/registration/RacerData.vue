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
  created() {
    this.initializeRunnerEmails();
  },
  data() {
    return {
      valid: false,
      localRacerData: {
        ...this.racerData,
        dateOfBirth: this.racerData.dateOfBirth || '',
        parentGuardianName: this.racerData.parentGuardianName || '',
        parentGuardianSignature: this.racerData.parentGuardianSignature || '',
        // minor: this.racerData.minor || false,
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
      runnerEmails: [],  // New data property for runner emails
    };
  },
  watch: {
    race: {
      handler() {
        this.initializeRunnerEmails();
      },
      deep: true,
      immediate: true,
    },
    racerData: {
      handler(newVal) {
        this.localRacerData = {
          ...newVal,
          dateOfBirth: newVal.dateOfBirth || '',
          parentGuardianName: newVal.parentGuardianName || '',
          parentGuardianSignature: newVal.parentGuardianSignature || '',
          // minor: newVal.minor || false,
        };
      },
      deep: true,
    },
  },
  methods: {
    initializeRunnerEmails() {
      if (this.race && this.race.num_runners) {
        this.runnerEmails = Array(this.race.num_runners).fill('');
      }
    },
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
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="teamName"
            label="Team Name"
            :rules="nameRules"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="projectedTeamTime"
            label="Projected Team Time"
            placeholder="HH:MM:SS"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="(email, index) in runnerEmails" :key="index" cols="12" md="6">
          <v-text-field
            v-model="runnerEmails[index]"
            :rules="emailRules"
            :label="`Leg ${index + 1} Runner Email`"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </template>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRacerData.firstName"
          :rules="nameRules"
          label="First Name"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRacerData.lastName"
          :rules="nameRules"
          label="Last Name"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRacerData.email"
          :rules="emailRules"
          label="Email"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRacerData.phone"
          :rules="phoneRules"
          label="Phone"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="localRacerData.gender"
          :items="genders"
          label="Gender"
          required
        ></v-select>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRacerData.dateOfBirth"
          label="Date of Birth"
          type="date"
          :rules="dobRules"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <!-- <v-checkbox
      v-model="localRacerData.minor"
      label="The registrant is a minor (under 18 years old)"
    ></v-checkbox> -->
    <!-- <v-text-field
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
    ></v-textarea> -->
    <v-btn type="submit" color="primary" :disabled="!valid">Next</v-btn>
  </v-form>
</template>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>
