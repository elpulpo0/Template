<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { backend_url } from '../functions/utils'
import { useAuthStore } from '../stores/useAuthStore'

const authStore = useAuthStore()

const healthStatus = ref<string | null>(null)
const error = ref<string | null>(null)
const loading = ref<boolean>(false)

const healthCheck = async () => {
  loading.value = true
  healthStatus.value = null
  error.value = null
  try {
    const response = await axios.get(`${backend_url}/health`)
    healthStatus.value = response.data?.status || 'OK'
  } catch (err: any) {
    error.value = err.message || 'Error during health check'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  healthCheck()
})
</script>

<template>
  <div v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
    <div class="module">
      <h2>🩺 Health Check</h2>
      <button :disabled="loading" @click="healthCheck">
        {{ loading ? 'Checking...' : 'Check Again' }}
      </button>
      <p v-if="healthStatus">✅ Backend is up: {{ healthStatus }}</p>
      <p v-else-if="error">❌ Error: {{ error }}</p>
      <p v-else>⏳ Checking backend status...</p>
    </div>
  </div>
  <div v-else>
    <h2>🔒 Login required</h2>
    <p>Please log in to access the application's features.</p>
  </div>
</template>
