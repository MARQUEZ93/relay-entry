import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.API_URL, // Adjust this baseURL if necessary
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

export default {
  getEvent(eventSlug) {
    return apiClient.get(`/events/${eventSlug}/`);
  },
  getRace(eventSlug, raceId) {
    return apiClient.get(`/events/${eventSlug}/races/${raceId}/`);
  },
  createPaymentIntent(paymentData) {
    return apiClient.post('/api/create-payment-intent/', paymentData);
  },
};
