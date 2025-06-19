<script setup lang="ts">
import { ref, watch } from 'vue';
import api from '../axios';
import axios from 'axios';
import { useAuthStore } from '../stores/useAuthStore';
import { backend_url } from '../functions/utils';

console.log(backend_url)

const authStore = useAuthStore();

interface User {
  email: string;
  name: string;
  password: string;
  role: string;
}

const emit = defineEmits<{
  (e: 'updateRole', role: string): void;
}>()

const email = ref('');
const name = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const user = ref<User | null>(null);
const isRegistering = ref(false);
const showEditForm = ref(false);
const newName = ref('');
const newEmail = ref('');
const newPassword = ref('');

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  } catch (e) {
    return true;
  }
}

function resetMessages() {
  errorMessage.value = '';
  successMessage.value = '';
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

    if (response.status === 200 && response.data.access_token) {
      authStore.setAuthData({
        token: response.data.access_token,
        email: email.value,
        name: '',
        role: ''
      });
      await fetchUser();
      resetMessages();
    } else {
      throw new Error("Token manquant ou statut inattendu");
    }

  } catch (error) {
    console.error(error);
    errorMessage.value = "Échec de la connexion. Vérifiez vos identifiants.";
  }
};

const register = async () => {
  try {
    if (password.value !== confirmPassword.value) {
      errorMessage.value = "Les mots de passe ne correspondent pas.";
      return;
    }

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
      confirmPassword.value = '';
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
  resetMessages();

  if (!newName.value.trim() && !newEmail.value.trim() && !newPassword.value.trim()) {
    errorMessage.value = 'Veuillez remplir au moins un champ pour mettre à jour votre profil.';
    return;
  }

  if (newPassword.value && newPassword.value !== confirmPassword.value) {
    errorMessage.value = "Les mots de passe ne correspondent pas.";
    return;
  }

  if (newPassword.value && newPassword.value.length < 6) {
    errorMessage.value = "Le mot de passe doit contenir au moins 6 caractères.";
    return;
  }

  if (newEmail.value && !newEmail.value.includes('@')) {
    errorMessage.value = "L'email saisi n'est pas valide.";
    return;
  }

  const payload: Record<string, string> = {};

  if (newName.value.trim()) payload.name = newName.value;
  if (newEmail.value.trim()) payload.email = newEmail.value;
  if (newPassword.value.trim()) payload.password = newPassword.value;

  try {
    await api.patch(`${backend_url}/users/users/me`, payload, {
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      }
    });

    successMessage.value = 'Profil mis à jour avec succès.';
    errorMessage.value = '';
    newEmail.value = '';
    newName.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    fetchUser();
  } catch (error) {
    console.error(error);
    errorMessage.value = "Une erreur est survenue lors de la mise à jour. Veuillez réessayer.";
  }
};

const fetchUser = async () => {
  try {
    const token = authStore.token;
    if (!token) throw new Error('Pas de token');

    const response = await api.get(`${backend_url}/users/users/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    authStore.setAuthData({
      token,
      email: authStore.email,
      name: response.data.name,
      role: response.data.role
    });

    user.value = {
      email: authStore.email,
      password: '',
      name: response.data.name.charAt(0).toUpperCase() + response.data.name.slice(1),
      role: response.data.role
    };

    emit('updateRole', response.data.role);

  } catch (error) {
    console.error(error);
    handleLogout();
  }
};

const handleLogout = () => {
  authStore.logout();
  user.value = null;
  resetMessages();
  emit('updateRole', '');
};

watch(() => authStore.token, async (newToken) => {
  if (newToken && !isTokenExpired(newToken)) {
    await fetchUser();
  } else {
    handleLogout();
  }
}, { immediate: true });
</script>

<template>
  <div :class="['auth-container', { 'wide': showEditForm }]">
    <div v-if="!authStore.token" class="auth-form">
      <h2 v-if="!isRegistering">Connexion</h2>
      <h2 v-else>Créer un compte</h2>

      <!-- Formulaire de connexion -->
      <form v-if="!isRegistering" @submit.prevent="login" :key="'login-form'">
        <input class="input-auth" type="email" id="email" v-model="email" placeholder="Email" autocomplete="username" />
        <input class="input-auth" type="password" id="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
        <button type="button" @click="login">Se connecter</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p>Pas encore de compte ? <a href="#" @click="isRegistering = true; resetMessages()">Créez un compte</a></p>
      </form>

      <!-- Formulaire d'inscription -->
      <form v-else @submit.prevent="register" :key="'register-form'">
        <input class="input-auth" type="email" v-model="email" placeholder="Email" autocomplete="username" />
        <input class="input-auth" type="name" v-model="name" placeholder="Nom" />
        <input class="input-auth" type="password" v-model="password" placeholder="Mot de passe" autocomplete="new-password" />
        <input class="input-auth" type="password" v-model="confirmPassword" placeholder="Confirmez le mot de passe" autocomplete="new-password" />
        <button type="submit">Créer un compte</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p>Déjà un compte ? <a href="#" @click="isRegistering = false; resetMessages()">Se connecter</a></p>
      </form>
    </div>

    <div v-else class="user-info">
      <h2>Bienvenue {{ user?.name }}</h2>
      <button @click="showEditForm = !showEditForm; resetMessages()">
        {{ showEditForm ? 'Annuler' : 'Voir / Modifier mon profil' }}
      </button>

      <div v-if="showEditForm" class="edit-form">
        <div class="user-details">
          <p><strong>Nom :</strong> {{ user?.name }}</p>
          <p><strong>Email :</strong> {{ user?.email }}</p>
          <p><strong>Rôle :</strong> {{ user?.role }}</p>
        </div>

        <div>
          <h2>Modifier mes informations</h2>
          <form class="form-grid">
            <label for="newName">Nom</label>
            <input class="input-auth" id="newName" type="text" v-model="newName" placeholder="nom" autocomplete="name" />

            <label for="newEmail">Email</label>
            <input class="input-auth" id="newEmail" type="email" v-model="newEmail" placeholder="email" autocomplete="email" />

            <label for="newPassword">Mot de passe</label>
            <input class="input-auth" id="newPassword" type="password" v-model="newPassword" placeholder="mot de passe" autocomplete="new-password" />

            <label for="confirmPassword">Confirmez le mot de passe</label>
            <input class="input-auth" id="confirmPassword" type="password" v-model="confirmPassword" placeholder="mot de passe" autocomplete="new-password" />
          </form>

          <button @click.prevent="updateProfile">Enregistrer les modifications</button>

          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </div>
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
  border: 1px solid magenta;
  font-family: 'Courier New', Courier, monospace;
  background-color: #000;
  color: magenta;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: magenta;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 24px;
  align-items: center;
}

.form-grid label {
  text-align: right;
  padding-right: 8px;
  color: magenta;
}

.form-grid input {
  width: 100%;
}

.input-auth {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid magenta;
  background-color: #000;
  color: magenta;
  font-family: 'Courier New', Courier, monospace;
}

.input-auth:focus {
  outline: none;
  border-color: magenta;
  background-color: #111;
}

button {
  padding: 12px;
  background-color: magenta;
  color: black;
  border: 1px solid magenta;
  font-size: 15px;
  cursor: pointer;
  font-weight: bold;
  font-family: 'Courier New', Courier, monospace;
  width: 100%;
}

button:hover {
  background-color: #00cc00;
}

p {
  text-align: center;
  font-size: 14px;
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
}

p.error {
  color: #ff4444;
  font-weight: bold;
}

p.success {
  color: magenta;
  font-weight: bold;
}

a {
  color: magenta;
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}

.user-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
  font-family: 'Courier New', Courier, monospace;
}

.edit-form {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.auth-container.wide {
  max-width: 800px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 24px;
  background-color: #000;
}

</style>
