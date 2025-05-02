<script setup lang="ts">

import { useAuthStore } from '../stores/useAuthStore'
const authStore = useAuthStore();
</script>

<template>
  <div>
    <div v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)">
      <h1>Page1</h1>
    </div>
    
    <!-- Modules -->
    <div v-if="['admin', 'editor', 'reader'].includes(authStore.userRole)" class="module">
      <div>
        <h2>Module 1</h2>
        <p>Bonjour, votre rôle est {{  authStore.userRole }}</p>
      </div>
    </div>

</div>
</template>
