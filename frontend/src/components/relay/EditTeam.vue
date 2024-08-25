<script>
import api from '@/services/api';

export default {
  data() {
    return {
      team: null,  // Will hold the team data
      snackbar: {
        show: false,
        message: '',
        timeout: 5000
      }
    };
  },
  created() {
    const token = this.$route.params.token;
    this.fetchTeamData(token);
  },
  methods: {
    goBack() {
      const urlAlias = this.team.race.event.url_alias;  // Assuming the URL alias is nested like this
      this.$router.push(`/events/${urlAlias}`);
    },
    fetchTeamData(token) {
      api.getTeamData(token)
        .then(response => {
          this.team = response.data.team;
        })
        .catch(error => {
          console.error('Error fetching team data:', error);
          this.showError('An error occurred while fetching the team data.');
        });
    },
    updateTeam() {
      const token = this.$route.params.token;
      api.updateTeam(token, this.team)
        .then(response => {
          this.showError(response.data.message);

          // Wait 5 seconds, then toggle back to the previous state
          setTimeout(() => {
            this.goBack();
          }, 5000);
        })
        .catch(error => {
          console.error('Error updating team:', error);
          this.showError('An error occurred while updating the team.');
        });
    },
    showError(message) {
      this.snackbar.message = message;
      this.snackbar.show = true;
    }
  }
};
</script>
<template>
  <v-container class="mt-5">
    <v-row justify="center mb-5">
      <v-col cols="12" md="8">
        <v-btn color="primary" @click="goBack">
          <v-icon left>mdi-arrow-left</v-icon>
          Go Back
        </v-btn>
      </v-col>
    </v-row>

    <v-row justify="center mb-5" v-if="team">
      <v-col cols="12" md="6">
        <v-form @submit.prevent="updateTeam">
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="team.name"
                label="Team Name"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="6">
              <v-select
                v-model="team.projected_team_time"
                :items="team.projected_team_time_choices"
                label="Projected Team Time"
                required
              ></v-select>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-subheader>Team Members</v-subheader>
          <v-row v-for="index in Math.ceil(team.members.length / 2)" :key="index">
            <!-- First text field for the current pair -->
            <v-col cols="6">
              <v-text-field
                v-model="team.members[(index - 1) * 2].email"
                :label="`Leg ${team.members[(index - 1) * 2].leg_order} Email`"
                type="email"
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                required
              ></v-text-field>
            </v-col>

            <!-- Second text field for the current pair, if it exists -->
            <v-col cols="6" v-if="team.members[(index - 1) * 2 + 1]">
              <v-text-field
                v-model="team.members[(index - 1) * 2 + 1].email"
                :label="`Leg ${team.members[(index - 1) * 2 + 1].leg_order} Email`"
                type="email"
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-divider class="my-4"></v-divider>
          <v-btn type="submit" color="primary">Update Team</v-btn>
        </v-form>
      </v-col>
    </v-row>

    <!-- Snackbar for Notifications -->
    <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout">
      {{ snackbar.message }}
      <v-btn color="red" text @click="snackbar.show = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>
