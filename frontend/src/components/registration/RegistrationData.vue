<script>
export default {
  props: {
    race: {
      type: Object,
    },
    registrationData: { 
      type: Object,
      required: true,
    },
  },
  created() {
    this.initializeRunnerEmails();
    this.initializeProjectTeamTimeChoices();
  },
  data() {
    return {
      valid: false,
      localRegistrationData: {
        ...this.registrationData,
        teamData: {
          name: this.registrationData.teamData?.name || '',
          projectedTeamTime: this.registrationData.teamData?.projectedTeamTime || '',
          emails: this.registrationData.teamData?.emails || [],
        },
        dateOfBirth: this.registrationData.dateOfBirth || '',
        // parentGuardianName: this.registrationData.parentGuardianName || '',
        // parentGuardianSignature: this.registrationData.parentGuardianSignature || '',
        // minor: this.registrationData.minor || false,
      },
      projectedTeamTimeChoices: this.race?.projected_team_time_choices || [],
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length > 1) || 'Name must be more than 1 character',
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      // phoneRules: [
      //   v => !!v || 'Phone is required',
      //   v => /^\d{10}$/.test(v) || 'Phone must be valid',
      // ],
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
        this.initializeProjectTeamTimeChoices();
      },
      deep: true,
      immediate: true,
    },
    registrationData: {
      handler(newVal) {
        this.localRegistrationData = {
          ...newVal,
          dateOfBirth: newVal.dateOfBirth || '',
          // parentGuardianName: newVal.parentGuardianName || '',
          // parentGuardianSignature: newVal.parentGuardianSignature || '',
          // minor: newVal.minor || false,
        };
      },
      deep: true,
    },
  },
  methods: {
    initializeRunnerEmails() {
      // Check if race and num_runners are defined
      if (this.race && this.race.num_runners) {
        // Ensure teamData.emails is an array
        if (!Array.isArray(this.localRegistrationData.teamData.emails)) {
          this.localRegistrationData.teamData.emails = [];
        }

        // Fill in missing emails, preserving existing ones
        for (let i = 0; i < this.race.num_runners; i++) {
          if (!this.localRegistrationData.teamData.emails[i]) {
            this.localRegistrationData.teamData.emails[i] = {
              email: '',
              leg_order: i + 1
            };
          } else {
            // Ensure the leg_order is correct even for existing entries
            this.localRegistrationData.teamData.emails[i].leg_order = i + 1;
          }
        }
      }
    },
    initializeProjectTeamTimeChoices() {
      if (this.race && this.race.projected_team_time_choices) {
        this.projectedTeamTimeChoices = this.race.projected_team_time_choices;
      }
    },
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit('complete', this.localRegistrationData);
      }
    },
  },
};
</script>

<template>
  <v-form ref="form" v-model="valid" @submit.prevent="submit">
    <template v-if="race && race.is_relay">
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="localRegistrationData.teamData.name"
            label="Team Name"
            :rules="nameRules"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-select
            v-model="localRegistrationData.teamData.projectedTeamTime"
            :items="projectedTeamTimeChoices"
            label="Projected Team Time"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="(member, index) in localRegistrationData.teamData.emails" :key="index" cols="6">
          <v-text-field
            v-model="member.email"
            :rules="emailRules"
            :label="`Leg ${member.leg_order} Email`"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </template>
    <v-row>
      <v-col cols="6">
        <v-text-field
          v-model="localRegistrationData.firstName"
          :rules="nameRules"
          label="First Name"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="localRegistrationData.lastName"
          :rules="nameRules"
          label="Last Name"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          v-model="localRegistrationData.email"
          :rules="emailRules"
          label="Email"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="localRegistrationData.gender"
          :items="genders"
          label="Gender"
          required
        ></v-select>
      </v-col>
      <!-- <v-col cols="12" md="6">
        <v-text-field
          v-model="localRegistrationData.phone"
          :rules="phoneRules"
          label="Phone"
          required
        ></v-text-field>
      </v-col> -->
    </v-row>
    <v-row>
      <v-col cols="6">
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
