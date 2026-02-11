export default {
	path: '/dashboard',
	name: 'Dashboard',
	component: () => import('@/layouts/Dashboard.vue'),
	redirect: '/dashboard/profile',
	children: [
		{
			path: 'profile',
			name: 'Profile',
			component: () => import('@/views/dashboard/Profile.vue'),
		},
		{
			path: 'reservations',
			name: 'Reservations',
			component: () => import('@/views/dashboard/Reservations.vue'),
		},
		{
			path: 'transactions',
			name: 'Transactions',
			component: () => import('@/views/dashboard/Transactions.vue'),
		},
	],
};
