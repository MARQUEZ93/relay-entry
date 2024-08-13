
  
<script>
export default {
    name: 'ContactComponent',
    data() {
        return {
            form: {
                name: '',
                email: '',
                role: '',
                message: '',
            },
            valid: true,
            nameRules: [
                v => !!v || 'Name is required',
            ],
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            roleRules: [
                v => !!v || 'Role is required',
            ],
            messageRules: [
                v => !!v || 'Message is required',
            ],
        };
    },
    methods: {
        submitForm() {
            if (this.$refs.form.validate()) {
                // Here you'd typically make an API call to submit the form data
                // For example:
                // this.$http.post('/api/contact', this.form)
                //     .then(response => {
                //         // Handle success
                //     })
                //     .catch(error => {
                //         // Handle error
                //     });

                console.log('Form submitted:', this.form);
                this.$refs.form.reset();
                // You can also show a success message here
            }
        }
    }
};
</script>
<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1>Contact Us</h1>
                <p>Fill out the form below, and we'll respond within 24 hours!</p>
                <v-row>
                    <v-col cols="12">
                        <v-sheet class="my-5 pa-5" elevation="2">
                            <h2>Start your own event!</h2>
                            <v-form ref="form" v-model="valid">
                                <v-row>
                                    <v-col cols="6">
                                        <v-text-field
                                            v-model="form.name"
                                            :rules="nameRules"
                                            label="Full name"
                                            required
                                        ></v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-text-field
                                            v-model="form.email"
                                            :rules="emailRules"
                                            label="Your Email"
                                            required
                                        ></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col>
                                        <v-select
                                            v-model="form.role"
                                            :items="['Event Director', 'Participant', 'Timer', 'Charity', 'Other']"
                                            :rules="roleRules"
                                            label="Who are you?"
                                            required
                                        ></v-select>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col cols="12">
                                        <v-textarea
                                            v-model="form.message"
                                            :rules="messageRules"
                                            label="Your Message"
                                            required
                                        ></v-textarea>
                                    </v-col>
                                </v-row>
                                <v-btn
                                    color="primary"
                                    @click="submitForm"
                                >
                                    Submit
                                </v-btn>
                            </v-form>
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
  