
  
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
                <h1>About</h1>
                <p>Our 2024 plans</p>
                <v-row>
                    <v-col cols="12">
                        <v-sheet class="my-5 pa-5" elevation="2">
                            <h2>Our Mission</h2>
                            <p>RelayEntry was created to make it easier for anyone to start their own race. </p>
                            <p>We are committed to providing the best racing platform that caters to the needs of race organizers, racers and spectators alike. </p>
                            <p>Currently, our product supports team relay races, with plans to expand to other race types EOY.</p>
                        </v-sheet>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>
    h1 {
        color: #2c3e50;
        margin-top: 20px;
        text-align: center;
        margin-bottom: 10px;
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
  