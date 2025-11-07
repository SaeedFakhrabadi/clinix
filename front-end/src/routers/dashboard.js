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
			path: 'history',
			name: 'History',
			component: () => import('@/views/dashboard/History.vue'),
		},
		{
			path: 'doctors-list',
			name: 'DoctorsList',
			component: () => import('@/views/dashboard/DoctorsList.vue'),
		},
	],
};
