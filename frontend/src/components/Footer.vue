<template>
  <footer class="footer">
    <p class="copyright">
      © {{ new Date().getFullYear() }} El Pulpo — All rights reserved.
    </p>
    <p>
      {{ app_name ? (app_name.charAt(0).toUpperCase() + app_name.slice(1)) : '' }} v{{ version }} – last update: {{ buildDate }}
    </p>
    <p class="copyright">
      commit: <a :href="commitUrl" target="_blank" rel="noopener">{{ commitHash }}</a> ({{ commitMessage }})
    </p>
  </footer>
</template>

<script setup>
const version = import.meta.env.VITE_APP_VERSION
const buildDate = import.meta.env.VITE_APP_BUILD_DATE
const commitHash = import.meta.env.VITE_APP_LAST_COMMIT_HASH
const commitMessage = import.meta.env.VITE_APP_LAST_COMMIT_MESSAGE
const githubUrl = import.meta.env.VITE_GITHUB_URL
const commitUrl = `${githubUrl}/commit/${commitHash}`
const app_name = import.meta.env.VITE_APP_NAME
</script>

<style scoped>
.footer {
  margin-top: 50px;
  text-align: center;
  font-size: 0.95rem;
}

.footer-link {
  color: #00bcd4;
  text-decoration: none;
  font-weight: 600;
}

.footer-link:hover {
  text-decoration: underline;
}

.copyright {
  margin-top: 8px;
  font-size: 0.85rem;
  color: orange;
}
</style>
