import axios from 'axios';

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api",
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
  // Combined method for creating payment intent and registration
  createPaymentAndRegistration(data) {
    return apiClient.post('/create-payment-and-registration/', data);
  },
};
