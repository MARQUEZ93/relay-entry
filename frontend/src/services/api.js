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

let isRefreshing = false;
let refreshSubscribers = [];

function subscribeTokenRefresh(cb) {
  refreshSubscribers.push(cb);
}

function onRefreshed(accessToken) {
  refreshSubscribers.forEach(cb => cb(accessToken));
  refreshSubscribers = [];
}

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
      originalRequest._retryCount++; // Increment retry count

      if (!isRefreshing) {
        isRefreshing = true;

        try {
          const response = await apiClient.post('/token/refresh/', { refresh: refreshToken });
          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          // Mark refreshing as done
          isRefreshing = false;
          onRefreshed(newAccessToken);

          // Update the Authorization header for this request
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest); // Retry the original request
        } catch (err) {
          // If the refresh token is invalid, logout the user
          if (err.response && err.response.status === 401) {
            apiClient.logout();
            return Promise.reject(err);
          }
          isRefreshing = false;
          return Promise.reject(err);
        }
      } else {
        // If there's already a refresh in progress, queue the request
        return new Promise((resolve) => {
          subscribeTokenRefresh((newAccessToken) => {
            // Update the original request's Authorization header and retry
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
            resolve(apiClient(originalRequest));
          });
        });
      }
    }

    return Promise.reject(error);
  }
);

export default {
  getUserEvents() {
    return apiClient.get(`/dashboard/events/`);
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
  refreshToken(refreshToken) {
    return apiClient.post('/token/refresh/', {
      refresh: refreshToken,
    });
  },
  logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      // If no refresh token exists, just clear and redirect
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete apiClient.defaults.headers.common['Authorization'];
      return;
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
    return apiClient.post('/logout/', { refresh_token: refreshToken })
  },
};
