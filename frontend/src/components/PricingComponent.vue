<script>
  export default {
    name: 'PricingComponent',
    data(){
      return {
        stripeDescription: "All payments are processed through Stripe Connect. Race directors create their own Stripe accounts, and we handle the rest to ensure smooth and secure transactions.",
      }
    },
    async mounted() {
      window.scrollTo(0, 0);
    },
  };
</script>
<template>
    <v-container>
        <v-row>
        <v-col cols="12">
            <h1>Pricing</h1>
            <p>Making race day affordable again</p>
            <v-sheet class="mx-auto my-5 pa-5" elevation="2">
            <v-row>
                <v-col cols="12">
                  <h2>2.9% + 30¢ per Transaction</h2>
                  <p class="texas-transaction d-flex align-center justify-center">
                    <strong>
                      $50 for every $5,000 in sales!
                    </strong>
                    <v-icon size="x-small" class="ml-2" color="primary" v-tooltip.top="stripeDescription">
                          mdi-information
                    </v-icon>
                  </p>
                </v-col>
            </v-row>
            <v-divider class="my-5"></v-divider>
            <v-row>
                <v-col cols="12">
                  <ul class="pricing-list">
                      <li>
                        <v-icon left>mdi-currency-usd</v-icon>
                        &nbsp;The absolute lowest transaction fees
                      </li>
                      <li>
                        <v-icon left>mdi-wallet</v-icon>
                        &nbsp;Receive payments immediately
                      </li>
                      <li>
                        <v-icon left>mdi-file-document-edit</v-icon>
                        &nbsp;No contracts
                      </li>
                      <li>
                        <v-icon left>mdi-map-marker</v-icon>
                        &nbsp;Perfect for races across the USA
                      </li>
                      <li>
                        <v-icon left>mdi-access-point</v-icon>
                        &nbsp;Accessibility compliant
                      </li>
                      <li>
                        <v-icon left>mdi-run-fast</v-icon>
                        &nbsp;Designed for team relay races
                      </li>
                      <li>
                        <v-icon left>mdi-cellphone</v-icon>
                        &nbsp;Mobile-first platform
                      </li>
                      <li>
                        <v-icon left>mdi-pencil</v-icon>
                        &nbsp;Waivers completed by all participants
                      </li>
                      <li>
                        <v-icon left>mdi-web</v-icon>
                        &nbsp;Your event page can be your race site
                      </li>
                      <li>
                        <v-icon left>mdi-mail</v-icon>
                        &nbsp;Customizable email system
                      </li>
                      <li>
                        <v-icon left>mdi-cog</v-icon>
                        &nbsp;Customizable UI per request
                      </li>
                  </ul>
                </v-col>
            </v-row>
            </v-sheet>
        </v-col>
        </v-row>
    </v-container>
  </template>
  
<style scoped>
  h1 {
    color: black;
    margin-top: 20px;
    text-align: center;
  }
  
  p {
    font-size: 1.2em;
    color: black;
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
    word-wrap: break-word;
    white-space: normal;
  }
  
  .pricing-list li v-icon {
    margin-right: 8px;
    color: #4caf50;
  }

  .texas-transaction {
    cursor: pointer; /* Added to indicate interactivity */
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
  