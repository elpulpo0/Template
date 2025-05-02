import { createRouter, createWebHistory } from 'vue-router'
import Page1 from '../components/Page1.vue'

const routes = [
  {
    path: '/page1',
    name: 'Page 1',
    component: Page1
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
