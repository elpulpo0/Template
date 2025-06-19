import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { readFileSync } from 'fs'
import { resolve } from 'path'

const packageJson = JSON.parse(readFileSync('./package.json', 'utf-8'))

const months = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]

const now = new Date()
const formattedDate = `${String(now.getDate()).padStart(2, '0')} ${months[now.getMonth()]} ${now.getFullYear()}`

let buildMeta = { hash: 'inconnu', message: 'message indisponible' }
try {
  const buildMetaPath = resolve(__dirname, 'build-meta.json')
  const raw = readFileSync(buildMetaPath, 'utf-8')
  buildMeta = JSON.parse(raw)
} catch (e) {
  console.warn('No build-meta.json found, using defaults.')
}

export default defineConfig({
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
})