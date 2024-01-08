import { createRouter, createWebHistory } from 'vue-router'
import ListSeries from '../components/ListSeries.vue'
import Serie from '../components/Serie.vue'
import Admin from '../components/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'ListSeries',
    component: ListSeries,
  },
  {
    path: '/serie/:title',
    name: 'Serie',
    component: Serie,
    props: true
  },
  {
    path: '/admin/:title',
    name: 'Admin',
    component: Admin,
    props: true
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
