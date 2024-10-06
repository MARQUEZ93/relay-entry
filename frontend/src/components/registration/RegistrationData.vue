<script>
export default {
  props: {
    race: {
      type: Object,
    },
    event: {
      type: Object,
    },
    registrationData: { 
      type: Object,
      required: true,
    },
    raceField:{
      type: Boolean,
      default: false,
    }
  },
  mounted(){
    if (process.env.NODE_ENV === 'development'){
      this.fillForm();
    }
  },
  created() {
    this.initializeRunnerEmails();
    this.initializeProjectTeamTimeChoices();
    this.initializeRaceChoices();
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
        selectedRace: this.registrationData.selectedRace || '',
        dateOfBirth: this.registrationData.dateOfBirth || '',
        parentGuardianName: this.registrationData.parentGuardianName || '',
        parentGuardianSignature: this.registrationData.parentGuardianSignature || '',
        minor: this.registrationData.minor || false,
      },
      races: [],
      projectedTeamTimeChoices: this.race?.projected_team_time_choices || [],
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length > 1) || 'Name must be more than 1 character',
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Email must be valid',
      ],
      confirmEmailRules: [
        v => !!v || 'Confirm Email is required',
        v => /.+@.+\..+/.test(v) || 'Confirm email must be valid',
        v => v === this.localRegistrationData.email || 'Emails must match',
      ],
      parentGuardianNameRules: [
        v => !!v || 'Parent Guardian Name is required',
        v => (v && v.length > 1) || 'Name must be more than 1 character',
      ],
      parentGuardianSignatureRules: [
        v => !!v || 'Guardian Signature is required',
        v => (v && v.length > 1) || 'Guardian Signature must be more than 1 character',
        v => v === this.localRegistrationData.parentGuardianName || 'Signature must match',
      ],
      // phoneRules: [
      //   v => !!v || 'Phone is required',
      //   v => /^\d{10}$/.test(v) || 'Phone must be valid',
      // ],
      genders: ['Male', 'Female', 'Other'],
      dobRules: [
        v => !!v || 'Date of Birth is required',
        // v => this.isAdult(v) || 'You must be at least 18 years old, or check the minor box and provide guardian information',
      ],
    };
  },
  watch: {
    event: {
      handler() {
        this.initializeRaceChoices();
      },
      deep: true,
      immediate: true,
    },
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
          selectedRace: newVal.selectedRace || '',
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
    // isAdult(dob) {
    //   if (!dob) return false;
    //   const today = new Date();
    //   const birthDate = new Date(dob);
    //   const age = today.getFullYear() - birthDate.getFullYear();
    //   const monthDiff = today.getMonth() - birthDate.getMonth();
      
    //   // Adjust the age if the birth month and day have not passed yet
    //   if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    //     return age > 18;
    //   }
    //   return age >= 18;
    // },
    getRandomString(){
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      const length = 4;  // Desired length of the random string
      for (let i = 0; i < length; i++) {
          const randomIndex = Math.floor(Math.random() * characters.length);
          result += characters[randomIndex];
      }
      return result;
    },
    fillForm(){
      // this.localRegistrationData["dateOfBirth"] = "2024-09-03";
      this.localRegistrationData["firstName"] = "Hello";
      this.localRegistrationData["lastName"] = "Lasty";
      const randomEmail = this.getRandomString() + "@gmail.com";
      this.localRegistrationData["email"] = randomEmail;
      this.localRegistrationData["confirmEmail"] = randomEmail;
      this.localRegistrationData["gender"] = "Male";
      this.localRegistrationData["teamData"]["projectedTeamTime"] = "7:00 / mile";
      this.localRegistrationData["teamData"]["name"] = this.getRandomString();
      for (let i = 0; i < 4; i++) {
        this.localRegistrationData.teamData.emails[i] = {
          email: this.getRandomString() + "@gmail.com",
          leg_order: i + 1
        };
      }
    },
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
    initializeRaceChoices() {
      if (this.raceField && this.event && this.event.races) {
        this.races = this.event.races;
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
            :rules="[v => !!v || 'Projected Team Time is required']"
            required
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="(member, index) in localRegistrationData.teamData.emails" :key="'leg-emails' + index" cols="6">
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
        <v-text-field
          v-model="localRegistrationData.confirmEmail"
          :rules="confirmEmailRules"
          label="Confirm Email"
          required
        ></v-text-field>
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
      <v-col cols="6" v-if="this.raceField">
        <v-select
            v-model="localRegistrationData.selectedRace"
            :items="races"
            item-title="name"
            item-value="id"
            label="Race"
            :rules="[v => !!v || 'Race is required']"
            required
          ></v-select>
      </v-col>
      <v-col cols="6">
        <!-- TODO: UPDATE VUE 3.6 to get vue-date-input -->
        <v-text-field
          type="date"
          v-model="localRegistrationData.dateOfBirth"
          label="Date of Birth"
          :rules="dobRules"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          v-model="localRegistrationData.gender"
          :items="genders"
          label="Gender"
          :rules="[v => !!v || 'Gender is required']"
          required
        ></v-select>
      </v-col>
      <v-col cols="6">
        <v-checkbox
          v-model="localRegistrationData.minor"
          label="The registrant is a minor (under 18 years old)"
        ></v-checkbox>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          v-if="localRegistrationData.minor"
          :rules="parentGuardianNameRules"
          v-model="localRegistrationData.parentGuardianName"
          label="Parent/Guardian Name"
        ></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-if="localRegistrationData.minor"
          :rules="parentGuardianSignatureRules"
          v-model="localRegistrationData.parentGuardianSignature"
          label="Parent/Guardian Signature"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-btn type="submit" color="primary" :disabled="!valid">Next</v-btn>
  </v-form>
</template>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>
