<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../axios';
import axios from 'axios';
import { useAuthStore } from '../stores/useAuthStore';
import { backend_url } from '../functions/utils';

const authStore = useAuthStore();

interface User {
  email: string;
  name: string;
  role: string;
}

const emit = defineEmits<{
  (e: 'updateRole', role: string): void;
}>()

const email = ref('');
const name = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isAuthenticated = ref(false);
const user = ref<User | null>(null);
const isRegistering = ref(false);
const showEditForm = ref(false);
const newName = ref('');
const newEmail = ref('');
const newPassword = ref('');

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
    const response = await api.post(
      `${backend_url}/users/users/`,
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

    if (response.status === 201) {
      errorMessage.value = '';
      successMessage.value = 'Inscription réussie, vous pouvez maintenant vous connecter.';
      email.value = '';
      name.value = '';
      password.value = '';
      isRegistering.value = false;

    }
  } catch (error: unknown) {
    console.error(error);

    if (axios.isAxiosError(error)) {
      errorMessage.value = error.response?.data.detail || 'Échec de la création du compte. Vérifiez les informations.';
    } else {
      errorMessage.value = 'Une erreur s\'est produite, veuillez réessayer plus tard.';
    }
  }
};

const updateProfile = async () => {
  errorMessage.value = '';
  successMessage.value = '';

  // Vérifier si le champ `newName` est requis
  if (!newName.value.trim()) {
    errorMessage.value = 'Le nom est requis et ne peut pas être vide.';
    return;
  }

  // Validation de l'email
  if (newEmail.value && !newEmail.value.includes('@')) {
    errorMessage.value = "L'email saisi n'est pas valide.";
    return;
  }

  // Validation du mot de passe
  if (newPassword.value && newPassword.value.length < 6) {
    errorMessage.value = "Le mot de passe doit contenir au moins 6 caractères.";
    return;
  }

  // Préparer les données à envoyer
  const token = localStorage.getItem('token');
  const payload: Record<string, string> = {};

  if (newName.value) payload.name = newName.value;
  if (newEmail.value) payload.email = newEmail.value;
  if (newPassword.value) payload.password = newPassword.value;

  // Si aucune donnée valide n'est à envoyer, ne pas envoyer de requête
  if (Object.keys(payload).length === 0) {
    errorMessage.value = 'Veuillez remplir au moins un champ pour mettre à jour votre profil.';
    return;
  }

  try {
    // Envoyer la requête API
    await api.patch(`${backend_url}/users/users/me`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    successMessage.value = 'Profil mis à jour avec succès.';
    errorMessage.value = '';
    showEditForm.value = false;
    fetchUser(); // Recharge les infos utilisateur
  } catch (error) {
    console.error(error);
    errorMessage.value = "Une erreur est survenue lors de la mise à jour. Veuillez réessayer.";
  }
};

const fetchUser = async () => {
  try {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('user_email') || '';

    if (!email) {
      throw new Error('Email not found');
    }

    const response = await api.get(`${backend_url}/users/users/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });

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
      <form v-if="!isRegistering" :key="'login-form'">
        <input type="email" v-model="email" placeholder="Email" autocomplete="username" />
        <input type="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
        <button @click.prevent="login">Se connecter</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p>Pas encore de compte ? <a href="#" @click="isRegistering = true">Créez un compte</a></p>
      </form>

      <!-- Formulaire d'inscription -->
      <form v-else :key="'register-form'">
        <input type="email" v-model="email" placeholder="Email" autocomplete="username" />
        <input type="name" v-model="name" placeholder="Nom" />
        <input type="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
        <button @click.prevent="register">Créer un compte</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p>Déjà un compte ? <a href="#" @click="isRegistering = false">Se connecter</a></p>
      </form>
    </div>

    <div v-else class="user-info">
      <p>Bienvenue {{ user?.name }}</p>
      <p>Tu as le rôle "{{ user?.role }}"</p>
      <button @click="showEditForm = !showEditForm">
        {{ showEditForm ? 'Annuler' : 'Modifier mon profil' }}
      </button>

      <div v-if="showEditForm" class="edit-form">
        <h3>Modifier mes informations</h3>

        <form>
          <label for="newName">Nouveau nom</label>
          <input
            id="newName"
            type="text"
            v-model="newName"
            placeholder="Entrez votre nouveau nom"
            autocomplete="name" />

          <label for="newEmail">Nouvel email</label>
          <input
            id="newEmail"
            type="email"
            v-model="newEmail"
            placeholder="Entrez votre nouvel email"
            autocomplete="email" />

          <label for="newPassword">Nouveau mot de passe</label>
          <input
            id="newPassword"
            type="password"
            v-model="newPassword"
            placeholder="Entrez votre nouveau mot de passe"
            autocomplete="new-password" />
        </form>

        <button @click.prevent="updateProfile">Enregistrer les modifications</button>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
      </div>
      <button @click="handleLogout">Se déconnecter</button>
    </div>
  </div>
</template>


<style scoped>
.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #2f2f2f;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Segoe UI', sans-serif;
  color: #fff;
}

.auth-form h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #00bcd4;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

input {
  padding: 12px 14px;
  border: 1px solid #555;
  border-radius: 8px;
  font-size: 15px;
  background-color: #444;
  color: #fff;
  transition: border-color 0.3s ease, background-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #00bcd4;
  background-color: #555;
  box-shadow: 0 0 0 2px rgba(0, 188, 212, 0.2);
}

button {
  padding: 12px;
  background-color: #00bcd4;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #0097a7;
}

p {
  text-align: center;
  font-size: 14px;
  margin: 0;
}

p.error {
  color: #f44336;
  font-weight: bold;
}

p.success {
  color: #4caf50;
  font-weight: bold;
}

a {
  color: #00bcd4;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

.user-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.edit-form {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
