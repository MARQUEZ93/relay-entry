
  
<script>
export default {
    name: 'AboutComponent',
    data() {
        return {
            client: "Bex Wells (Sunrise Track Club)",
            review: "RelayEntry was a game changer for race signup! It was easy for teams to use to register and for me to have the data I needed prior to the race! The post race results were posted quickly and emailed out to participants, saving me another step. So glad I found this one stop shop for race sign up!",
        };
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
                <h1>About Us</h1>
                <p>The best running platform for team relay races!</p>
                <v-row>
                    <v-col cols="12">
                        <v-sheet class="my-5 pa-5" elevation="2">
                            <h2>Mission</h2>
                            <p>RelayEntry was created by <a href="https://www.dromarquez.com/">Alejandro E. Marquez</a> after a bad UX experience encountered while registering for a team relay race.</p>
                        </v-sheet>
                    </v-col>
                    <v-col cols="12">
                        <v-sheet class="my-5 pa-5" elevation="2">
                            <h2>Testimonial</h2>
                            <blockquote class="testimonial-quote">{{ review }}</blockquote>
                            <p class="testimonial-client">
                                — <a class="client-link" href="https://sunrisetrackclub.com/">{{ client }}</a>, <a href="/events/sunrise-track-club-sunset-relays" class="event-link">Sunrise Relays 2024</a>
                            </p>
                        </v-sheet>
                    </v-col>
                    <!-- New Section for Privacy Policy & Terms of Agreement -->
                    <v-col cols="12">
                        <v-sheet class="my-5 pa-5" elevation="2">
                            <h2>Policies & Agreements</h2>
                            <v-btn text :to="{ path: '/privacy-policy' }">Privacy Policy</v-btn>
                            <v-btn text :to="{ path: '/terms-of-agreement' }">Terms of Agreement</v-btn>
                        </v-sheet>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>
    h1 {
        margin-top: 20px;
        text-align: center;
        margin-bottom: 10px;
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

    .features-list {
        list-style-type: disc;
        padding-left: 20px;
    }

    .features-list li {
        text-align: left;
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        font-size: 1.1em;
        word-wrap: break-word;
        white-space: normal;
    }

    .features-list li v-icon {
        margin-right: 8px;
        color: #4caf50;
    }

    .testimonial-quote {
        font-style: italic;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 15px;
        color: #2c3e50;
    }

  .testimonial-client {
    font-weight: bold;
    text-align: center;
    color: #4caf50;
  }

  .event-link {
    color: #1867c0; 
    text-decoration: none;
  }
  .client-link {
    color: #4caf50; 
    text-decoration: none;
  }

  .event-link:hover, .client-link:hover {
    text-decoration: underline;
  }

    @media (max-width: 600px) {
        h1, h2 {
            font-size: 1.5em;
        }

        .testimonial-quote, .features-list li, p, .testimonial-client {
            font-size: 1em;
        }

    }
</style>
  