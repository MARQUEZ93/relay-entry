<script>
  import homeImage from '@/assets/homeImage.jpg';
  export default {
    name: 'HomeComponent',
    data() {
      return {
        homeImage,
      };
    },
  };
</script>

<template>
  <v-container>
    <v-row class="home-background-image">
      <v-col cols="12">
        <h1>Welcome to RelayEntry</h1>
        <p>Your ultimate solution for race registrations</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-sheet class="my-5 pa-5" elevation="2">
          <h2>Race Day is the Best Day</h2>
          <p>
            Experience the best race day with RelayEntry's budget-friendly pricing. Our platform streamlines race management: seamless waiver signing, efficient data collection, and enhanced accessibility for all participants. RelayEntry is designed with a mobile-first approach to deliver an exceptional user experience, specifically tailored for team relay races.
          </p>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
  h1 {
    color: black;
    margin-top: -200px;
    font-weight: 700;
  }

  h2 {
    color: #4caf50;
    margin-bottom: 10px;
  }

  p {
    font-size: 1.2em;
    color: black;
  }

  .curved-image-container {
    position: relative;
    overflow: hidden;
  }

  .home-background-image {
    background-image: url('@/assets/homeImage.jpg');
    background-size: cover;
    background-position: center;
    height: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
    clip-path: ellipse(100% 90% at 50% 100%);
  }

  .curved-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
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
