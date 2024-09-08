<script>
export default {
    name: 'PrivacyPolicyComponent',
    data() {
        return {
            title: "Privacy Policy",
            lastUpdated: "September 2024",
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
                <h1>{{ title }}</h1>
                <p><strong>Last Updated:</strong> {{ lastUpdated }}</p>
                <v-sheet class="my-5 pa-5" elevation="2">
                    <h2>Data Collection</h2>
                    <p>We collect information such as name, email, and race registration details when you sign up for events. However, we do not store any payment information. All transactions are securely processed through Stripe.</p>

                    <h2>Data Usage</h2>
                    <p>The information we collect is used solely for event registration purposes. Your data is only shared with the event coordinator for the event you registered for and is never sold or shared with third parties.</p>

                    <h2>Data Security</h2>
                    <p>We employ industry best practices, including encryption and secure servers, to protect your personal information. Rest assured, your data is safe with us.</p>

                    <h2>Minors</h2>
                    <p>For participants under the age of 18, a parent or guardian must complete the registration process. We do not knowingly collect information from minors without consent from a parent or guardian.</p>

                    <h2 class="pb-2">Third-Party Services</h2>
                    <p>We use Stripe to securely process payments. Stripe handles the transaction, and we do not retain any payment information.</p>

                    <h2 class="pb-2">Cookies & Tracking</h2>
                    <p class="pb-2">We do not use cookies or any other tracking technologies on our platform.</p>

                    <h2 class="pb-2">User Rights</h2>
                    <p>You have the right to access, modify, or delete the personal information we have on file. If you wish to do so, please contact us at relayentry@gmail.com</p>
                </v-sheet>
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
        text-align: center;
    }
    
    h2 {
        color: #4caf50;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .v-divider {
        margin-top: 20px;
    }

    @media (max-width: 600px) {
        h1, h2 {
            font-size: 1.5em;
        }

        p {
            font-size: 1em;
        }
    }
</style>
