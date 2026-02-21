export default {
	path: '/dashboard',
	name: 'Dashboard',
	component: () => import('@/layouts/Dashboard.vue'),
	redirect: '/dashboard/notifications',
	children: [
		{
			path: 'notifications',
			name: 'Notifications',
			component: () => import('@/views/dashboard/Notifications.vue'),
		},
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
		{
			path: 'complaint',
			name: 'Complaint',
			component: () => import('@/views/dashboard/Complaint.vue'),
		},
	],
};
