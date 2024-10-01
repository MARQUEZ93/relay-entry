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
    // Add JWT access token to Authorization header
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

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

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refresh_token');

    // Prevent interceptor from intercepting token refresh request
    if (originalRequest.url === '/token/refresh/') {
      return Promise.reject(error);
    }

    if (
      error.response &&
      error.response.status === 401 &&
      refreshToken
    ) {
      try {
        // Attempt to refresh the access token
        const response = await apiClient.post('/token/refresh/', { refresh: refreshToken });

        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);

        // Update the Authorization header for the original request
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        // Retry the original request with the new token
        return apiClient(originalRequest);
      } catch (err) {
        console.error('Error during token refresh:', err);

        // Logout the user if token refresh fails
        apiClient.logout();
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default {
  getUserRace(raceId) {
    return apiClient.get(`/dashboard/races/${raceId}/`);
  },
  updateUserRace(raceId, data) {
    return apiClient.put(`/dashboard/races/update/${raceId}/`, data);
  },
  getUserEvent(id){
    return apiClient.get(`/dashboard/events/${id}/`);
  },
  getUserEvents() {
    return apiClient.get(`/dashboard/events/`);
  },
  updateEvent(eventId, eventData) {
    return apiClient.put(`/dashboard/events/update/${eventId}/`, eventData);
  },
  createEvent(eventData) {
    return apiClient.post(`/dashboard/events/create/`, eventData);
  },
  fetchCsrfToken() {
    return apiClient.get(`/get-csrf/`);
  },
  getTeamData(token) {
    return apiClient.get(`/teams/get-team/${token}/`);
  },
  updateTeam(token, teamData) {
    return apiClient.put(`/edit-team/${token}/`, teamData);
  },
  requestEditLink(url_alias, data) {
    return apiClient.post(`/events/${url_alias}/request-edit-link/`, data);
  },
  getEvent(eventSlug) {
    return apiClient.get(`/events/${eventSlug}/`);
  },
  getRace(eventSlug, raceId) {
    return apiClient.get(`/events/${eventSlug}/races/${raceId}/`);
  },
  getTeamRaceResults(raceId) {
    return apiClient.get(`/races/${raceId}/team-results/`);
  },
  registerTeam(data) {
    return apiClient.post('/teams/register/', data);
  },
  registerForEvent(eventSlug, data) {
    return apiClient.post(`/events/${eventSlug}/register/`, data);
  },
  createPaymentIntent(data){
    return apiClient.post(`/create-payment-intent/`, data);
  },
  sendContact(data){
    return apiClient.post(`/contact/`, data);
  },
  confirmEventRegistration(eventSlug, name){
    return apiClient.get(`/search/${eventSlug}/${name}`);
  },
  dashboard(){
    return apiClient.get(`/dashboard/`);
  },
  login(username, password){
    return apiClient.post(`/token/`, {
      username: username,
      password: password,
    });
  },
  logout() {
    console.log("logout()")
    const refreshToken = localStorage.getItem('refresh_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
    console.log(refreshToken);
    if (!refreshToken) {
      return;
    }
    return apiClient.post('/logout/', { refresh_token: refreshToken })
  },
};
