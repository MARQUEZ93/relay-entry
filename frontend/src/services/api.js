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

    // Initialize retry count if it doesn't exist
    if (!originalRequest._retryCount) {
      originalRequest._retryCount = 0;
    }

    if (
      error.response &&
      error.response.status === 401 &&
      refreshToken &&
      originalRequest._retryCount < 3 // Retry limit
    ) {
      originalRequest._retry = true;
      originalRequest._retryCount++; // Increment retry count

      try {
        const response = await apiClient.post('/token/refresh/', { refresh: refreshToken });
        localStorage.setItem('access_token', response.data.access);

        // Update the Authorization header for this request
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
        return apiClient(originalRequest);
      } catch (err) {
        // If the refresh token is invalid, logout the user
        if (err.response && err.response.status === 401) {
          apiClient.logout();
        }
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default {
  fetchCsrfToken() {
    return apiClient.get(`/get-csrf/`);
  },
  getTeamData(token) {
    return apiClient.get(`/teams/get-team/${token}/`);
  },
  updateTeam(token, teamData) {
    console.log(teamData);
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
  refreshToken(refreshToken) {
    return apiClient.post('/token/refresh/', {
      refresh: refreshToken,
    });
  },
  logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
    return apiClient.post('/logout/', {
      refresh_token: refreshToken
    });
  },
};
