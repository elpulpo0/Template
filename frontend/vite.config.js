import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { readFileSync } from 'fs'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  // Lecture de version dans package.json
  const packageJson = JSON.parse(readFileSync('./package.json', 'utf-8'))

  // Formattage de la date
  const months = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ]
  const now = new Date()
  const formattedDate = `${String(now.getDate()).padStart(2, '0')} ${months[now.getMonth()]} ${now.getFullYear()}`

  // Lecture du fichier build-meta.json si dispo
  let buildMeta = { hash: 'inconnu', message: 'message indisponible' }
  try {
    const buildMetaPath = resolve(__dirname, 'build-meta.json')
    const raw = readFileSync(buildMetaPath, 'utf-8')
    buildMeta = JSON.parse(raw)
  } catch (e) {
    console.warn('⚠️ Aucun fichier build-meta.json trouvé, valeurs par défaut utilisées.')
  }

  return {
    server: {
      port: parseInt(env.VITE_PORT) || 5173,
    },
    plugins: [vue()],
    build: {
      sourcemap: true,
    },
    define: {
      'import.meta.env.VITE_APP_VERSION': JSON.stringify(packageJson.version),
      'import.meta.env.VITE_APP_BUILD_DATE': JSON.stringify(formattedDate),
      'import.meta.env.VITE_APP_LAST_COMMIT_HASH': JSON.stringify(buildMeta.hash),
      'import.meta.env.VITE_APP_LAST_COMMIT_MESSAGE': JSON.stringify(buildMeta.message),
    },
    base: './',
  }
})
