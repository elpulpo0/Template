<script setup lang="ts">
import Auth from './components/Auth.vue'
import Footer from './components/Footer.vue'
import { useAuthStore } from './stores/useAuthStore'

const authStore = useAuthStore();

const handleRoleChange = (newRole: string) => {
  authStore.updateRole(newRole);
  localStorage.setItem('user_role', newRole);
};
</script>

<template>
  <div>
    <header class="header">
      <div class="left-section">
        <img src="./assets/logo.png" alt="Logo" class="logo" />
        <ul class="nav-links" v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
          <li><router-link to="/users" class="nav-link">Users</router-link></li>
        </ul>
      </div>
      <Auth @updateRole="handleRoleChange" />
    </header>

    <!-- Affichage du contenu des routes -->
    <router-view></router-view>

    <Footer />
  </div>
</template>

<style scoped>
/* Police et couleurs type terminal */
body {
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  background-color: #000;
  color: #00ff00;
}

/* Header façon terminal */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  color: #00ff00;
}

/* Logo */
.logo {
  height: 100px;
  margin-bottom: 50px;
  filter: brightness(0) saturate(100%) invert(68%) sepia(95%) saturate(330%) hue-rotate(74deg) brightness(93%) contrast(96%);
}

/* Navbar */
.navbar {
  background-color: #000;
  padding: 10px 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
  border-bottom: 1px solid #00ff00;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Liens de navigation façon terminal */
.nav-links {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 25px;
}

.nav-link {
  text-decoration: none;
  color: cyan;
  font-size: 16px;
  transition: color 0.3s;
  font-family: 'Courier New', Courier, monospace;
}

/* Bouton menu hamburger (mobile) */
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
  background-color: #00ff00;
  border-radius: 0;
}
</style>
