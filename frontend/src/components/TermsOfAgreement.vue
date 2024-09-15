<script>
export default {
    name: 'TermsOfAgreementComponent',
    data() {
        return {
            title: "Terms of Agreement",
            lastUpdated: "September 15 2024",
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
                    <h2>User Responsibilities</h2>
                    <p>By using our platform to register for events, you agree to provide accurate and truthful information. You are also responsible for complying with the rules of the event you register for, as set by the event coordinator.</p>

                    <h2>Event Coordinators</h2>
                    <p>Event coordinators have the ability to create and manage accounts on our platform. They can delete their accounts at any time, at which point their data will be removed from our systems.</p>

                    <h2>Registrants</h2>
                    <p>Registrants do not need to create accounts to participate in events. However, after registering, you will receive an email to confirm your registration details. It is your responsibility to ensure that you receive and confirm this email.</p>

                    <h2>Event Cancellations and Changes</h2>
                    <p>In the event of cancellations or significant changes to an event, we will work with the event coordinator to ensure a fair resolution for all parties involved. Any returns or adjustments will be handled on a case-by-case basis.</p>

                    <h2>Refund Policy</h2>
                    <p>We do not offer refunds for legitimate purchases. However, in cases where an event is canceled or significantly altered, we will collaborate with the event coordinator to address the situation fairly.</p>

                    <h2>Limitation of Liability</h2>
                    <p>We are not responsible for any issues or damages that arise from event changes, cancellations, or issues related to the payment process. Event coordinators are responsible for managing their events, and we facilitate the registration process.</p>

                    <h2>Account Deletion</h2>
                    <p>Event coordinators can delete their accounts at any time. Once an account is deleted, all associated data will be removed from our system. This does not affect the data provided by registrants, which is tied to specific events.</p>

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
        margin-top: 10px;
        color: #4caf50;
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
