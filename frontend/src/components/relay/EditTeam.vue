<script>
  export default {
    data() {
      return {
        team: {
          name: '',
          members: [
            { email: '', leg_order: '' } // Initial empty member for simplicity
          ]
        }
      };
    },
    created() {
        // TODO: fix this shit
    //   const token = this.$route.params.token;
      // Optionally, you could fetch the current team data here if needed
    },
    methods: {
      updateTeam() {
        console.log("updateTeam");
        // const token = this.$route.params.token;

        // axios.put(`/api/edit-team/${token}/`, this.team)
        //   .then(response => {
        //     this.$emit('show-snackbar', response.data.message);
        //   })
        //   .catch(error => {
        //     console.error('There was an error updating the team:', error);
        //     this.$emit('show-snackbar', 'An error occurred while updating the team.');
        //   });
      }
    }
  };
</script>
<template>
    <v-container class="mt-5">
        <v-card>
        <v-card-title>Edit Team</v-card-title>
        <v-card-text>
            <v-form @submit.prevent="updateTeam">
            <v-text-field
                v-model="team.name"
                label="Team Name"
                required
            ></v-text-field>

            <v-divider class="my-4"></v-divider>

            <v-subheader>Team Members</v-subheader>
            <div v-for="(member, index) in team.members" :key="index">
                <v-text-field
                v-model="member.email"
                label="Email"
                type="email"
                :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
                required
                ></v-text-field>
                <v-text-field
                v-model="member.leg_order"
                label="Leg Order"
                type="number"
                required
                ></v-text-field>
                <v-divider class="my-4"></v-divider>
            </div>

            <v-btn type="submit" color="primary">Update Team</v-btn>
            </v-form>
        </v-card-text>
        </v-card>
    </v-container>
</template>

  