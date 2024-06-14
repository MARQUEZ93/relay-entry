<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Welcome to RelayEntry</h1>
        <p>Your premier solution for race registrations.</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-sheet class="my-5 pa-5" elevation="2">
          <h2>Race Day is the Best Day</h2>
          <p>
            Experience the best race day with RelayEntry's budget-friendly pricing. Our platform streamlines race management: seamless waiver signing, efficient data collection, and enhanced accessibility for all participants. Designed with a mobile-first approach, RelayEntry provides an exceptional user experience, especially crafted for team relay races.
          </p>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomeComponent',
};
</script>

<style scoped>
h1 {
  color: #2c3e50;
  margin-top: 20px;
}

h2 {
  color: #4caf50;
  margin-bottom: 10px;
}

p {
  font-size: 1.2em;
  color: #2c3e50;
}

.features-list {
  list-style-type: none;
  padding: 0;
}

.features-list li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 1.1em;
}

.features-list li v-icon {
  margin-right: 8px;
  color: #4caf50;
}

@media (max-width: 600px) {
  h1, h2 {
    font-size: 1.5em;
  }

  p {
    font-size: 1em;
  }

  .features-list li {
    font-size: 1em;
  }
}
</style>
