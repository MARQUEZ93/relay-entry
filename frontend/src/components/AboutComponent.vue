
  
<script>
export default {
    name: 'AboutComponent',
    data() {
        return {
        texasDescription: "Texas races are eligible for lower rates because RelayEntry is a Texas small business. Contact us for more details!"
        };
    }
    };
</script>
<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-typography class="h1-about" variant="h1">About RelayEntry</v-typography>
                <v-sheet class="mx-auto my-5 pa-5" elevation="2">
                    <v-row>
                        <v-col cols="12">
                            <v-typography class="body-about" variant="body">RelayEntry was created to make it easier for anyone to start their own race. </v-typography>
                            <v-typography class="body-about" variant="body">We are committed to providing the best racing platform that caters to the needs of race organizers, racers and spectators alike. </v-typography>
                            <v-typography class="body-about" variant="body">Currently, our product supports team relay races, with plans to expand to other race types in Q4 2024.</v-typography>
                        </v-col>
                    </v-row>
                </v-sheet>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>
    .h1-about {
        color: #4caf50;
        margin-top: 20px;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 10px;
    }

    .body-about {
        font-size: 1.2em;
        color: #2c3e50;
        text-align: center;
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
  