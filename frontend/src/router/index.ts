import { createRouter, createWebHistory } from 'vue-router'
import Users from '../pages/Users.vue'
import Api from '../pages/Api.vue'

const routes = [
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/api',
    name: 'Api',
    component: Api
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
