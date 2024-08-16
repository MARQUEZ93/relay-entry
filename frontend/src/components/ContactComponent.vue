
  
<script>
import axios from 'axios';
import api from '@/services/api';  // Adjust the path according to your project structure
export default {
    name: 'ContactComponent',
    mounted() {
        this.getUserIp();
        if (process.env.NODE_ENV === 'development'){
            this.fillForm();
        }
    },
    data() {
        return {
            form: {
                name: '',
                email: '',
                role: '',
                message: '',
                ip: '',
                honey: '',
                confirmation: '',
            },
            valid: false,
            successMessage: '',
            errorMessage: '',
            nameRules: [
                v => !!v || 'Name is required',
            ],
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            roleRules: [
                v => (v !== '' && v !== null && v !== undefined) || 'Role is required',
            ],
            messageRules: [
                v => !!v || 'Message is required',
            ],
            confirmationRules: [
                v => !!v || 'Confirmation number is required',
            ],
        };
    },
    computed: {
        showConfirmationNumber() {
            return this.form.role === 'Registrant';
        },
        isDevelopment(){
            return process.env.NODE_ENV === 'development';
        },
    },
    methods: {
        fillForm(){
            this.form.name = 'First LastName';
            this.form.email = 'example@example.com';
            this.form.message = 'This is a test message. How are you? My race site is https://marathon.com/';
            this.form.role = 'Other';
        },
        async getUserIp() {
            const response = await axios.get('https://api.ipify.org?format=json');
            this.form.ip = response.data.ip;
        },
        async submitForm() {
            if (this.$refs.form.validate()) {
                if (!this.form.role){
                    this.errorMessage = 'Role is required';
                    return;
                }
                try {
                    const response = await api.sendContact({
                        name: this.form.name,
                        email: this.form.email,
                        role: this.form.role,
                        message: this.form.message,
                        ip: this.form.ip,
                        honey: this.form.honey,
                        confirmation: this.form.confirmation,
                    });
                    if (response.status === 200) {
                        this.successMessage = 'Your message has been sent successfully!';
                        this.errorMessage = ''; // Clear any previous error message
                        // Redirect to the home page after 3 seconds
                        setTimeout(() => {
                            this.$router.push({ path: '/' });
                        }, 3000);
                    } else {
                        this.errorMessage = response?.data?.message || 'An error occurred while sending your message. Please try again later.';
                        this.successMessage = ''; // Clear any previous success message
                    }
                } catch (error) {
                    this.errorMessage = error.response?.data?.message || 'An error occurred while sending your message. Please try again later.';
                    this.successMessage = ''; // Clear any previous success message
                } finally {
                    this.$refs.form.reset(); // Reset the form regardless of the outcome
                }
            }
        },
    },
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
                                    <v-col cols="12">
                                        <v-select
                                            v-model="form.role"
                                            :items="['Event Director', 'Registrant', 'Timer', 'Charity', 'Other']"
                                            :rules="roleRules"
                                            label="Who are you?"
                                            required
                                        ></v-select>
                                    </v-col>
                                    <!-- Confirmation Number Field (Only shows if role is 'Registrant') -->
                                    <v-col cols="6" v-if="showConfirmationNumber">
                                        <v-text-field
                                            v-model="form.confirmation"
                                            :rules="confirmationRules"
                                            label="Confirmation Number"
                                            required
                                        ></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col cols="12">
                                        <v-text-field
                                            v-model="form.honey"
                                            label="Honey"
                                            style="display: none;"
                                        ></v-text-field>
                                        <v-textarea
                                            v-model="form.message"
                                            :rules="messageRules"
                                            label="Your Message"
                                            required
                                        ></v-textarea>
                                    </v-col>
                                </v-row>
                                <v-row v-if="successMessage || errorMessage" class="mb-2">
                                    <v-col cols="12">
                                        <v-alert type="success" v-if="successMessage">{{ successMessage }}</v-alert>
                                        <v-alert type="error" v-if="errorMessage">{{ errorMessage }}</v-alert>
                                    </v-col>
                                </v-row>
                                <v-btn
                                    color="primary"
                                    @click="submitForm"
                                >
                                    Let's talk
                                </v-btn>
                                <v-btn
                                    v-if="isDevelopment"
                                    color="secondary"
                                    @click="fillForm"
                                >
                                    Demo
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
  