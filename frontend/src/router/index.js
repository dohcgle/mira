import { createRouter, createWebHistory } from 'vue-router'
import LoanWizard from '@/views/LoanWizard.vue'
import Login from '@/views/Login.vue'
import { authStore } from '../store/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      redirect: '/loan-wizard'
    },
    {
      path: '/contracts',
      name: 'contracts',
      component: () => import('../views/ContractList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/contracts/:id',
      name: 'contract-detail',
      component: () => import('../views/ContractDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/loan-wizard',
      name: 'loan-wizard',
      component: LoanWizard,
      meta: { requiresAuth: true }
    }
  ],
})

// Sahifa o'zgarishidan oldin tekshirish
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.accessToken) {
    // Agar sahifa auth talab qilsa va token bo'lmasa -> login'ga
    next('/login')
  } else if (to.name === 'login' && authStore.accessToken) {
    // Agar kiritilgan bo'lsa va login'ga kirsak -> bosh sahifaga
    next('/')
  } else {
    next()
  }
})

export default router

