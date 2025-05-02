import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useAuthStore = defineStore('auth', () => {
  // Utilisation de useStorage pour persister le rôle dans localStorage
  const userRole = useStorage<string>('user_role', '');

  // Fonction pour mettre à jour le rôle
  const updateRole = (newRole: string) => {
    userRole.value = newRole;
    localStorage.setItem('user_role', newRole);
  };

  const logout = () => {
    userRole.value = '';
    localStorage.removeItem('token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('name');
    localStorage.removeItem('user_role');
  };
  
  return { userRole, updateRole, logout };

});
