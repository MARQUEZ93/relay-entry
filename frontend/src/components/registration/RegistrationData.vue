<script>
export default {
  props: {
    race: {
      type: Object,
      required: true,
    },
    registrationData: {
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
      localRegistrationData: {
        ...this.registrationData,
        teamData: {
          name: this.teamData.name,
          projectedTeamTime: this.teamData.projectTeamTime,
          emails: this.teamData.emails,
        },
        projectedTeamTimeChoices: this.race.projected_team_time_choices || [],
        dateOfBirth: this.registrationData.dateOfBirth || '',
        // parentGuardianName: this.registrationData.parentGuardianName || '',
        // parentGuardianSignature: this.registrationData.parentGuardianSignature || '',
        // minor: this.registrationData.minor || false,
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
    registrationData: {
      handler(newVal) {
        this.localRegistrationData = {
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
        this.runnerEmails = {};
        for (let i = 1; i <= this.race.num_runners; i++) {
          this.$set(this.runnerEmails, `participant_${i}_email`, '');
        }
      }
    },
    submit() {
      if (this.$refs.form.validate()) {
        const dataToSubmit = {
          ...this.localRegistrationData,
          teamData: {
            name: this.teamName,  // Include team name
            projectedTeamTime: this.projectedTeamTime,  // Include projected team time
            runnerEmails: this.runnerEmails,  // Include runner emails
          }
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
            v-model="localRegistrationData.teamData.name"
            label="Team Name"
            :rules="nameRules"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="localRegistrationData.teamData.projectedTeamTime"
            :items="projectedTeamTimeChoices"
            label="Projected Team Time"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="(email, index) in runnerEmails" :key="index" cols="12" md="6">
          <v-text-field
            v-model="localRegistrationData.teamData.emails[email]"
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
          v-model="localRegistrationData.firstName"
          :rules="nameRules"
          label="First Name"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRegistrationData.lastName"
          :rules="nameRules"
          label="Last Name"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRegistrationData.email"
          :rules="emailRules"
          label="Email"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRegistrationData.phone"
          :rules="phoneRules"
          label="Phone"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="localRegistrationData.gender"
          :items="genders"
          label="Gender"
          required
        ></v-select>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="localRegistrationData.dateOfBirth"
          label="Date of Birth"
          type="date"
          :rules="dobRules"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <!-- <v-checkbox
      v-model="localRegistrationData.minor"
      label="The registrant is a minor (under 18 years old)"
    ></v-checkbox> -->
    <!-- <v-text-field
      v-if="localRegistrationData.minor"
      :rules="nameRules"
      v-model="localRegistrationData.parentGuardianName"
      label="Parent/Guardian Name"
    ></v-text-field>
    <v-textarea
      v-if="localRegistrationData.minor"
      :rules="nameRules"
      v-model="localRegistrationData.parentGuardianSignature"
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
