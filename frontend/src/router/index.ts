import { createRouter, createWebHistory } from 'vue-router'
import Users from '../pages/Users.vue'

const routes = [
  {
    path: '/users',
    name: 'Users',
    component: Users
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
