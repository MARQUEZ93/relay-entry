import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust this baseURL if necessary
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

export default {
  getEvent(url_alias) {
    return apiClient.get(`/events/${url_alias}/`);
  },
  getRace(eventSlug, raceId) {
    return axios.get(`/api/events/${eventSlug}/races/${raceId}/`);
  },
};
