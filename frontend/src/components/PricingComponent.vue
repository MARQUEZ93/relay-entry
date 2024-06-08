<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Pricing</h1>
          <p>Making race day affordable again with simple pricing.</p>
          <v-sheet class="mx-auto my-5 pa-5" elevation="2">
            <v-row>
              <v-col cols="12">
                <h2>Transparent Pricing</h2>
                <p>2.9% + $1 per Transaction in Texas</p>
                <p>3.4% + $1 per Transaction in Other States</p>
              </v-col>
            </v-row>
            <v-divider class="my-5"></v-divider>
            <v-row>
              <v-col cols="12">
                <ul class="pricing-list">
                  <li>
                    <v-icon left>mdi-currency-usd</v-icon>
                    Low transaction fees to help you save more.
                  </li>
                  <li>
                    <v-icon left>mdi-map-marker</v-icon>
                    Perfect for races across the country.
                  </li>
                  <li>
                    <v-icon left>mdi-pencil</v-icon>
                    Ensure waivers are signed by every racer.
                  </li>
                  <li>
                    <v-icon left>mdi-access-point</v-icon>
                    Accessible software for all participants, including the visually impaired.
                  </li>
                  <li>
                    <v-icon left>mdi-run-fast</v-icon>
                    Designed for team relay races.
                  </li>
                  <li>
                    <v-icon left>mdi-cellphone</v-icon>
                    Mobile-first platform for easy access on the go.
                  </li>
                </ul>
              </v-col>
            </v-row>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'PricingComponent',
  };
  </script>
  
  <style scoped>
  h1 {
    color: #2c3e50;
    margin-top: 20px;
    text-align: center;
  }
  
  p {
    font-size: 1.2em;
    color: #2c3e50;
    text-align: center;
  }
  
  h2 {
    color: #4caf50;
    margin-bottom: 10px;
  }
  
  .v-divider {
    margin-top: 20px;
  }
  
  .pricing-list {
    list-style-type: disc;
    padding-left: 20px;
  }
  
  .pricing-list li {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    font-size: 1.1em;
  }
  
  .pricing-list li v-icon {
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
  
    .pricing-list li {
      font-size: 1em;
    }
  }
  </style>
  