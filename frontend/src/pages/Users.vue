<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { auth_url } from '../functions/utils'
import { useAuthStore } from '../stores/useAuthStore'
const authStore = useAuthStore();

type User = {
  id: number
  name: string
  email: string
  role: string
  is_active: boolean
  tokens?: { app_name: string, created_at: string, expires_at: string, revoked: boolean }[]
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const editingUserId = ref<number | null>(null);
const editName = ref('');
const editEmail = ref('');
const editPassword = ref('');

const fetchUsers = async () => {
  loading.value = true;
  error.value = '';
  try {
    const { data } = await axios.get(`${auth_url}/users/users`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });

    if (Array.isArray(data)) {
      users.value = data;
    } else {
      throw new Error('Invalid user data');
    }

    const { data: tokensData } = await axios.get(`${auth_url}/auth/refresh-tokens`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });

    tokensData.forEach((tokenData: any) => {
      const user = users.value.find(user => user.id === tokenData.user_id);
      if (user) {
        if (!user.tokens) {
          user.tokens = [];
        }
        if (!tokenData.revoked) {
          user.tokens.push({
            app_name: tokenData.app,
            created_at: tokenData.created_at,
            expires_at: tokenData.expires_at,
            revoked: tokenData.revoked
          });
        }
      }
    });
  } catch (err: any) {
    console.error('Error while fetching users and tokens', err);

    if (axios.isAxiosError(err)) {
      if (err.response?.status === 403) {
        error.value = '⛔ Access denied: you do not have permission to view the users.';
      } else if (err.response?.status === 401) {
        error.value = '🔐 Session expired. Please log in again.';
      } else {
        error.value = 'An error occurred while fetching users and tokens.';
      }
    } else {
      error.value = '	Unknown error.';
    }
  } finally {
    loading.value = false;
  }
};

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

    await axios.patch(`${auth_url}/users/users/${userId}`, updatePayload, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });

    cancelEdit();
    fetchUsers();
  } catch (err) {
    console.error('Update error', err);
    error.value = 'Error while updating the user.';
  }
};

const updateRole = async (userId: number, newRole: string) => {
  try {
    await axios.patch(`${auth_url}/users/users/${userId}/role`, { role: newRole }, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    fetchUsers()
  } catch (err) {
    console.error('Error while updating the role', err)
    error.value = 'Error while updating the role'
  }
}

const deleteUser = async (userId: number) => {
  try {
    await axios.delete(`${auth_url}/users/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    fetchUsers()
  } catch (err) {
    console.error('Error while deleting the user', err)
    error.value = 'Error while deleting the user'
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
  { immediate: true }
);

</script>

<template>
  <div v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
    <div v-if="loading">Loading users...</div>
    <div v-if="error">{{ error }}</div>

    <div v-if="users.length" class="module">
      <h2>Users</h2>
      <table>
        <thead>
          <tr>
            <th class="recoltes small">Name</th>
            <th class="recoltes small">Role</th>
            <th class="recoltes small">Active</th>
            <th class="recoltes small">Last Session</th>
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
              <ul class="token-list">
                <li v-for="token in user.tokens" :key="token.app_name">
                  <strong>{{ token.app_name }}</strong>: {{ new Date(token.created_at).toLocaleDateString() }}
                </li>
              </ul>
            </td>
            <td v-if="['admin'].includes(authStore.userRole) && editingUserId !== user.id">
              <button class="delete-btn" @click="deleteUser(user.id)">&#10060;</button>
              <button class="edit-btn" @click="startEditing(user)">&#9998;</button>
            </td>
            <td v-if="['admin'].includes(authStore.userRole) && editingUserId == user.id">
              <form class="form-section">
                <input class="form-input" v-model="editName" placeholder="Name" />
                <input class="form-input" v-model="editEmail" placeholder="Email" />
                <input class="form-input" v-model="editPassword" placeholder="Password" />
                <button v-if="user.role === 'reader'" @click="updateRole(user.id, 'editor')">Make Editor</button>
              </form>
              <button @click="submitEdit(user.id)">Save</button>
              <button @click="cancelEdit">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else>
    <h2>🔒 Login required</h2>
    <p>Please log in to access the application's features.</p>
  </div>
</template>

<style scoped>
.token-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
