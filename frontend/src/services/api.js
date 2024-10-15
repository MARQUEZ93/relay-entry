import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  withCredentials: true,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

function clearTokens(){ 
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

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
        clearTokens();
        delete apiClient.defaults.headers.common['Authorization'];
        console.error('Error during token refresh:', err);
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
  updateRace(raceId, data) {
    return apiClient.patch(`/dashboard/races/update/${raceId}/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  createRace(data) {
    return apiClient.post(`/dashboard/races/create/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getUserEvent(id){
    return apiClient.get(`/dashboard/events/${id}/`);
  },
  getUserEvents() {
    return apiClient.get(`/dashboard/events/`);
  },
  updateEvent(eventId, eventData) {
    return apiClient.patch(`/dashboard/events/update/${eventId}/`, eventData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  createEvent(eventData) {
    return apiClient.post(`/dashboard/events/create/`, eventData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  fetchCsrfToken() {
    return apiClient.get(`/get-csrf/`);
  },
  getTeamData(token) {
    return apiClient.get(`/teams/get-team/${token}/`);
  },
  updateTeam(token, teamData) {
    return apiClient.patch(`/edit-team/${token}/`, teamData);
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
  async logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    clearTokens();
    delete apiClient.defaults.headers.common['Authorization'];
    if (!refreshToken) {
      return;
    }
    try {
      return apiClient.post('/logout/', { refresh_token: refreshToken })
        .catch(error => {
          // Handle API response error
          console.error('Error during logout:', error.response ? error.response.data : error.message);
        });
    } catch (error) {
      // Handle unexpected errors
      console.error('Unexpected error during logout:', error.message);
    }
  },
};
