<script setup lang="ts">
import { ref, onMounted  } from 'vue';
import api from '../axios';
import { useAuthStore } from '../stores/useAuthStore';

const authStore = useAuthStore();

interface User {
  email: string;
  name: string;
  role: string;
}

const emit = defineEmits<{
  (e: 'updateRole', role: string): void;
}>();

const backend_url = import.meta.env.VITE_BACKEND_URL;
const email = ref('');
const name = ref('');
const password = ref('');
const errorMessage = ref('');
const isAuthenticated = ref(false);
const user = ref<User | null>(null);
const isRegistering = ref(false);

// Vérifie si l'utilisateur est déjà connecté
onMounted(() => {
  const token = localStorage.getItem('token');
  if (token && !isTokenExpired(token)) {
    fetchUser();
  } else {
    handleLogout(); // Déconnexion forcée si token expiré
  }
});


function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  } catch (e) {
    return true; // Si décodage échoue, considère le token invalide
  }
}

const login = async () => {
  try {
    const response = await api.post(
      `${backend_url}/auth/login`, 
      new URLSearchParams({
        username: email.value,
        password: password.value,
      }),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      }
    );

    // Enregistre le token reçu dans le localStorage
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user_email', email.value);
    localStorage.setItem('name', response.data.name);
    isAuthenticated.value = true;
    fetchUser();
  } catch (error) {
    console.error(error);
    errorMessage.value = "Échec de la connexion. Vérifiez vos identifiants.";
  }
};

const register = async () => {
  try {
    // Envoi des données pour créer un utilisateur
    const response = await api.post(
      `${backend_url}/auth/users/`,  // Route pour créer un utilisateur
      {
        email: email.value,
        name: name.value,
        password: password.value,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    // Si la réponse est réussie, passer à la vue de connexion
    if (response.status === 201) {
      // On change l'état pour afficher le formulaire de connexion
      isRegistering.value = false;  // Basculer sur le formulaire de connexion
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = 'Échec de la création du compte. Vérifiez les informations.';
  }
};

const fetchUser = async () => {
  try {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('user_email') || '';

    // Assurer que l'email est une chaîne de caractères
    if (!email) {
      throw new Error('Email not found');
    }

    // Appel à l'API pour récupérer les informations de l'utilisateur
    const response = await api.get(`${backend_url}/auth/users/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Vérification si la réponse est vide
    if (!response || !response.data || Object.keys(response.data).length === 0) {
      console.log('Réponse vide ou invalide reçue:', response);
      throw new Error('La réponse de l\'API est vide ou invalide');
    }

    authStore.updateRole(response.data.role);

    user.value = { 
    email, 
    name: response.data.name.charAt(0).toUpperCase() + response.data.name.slice(1), 
    role: response.data.role 
  };

    isAuthenticated.value = true;
  } catch (error) {
    // En cas d'erreur, nettoyer le token et l'email
    console.error('Erreur lors de la récupération de l\'utilisateur:', error);
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_email');
    localStorage.removeItem('name');
    isAuthenticated.value = false;
  }
};

const handleLogout = () => {
  authStore.logout();
  isAuthenticated.value = false;
  user.value = null;
  emit('updateRole', '');
};

</script>

<template>
    <div class="auth-container">
      <div v-if="!isAuthenticated" class="auth-form">
        <h2 v-if="!isRegistering">Connexion</h2>
        <h2 v-else>Créer un compte</h2>
  
        <!-- Formulaire de connexion -->
        <form v-if="!isRegistering">
          <input type="email" v-model="email" placeholder="Email" autocomplete="username" />
          <input type="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
          <button @click.prevent="login">Se connecter</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          <p>Pas encore de compte ? <a href="#" @click="isRegistering = true">Créez un compte</a></p>
        </form>
  
        <!-- Formulaire d'inscription -->
        <form v-else>
          <input type="email" v-model="email" placeholder="Email" autocomplete="username" />
          <input type="name" v-model="name" placeholder="Nom" />
          <input type="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
          <button @click.prevent="register">Créer un compte</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          <p>Déjà un compte ? <a href="#" @click="isRegistering = false">Se connecter</a></p>
        </form>
      </div>
  
      <div v-else class="user-info">
        <p>Bienvenue sur Ground Control {{ user?.name }}, tu as le rôle {{ user?.role }}.</p>
        <button class="button-auth" @click="handleLogout">Se déconnecter</button>
      </div>
    </div>
  </template>
  
  <style scoped>
  .auth-container {
    width: 30%;
    padding: 30px;
    background-color: #3f3f3f;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', sans-serif;
  }
  
  .auth-form h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #008791;
  }
  
  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  input {
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s ease;
  }
  
  input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.15);
  }
  
  button {
    padding: 10px;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  p {
    text-align: center;
    font-size: 14px;
  }
  
  p.error {
    color: #e74c3c;
    font-weight: bold;
  }
  
  a {
    color: #007bff;
    text-decoration: none;
    font-weight: 500;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  .user-info {
    text-align: center;
  }
  
  .button-auth {
    margin-top: 20px;
  }
  </style>
  