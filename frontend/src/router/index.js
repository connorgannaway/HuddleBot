import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/person',
      name: 'person',
      component: () => import('../views/PersonView.vue')
    },
    {
      path: '/daily',
      name: 'daily',
      component: () => import('../views/CheckInView.vue')
    }
  ]
})

export default router
