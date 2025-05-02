import axios from 'axios';
import { useAuthStore } from './stores/useAuthStore';

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
});

// Intercepteur global
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.href = '/login'; // ou une autre redirection
    }
    return Promise.reject(error);
  }
);

export default api;
