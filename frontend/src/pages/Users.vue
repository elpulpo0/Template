<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { backend_url } from '../functions/utils'
import { useAuthStore } from '../stores/useAuthStore'
const authStore = useAuthStore();

type User = {
  id: number
  name: string
  email: string
  role: string
  is_active: boolean
  tokens?: { created_at: string, expires_at: string, revoked: boolean }[]
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const editingUserId = ref<number | null>(null);
const editName = ref('');
const editEmail = ref('');
const editPassword = ref('');

const fetchUsers = async () => {
  loading.value = true
  try {
    const { data } = await axios.get(`${backend_url}/users/users`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    if (Array.isArray(data)) {
      users.value = data
    } else {
      throw new Error('Données utilisateurs invalides')
    }

    // Ensuite, récupérer les tokens associés à chaque utilisateur
    const { data: tokensData } = await axios.get(`${backend_url}/auth/refresh-tokens`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    // Associer les tokens aux utilisateurs
    tokensData.forEach((tokenData: any) => {
      const user = users.value.find(user => user.id === tokenData.user_id)
      if (user) {
        if (!user.tokens) {
          user.tokens = []
        }
        if (!tokenData.revoked) {
          user.tokens.push({
            created_at: tokenData.created_at,
            expires_at: tokenData.expires_at,
            revoked: tokenData.revoked
          })
        }
      }
    })
  } catch (err) {
    console.error('Erreur lors de la récupération des utilisateurs et tokens', err)
    error.value = 'Une erreur est survenue lors de la récupération des utilisateurs et tokens.'
  } finally {
    loading.value = false
  }
}

const startEditing = (user: User) => {
  editingUserId.value = user.id;
  editName.value = user.name;
  editEmail.value = '';
  editPassword.value = '';
};

const cancelEdit = () => {
  editingUserId.value = null;
  editName.value = '';
  editEmail.value = '';
  editPassword.value = '';
};

const submitEdit = async (userId: number) => {
  try {
    const updatePayload: any = {};
    if (editName.value) updatePayload.name = editName.value;
    if (editEmail.value) updatePayload.email = editEmail.value;
    if (editPassword.value) updatePayload.password = editPassword.value;

    await axios.patch(`${backend_url}/users/users/${userId}`, updatePayload, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });

    cancelEdit();
    fetchUsers();
  } catch (err) {
    console.error('Erreur de mise à jour', err);
    error.value = 'Erreur lors de la mise à jour de l’utilisateur.';
  }
};

const updateRole = async (userId: number, newRole: string) => {
  try {
    await axios.patch(`${backend_url}/users/users/${userId}/role`, { role: newRole }, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    fetchUsers()
  } catch (err) {
    console.error('Erreur lors de la mise à jour du rôle', err)
    error.value = 'Erreur lors de la mise à jour du rôle.'
  }
}

const deleteUser = async (userId: number) => {
  try {
    await axios.delete(`${backend_url}/users/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    fetchUsers()
  } catch (err) {
    console.error('Erreur lors de la suppression de l\'utilisateur', err)
    error.value = 'Erreur lors de la suppression de l\'utilisateur.'
  }
}

watch(
  () => authStore.token,
  (newToken) => {
    if (newToken) {
      fetchUsers();
    } else {
      users.value = [];
    }
  },
  { immediate: true } // pour appeler aussi au montage
);

</script>

<template>
  <div v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
    <div v-if="loading">Chargement des utilisateurs...</div>
    <div v-if="error">{{ error }}</div>

    <div v-if="users.length" class="module">
      <h2>Utilisateurs</h2>
      <table>
        <thead>
          <tr>
            <th class="recoltes small">Nom</th>
            <th class="recoltes small">Rôle</th>
            <th class="recoltes small">Actif</th>
            <th class="recoltes small">Connexions</th>
            <th v-if="['admin'].includes(authStore.userRole)" class="recoltes small">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name.charAt(0).toUpperCase() + user.name.slice(1) }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span v-if="user.is_active">✔️</span>
              <span v-else>❌</span>
            </td>
            <td>
              <!-- Affichage des tokens associés à l'utilisateur -->
              <ul>
                <div v-for="token in user.tokens">
                  {{ new Date(token.created_at).toLocaleDateString() }}
                </div>
              </ul>
            </td>
            <td v-if="['admin'].includes(authStore.userRole) && editingUserId !== user.id">
              <button class="delete-btn" @click="deleteUser(user.id)">&#10060;</button>
              <button class="edit-btn" @click="startEditing(user)">&#9998;</button>
            </td>
            <td v-if="['admin'].includes(authStore.userRole) && editingUserId == user.id">
              <form class="form-section">
                <input class="form-input" v-model="editName" placeholder="Nom" />
                <input class="form-input" v-model="editEmail" placeholder="Email" />
                <input class="form-input" v-model="editPassword" placeholder="Mot de passe" />
                <button v-if="user.role === 'reader'" @click="updateRole(user.id, 'editor')">Rendre Editeur</button>
              </form>
              <button @click="submitEdit(user.id)">Enregistrer</button>
              <button @click="cancelEdit">Annuler</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <!-- Message si l'utilisateur n'est pas connecté -->
  <div v-else>
    <h2>🔒 Connexion requise</h2>
    <p>Veuillez vous connecter pour accéder aux fonctionnalités de l’application.</p>
  </div>
</template>
