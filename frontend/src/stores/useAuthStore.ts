import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useAuthStore = defineStore('auth', () => {
  // Récupération persistée et réactive
  const userRole = useStorage<string>('role', '');
  const token = useStorage<string>('token', '');
  const email = useStorage<string>('email', '');
  const name = useStorage<string>('name', '');

  const updateRole = (newRole: string) => {
    userRole.value = newRole;
  };

  const setAuthData = (auth: { token: string; email: string; name: string; role: string }) => {
    token.value = auth.token;
    email.value = auth.email;
    name.value = auth.name;
    userRole.value = auth.role;
  };

  const logout = () => {
    token.value = '';
    email.value = '';
    name.value = '';
    userRole.value = '';
  };

  return {
    token,
    email,
    name,
    userRole,
    updateRole,
    setAuthData,
    logout
  };
});
