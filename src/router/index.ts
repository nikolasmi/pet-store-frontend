import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import { toast } from 'vue3-toastify'
import ProfileView from '@/views/ProfileView.vue'
import CartView from '@/views/CartView.vue'
import OrderView from '@/views/OrderView.vue'
import PetView from '@/views/PetView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/orders/user/:id',
      name: 'orders',
      component: OrderView
    },
    {
      path: '/pet/:id',
      name: 'pet',
      component: PetView
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); 
  const publicPages = ['home', 'register', 'login', 'pet'];

  if (!isAuthenticated && !publicPages.includes(to.name as string)) {
    toast.warning('morate biti prijavljeni') 
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
