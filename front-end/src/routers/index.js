import { createRouter, createWebHistory } from 'vue-router';
import { useCurrentUserStore } from '@/stores/currentUser';

import homeRoutes from './home';
import authRoutes from './auth';
import dashboardRoutes from './dashboard';
import notFoundRoutes from './notFound';

const routes = [
	{
		path: '/',
		redirect: '/home/landing',
	},
	homeRoutes,
	authRoutes,
	dashboardRoutes,
	notFoundRoutes,
];

const alwaysScrollToTop = ['Landing'];

const router = createRouter({
	history: createWebHistory(),
	routes,
	scrollBehavior(to, from, savedPosition) {
		if (savedPosition) return savedPosition;
		if (alwaysScrollToTop.includes(to.name)) return { top: 0 };
		return {};
	},
});

// Navigation guard
router.beforeEach((to, from, next) => {
	const currentUserStore = useCurrentUserStore();
	const isAuthenticated = !!currentUserStore.currentUser;

	if (to.path.startsWith('/dashboard') && !isAuthenticated) {
		return next('/auth/login');
	}

	if (to.path.startsWith('/auth') && isAuthenticated) {
		return next('/dashboard/profile');
	}

	next();
});

export default router;
