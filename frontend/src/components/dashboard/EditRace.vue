<script>
  import api from '@/services/api';
  
  export default {
    name: 'EditRace',
    data() {
      return {
        race: {},
        distanceOptions: ['5K', '10K', 'Half Marathon', 'Marathon', 'Ultra Marathon', 'Custom'],
      };
    },
    methods: {
      async fetchRace() {
        const { raceId } = this.$route.params;
        try {
          const response = await api.getRace(raceId);
          this.race = response.data;
        } catch (error) {
          this.$router.push('/dashboard');
        }
      },
      async updateRace() {
        const { raceId } = this.$route.params;
        try {
          await api.updateRace(raceId, this.race);
          this.$router.push(`/dashboard/events/${this.race.event}/`);
        } catch (error) {
          // Handle error
          this.$emit('showSnackbar', 'Error updating race.', 'error');
        }
      },
    },
    created() {
      this.fetchRace();
    },
  };
  </script>
  <template>
    <v-container>
      <v-form ref="form" @submit.prevent="updateRace">
        <v-text-field v-model="race.name" label="Race Name" required></v-text-field>
        <v-select
          v-model="race.distance"
          :items="distanceOptions"
          label="Distance"
          required
        ></v-select>
        <v-btn type="submit" color="primary">Save Changes</v-btn>
      </v-form>
    </v-container>
  </template>