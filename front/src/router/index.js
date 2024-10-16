import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TestPage from '@/components/TestPage.vue'
import PageTest from '@/components/PageTest.vue'
import Auth from '@/components/Auth.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/test',
      name:'test',
      component: TestPage
    },
    {
      path: '/',
      name:'auth',
      component: Auth
    }
  ]
})

export default router
