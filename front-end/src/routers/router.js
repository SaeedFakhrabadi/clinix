import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    redirect: '/dashboard/home',
  },
  {
    path: '/dashboard',
    redirect: '/dashboard/home',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/layouts/Dashboard.vue'),
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
      },
      {
        path: 'sign-up',
        name: 'SignUp',
        component: () => import('@/views/SignUp.vue'),
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard/home',
  },
];

const alwaysScrollToTop = ['Home'];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (alwaysScrollToTop.includes(to.name) && to.name !== from.name) {
      return { top: 0 };
    }

    return false;
  },
});

router.afterEach((to, from) => {
  if (alwaysScrollToTop.includes(to.name) && to.name === from.name) {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  }
});

export default router;
