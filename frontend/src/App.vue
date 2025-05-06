<script setup lang="ts">
import { createRouter, createWebHistory } from 'vue-router'
import Auth from './components/Auth.vue';

import { useAuthStore } from './stores/useAuthStore'

// Importer le store
const authStore = useAuthStore();

// Gérer le changement de rôle utilisateur
const handleRoleChange = (newRole: string) => {
  authStore.updateRole(newRole);
  localStorage.setItem('user_role', newRole);
};

</script>

<template>
  <div>
    <header class="header">
      <div>
        <img src="./assets/logo.png" alt="Logo" class="logo" />
        <ul class="nav-links" v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
          <li><router-link to="/page1" class="nav-link">Page 1</router-link></li>
        </ul>
      </div>
      <Auth @updateRole="handleRoleChange" />
    </header>

    <!-- Affichage du contenu des routes -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
/* Styles généraux de la page */
body {
  margin: 0;
  font-family: 'Arial', sans-serif;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #333;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.logo {
  height: 100px;
  margin-bottom: 50px;
}

/* Navbar */
.navbar {
  background-color: #333333;
  padding: 10px 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-links {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-links li {
  margin: 0 15px;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-size: 16px;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #42b983;
}

/* Mobile menu toggle */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  height: 20px;
  cursor: pointer;
}

.bar {
  width: 25px;
  height: 3px;
  background-color: white;
  border-radius: 5px;
}
</style>