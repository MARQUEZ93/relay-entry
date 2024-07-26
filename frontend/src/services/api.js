import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  withCredentials: true,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

// Function to get CSRF token from cookies
function getCSRFToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}
// Add a request interceptor to include the CSRF token in each request
apiClient.interceptors.request.use(
  (config) => {
    const token = getCSRFToken();
    if (token)  {
      config.headers['X-CSRFToken'] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  fetchCsrfToken() {
    return apiClient.get(`/get-csrf/`);
  },
  getEvent(eventSlug) {
    return apiClient.get(`/events/${eventSlug}/`);
  },
  getRace(eventSlug, raceId) {
    return apiClient.get(`/events/${eventSlug}/races/${raceId}/`);
  },
  getRaceResults(raceId) {
    return apiClient.get(`/races/${raceId}/results/`);
  },
  // TODO: revert
  // registerTeam(data) {
  //   return apiClient.post('/teams/register/', data);
  // },
  registerForEvent(eventSlug, data) {
    return apiClient.post(`/events/${eventSlug}/register/`, data);
  },
  // TODO: revert
  // createPaymentIntent(data){
  //   return apiClient.post(`/create-payment-intent/`, data);
  // }
};
